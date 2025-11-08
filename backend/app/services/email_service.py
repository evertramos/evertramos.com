import aiosmtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
from jinja2 import Template
from email.utils import parseaddr
import re

from app.config import settings
from app.models.payment import PaymentRequest, PaymentType

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_user = settings.smtp_user
        self.smtp_password = settings.smtp_password
    
    def _validate_email(self, email: str) -> bool:
        """Validate email format and security"""
        if not email or len(email) > 254:
            return False
        
        # Parse email address
        name, addr = parseaddr(email)
        if not addr or '@' not in addr:
            return False
        
        # Basic regex validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, addr))
    
    def _sanitize_subject(self, subject: str) -> str:
        """Sanitize email subject to prevent header injection"""
        # Remove newlines and carriage returns
        return re.sub(r'[\r\n]', '', subject)[:200]
    
    async def send_email(self, to_emails: List[str], subject: str, html_content: str, text_content: str = None):
        """Send email using SMTP"""
        try:
            # Validate all email addresses
            valid_emails = [email for email in to_emails if self._validate_email(email)]
            if not valid_emails:
                logger.error("No valid email addresses provided")
                return False
            
            # Sanitize subject
            safe_subject = self._sanitize_subject(subject)
            message = MIMEMultipart("alternative")
            message["Subject"] = safe_subject
            message["From"] = self.smtp_user or "noreply@ezyba.com"
            message["To"] = ", ".join(valid_emails)
            
            if text_content:
                text_part = MIMEText(text_content, "plain")
                message.attach(text_part)
            
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Configure SMTP based on environment
            smtp_kwargs = {
                "hostname": self.smtp_host,
                "port": self.smtp_port,
            }
            
            # Only add authentication for production (AWS SES)
            if self.smtp_user and self.smtp_password:
                smtp_kwargs.update({
                    "start_tls": True,
                    "username": self.smtp_user,
                    "password": self.smtp_password,
                })
            
            await aiosmtplib.send(message, **smtp_kwargs)
            
            logger.info(f"Email sent successfully to: {valid_emails}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    async def send_payment_confirmation(self, payment_request: PaymentRequest, payment_id: str, success: bool):
        """Send payment confirmation emails"""
        
        # Email to customer
        customer_subject = "Payment Confirmation - Ezyba" if success else "Payment Failed - Ezyba"
        customer_template = Template("""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #333;">{{ 'Payment Confirmed!' if success else 'Payment Failed' }}</h2>
            
            {% if success %}
            <p>Hi {{ name }},</p>
            <p>Your payment has been successfully processed!</p>
            {% else %}
            <p>Hi {{ name }},</p>
            <p>Unfortunately, your payment could not be processed. Please try again or contact support.</p>
            {% endif %}
            
            <div style="background: #f5f5f5; padding: 20px; border-radius: 5px; margin: 20px 0;">
                <h3>Payment Details:</h3>
                <p><strong>Amount:</strong> {{ amount_display }}</p>
                <p><strong>Type:</strong> {{ payment_type_display }}</p>
                <p><strong>Payment ID:</strong> {{ payment_id }}</p>
            </div>
            
            <p>If you have any questions, please don't hesitate to contact us.</p>
            <p>Best regards,<br>Ezyba Team</p>
        </body>
        </html>
        """)
        
        # Format amount for display
        amount_display = f"${payment_request.amount / 100:.2f}" if payment_request.currency.value == "usd" else f"R${payment_request.amount / 100:.2f}"
        payment_type_display = {
            PaymentType.ONE_TIME: "One-time payment",
            PaymentType.MONTHLY: "Monthly subscription",
            PaymentType.YEARLY: "Yearly subscription"
        }.get(payment_request.payment_type, "Unknown")
        
        customer_html = customer_template.render(
            success=success,
            name=payment_request.name,
            amount_display=amount_display,
            payment_type_display=payment_type_display,
            payment_id=payment_id
        )
        
        # Send to customer
        await self.send_email(
            [payment_request.email],
            customer_subject,
            customer_html
        )
        
        # Email to admin
        admin_subject = f"New Payment {'Received' if success else 'Failed'} - Ezyba"
        admin_template = Template("""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>{{ 'New Payment Received' if success else 'Payment Failed' }}</h2>
            
            <div style="background: #f5f5f5; padding: 20px; border-radius: 5px;">
                <h3>Customer Information:</h3>
                <p><strong>Name:</strong> {{ name }}</p>
                <p><strong>Email:</strong> {{ email }}</p>
                {% if phone %}<p><strong>Phone:</strong> {{ phone }}</p>{% endif %}
                
                <h3>Payment Details:</h3>
                <p><strong>Amount:</strong> {{ amount_display }}</p>
                <p><strong>Currency:</strong> {{ currency }}</p>
                <p><strong>Type:</strong> {{ payment_type_display }}</p>
                <p><strong>Payment ID:</strong> {{ payment_id }}</p>
                <p><strong>Status:</strong> {{ 'SUCCESS' if success else 'FAILED' }}</p>
            </div>
        </body>
        </html>
        """)
        
        admin_html = admin_template.render(
            success=success,
            name=payment_request.name,
            email=payment_request.email,
            phone=payment_request.phone,
            amount_display=amount_display,
            currency=payment_request.currency.value.upper(),
            payment_type_display=payment_type_display,
            payment_id=payment_id
        )
        
        # Send to admin emails
        await self.send_email(
            settings.notification_email_list,
            admin_subject,
            admin_html
        )