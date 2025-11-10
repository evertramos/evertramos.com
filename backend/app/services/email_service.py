import aiosmtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
from jinja2 import Template
from email.utils import parseaddr
import re
import html

from app.config import settings
from app.models.payment import PaymentRequest, PaymentType
from app.templates.email_templates import EMAIL_TEMPLATES, BASE_EMAIL_TEMPLATE

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
            
            logger.info(f"[MAILPIT] Email sent successfully to: {valid_emails}")
            return True
            
        except Exception as e:
            logger.error(f"[MAILPIT] Failed to send email: {e}")
            return False
    
    async def send_payment_confirmation(self, payment_request: PaymentRequest, payment_id: str, success: bool):
        """Send payment confirmation emails"""
        
        # Get language (default to pt)
        lang = payment_request.language or "pt"
        templates = EMAIL_TEMPLATES.get(lang, EMAIL_TEMPLATES["pt"])
        
        logger.info(f"[MAILPIT] Sending payment confirmation - Success: {success}, Language: {lang}, Email: {payment_request.email}")
        
        # Format amount for display
        currency_symbol = settings.usd_symbol if payment_request.currency.value == "usd" else settings.brl_symbol
        amount_display = f"{currency_symbol}{payment_request.amount / 100:.2f}"
        
        # Get payment type display text
        payment_type_display = templates["payment_types"].get(
            payment_request.payment_type.value, 
            payment_request.payment_type.value
        )
        
        # Customer email
        template_key = "customer_success" if success else "customer_failed"
        customer_template = templates[template_key]
        
        customer_subject = customer_template["subject"].format(company_name=settings.company_name)
        
        # Render content first
        content_html = Template(customer_template["content"]).render(
            name=html.escape(payment_request.name),
            amount_display=amount_display,
            payment_type_display=payment_type_display,
            payment_id=payment_id,
            support_email=settings.support_email,
            company_name=settings.company_name
        )
        
        # Then render full email with base template
        customer_html = Template(BASE_EMAIL_TEMPLATE).render(
            lang=lang,
            subject=customer_subject,
            header_title="Pagamento" if lang == "pt" else "Payment",
            content=content_html,
            company_name=settings.company_name,
            support_email=settings.support_email
        )
        
        # Send to customer
        await self.send_email(
            [payment_request.email],
            customer_subject,
            customer_html
        )
        
        # Admin email (always in Portuguese)
        admin_subject = f"{'Novo Pagamento Recebido' if success else 'Falha no Pagamento'} - {settings.company_name}"
        admin_html = self._render_admin_template(
            success, payment_request, amount_display, payment_type_display, payment_id
        )
        
        # Send to admin emails
        await self.send_email(
            settings.notification_email_list,
            admin_subject,
            admin_html
        )
    
    def _render_admin_template(self, success: bool, payment_request: PaymentRequest, amount_display: str, payment_type_display: str, payment_id: str) -> str:
        """Render admin email template"""
        template = Template("""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>{{ 'Novo Pagamento Recebido' if success else 'Falha no Pagamento' }} - {{ company_name }}</h2>
            
            <div style="background: #f5f5f5; padding: 20px; border-radius: 5px;">
                <h3>Informações do Cliente:</h3>
                <p><strong>Nome:</strong> {{ name }}</p>
                <p><strong>Email:</strong> {{ email }}</p>
                {% if phone %}<p><strong>Telefone:</strong> {{ phone }}</p>{% endif %}
                <p><strong>Idioma:</strong> {{ language }}</p>
                
                <h3>Detalhes do Pagamento:</h3>
                <p><strong>Valor:</strong> {{ amount_display }}</p>
                <p><strong>Moeda:</strong> {{ currency }}</p>
                <p><strong>Tipo:</strong> {{ payment_type_display }}</p>
                <p><strong>ID do Pagamento:</strong> {{ payment_id }}</p>
                <p><strong>Status:</strong> {{ 'SUCESSO' if success else 'FALHA' }}</p>
            </div>
        </body>
        </html>
        """)
        
        return template.render(
            success=success,
            name=html.escape(payment_request.name),
            email=html.escape(payment_request.email),
            phone=html.escape(payment_request.phone) if payment_request.phone else None,
            language=payment_request.language or "pt",
            amount_display=amount_display,
            currency=payment_request.currency.value.upper(),
            payment_type_display=payment_type_display,
            payment_id=payment_id,
            company_name=settings.company_name
        )