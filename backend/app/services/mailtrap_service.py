import mailtrap as mt
import logging
from typing import List
from jinja2 import Template
import html

from app.config import settings
from app.models.payment import PaymentRequest, PaymentType
from app.templates.email_templates import EMAIL_TEMPLATES, BASE_EMAIL_TEMPLATE

logger = logging.getLogger(__name__)


class MailtrapService:
    def __init__(self):
        self.client = mt.MailtrapClient(token=settings.mailtrap_api_token)
        self.sender_email = settings.sender_email
        self.sender_name = settings.sender_name
    
    async def send_payment_confirmation(self, payment_request: PaymentRequest, payment_id: str, success: bool):
        """Send payment confirmation emails using Mailtrap API"""
        
        # Get language (default to pt)
        lang = payment_request.language or "pt"
        templates = EMAIL_TEMPLATES.get(lang, EMAIL_TEMPLATES["pt"])
        
        logger.info(f"[MAILTRAP] Sending payment confirmation - Success: {success}, Language: {lang}, Email: {payment_request.email}")
        
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
        
        customer_mail = mt.Mail(
            sender=mt.Address(email=self.sender_email, name=self.sender_name),
            to=[mt.Address(email=payment_request.email)],
            subject=customer_subject,
            html=customer_html,
            category="Payment Confirmation"
        )
        
        # Admin email (always in Portuguese)
        admin_subject = f"{'Novo Pagamento Recebido' if success else 'Falha no Pagamento'} - {settings.company_name}"
        admin_html = self._render_admin_template(
            success, payment_request, amount_display, payment_type_display, payment_id
        )
        
        admin_emails = [mt.Address(email=email) for email in settings.notification_email_list]
        admin_mail = mt.Mail(
            sender=mt.Address(email=self.sender_email, name=self.sender_name),
            to=admin_emails,
            subject=admin_subject,
            html=admin_html,
            category="Admin Notification"
        )
        
        try:
            # Send customer email
            # logger.info(f"[MAILTRAP] Sending customer email to: {payment_request.email}")
            self.client.send(customer_mail)
            logger.info(f"[MAILTRAP] Customer email sent successfully")
            
            # Send admin email
            # logger.info(f"[MAILTRAP] Sending admin email to: {settings.notification_email_list}")
            self.client.send(admin_mail)
            logger.info(f"[MAILTRAP] Admin email sent successfully")
            
            # logger.info(f"[MAILTRAP] All payment confirmation emails sent for payment {payment_id} (lang: {lang})")
            return True
            
        except Exception as e:
            logger.error(f"[MAILTRAP] Failed to send payment confirmation emails: {e}")
            return False
    

    
    def _render_admin_template(self, success: bool, payment_request: PaymentRequest, amount_display: str, payment_type_display: str, payment_id: str) -> str:
        """Render admin email template (always in Portuguese)"""
        template = Template("""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #333;">{{ 'Novo Pagamento Recebido' if success else 'Falha no Pagamento' }} 💳</h2>
            
            <div style="background: #f8f9fa; border-left: 4px solid {{ '#28a745' if success else '#dc3545' }}; padding: 20px; margin: 20px 0;">
                <h3 style="margin-top: 0; color: #333;">👤 Informações do Cliente:</h3>
                <p><strong>Nome:</strong> {{ name }}</p>
                <p><strong>Email:</strong> {{ email }}</p>
                {% if phone %}<p><strong>Telefone:</strong> {{ phone }}</p>{% endif %}
                <p><strong>Idioma:</strong> {{ language }}</p>
                
                <h3 style="color: #333;">💰 Detalhes do Pagamento:</h3>
                <p><strong>Valor:</strong> {{ amount_display }}</p>
                <p><strong>Moeda:</strong> {{ currency }}</p>
                <p><strong>Tipo:</strong> {{ payment_type_display }}</p>
                <p><strong>ID:</strong> <code>{{ payment_id }}</code></p>
                <p><strong>Status:</strong> <span style="color: {{ '#28a745' if success else '#dc3545' }}; font-weight: bold;">{{ 'SUCESSO ✅' if success else 'FALHA ❌' }}</span></p>
            </div>
            
            <p style="color: #666; font-size: 14px;">Email automático do sistema de pagamentos</p>
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
    
    async def send_email(self, to_emails: List[str], subject: str, html_content: str, category: str = "General"):
        """Generic email sending method using Mailtrap API"""
        try:
            recipients = [mt.Address(email=email) for email in to_emails]
            
            mail = mt.Mail(
                sender=mt.Address(email=self.sender_email, name=self.sender_name),
                to=recipients,
                subject=subject,
                html=html_content,
                category=category
            )
            
            self.client.send(mail)
            logger.info(f"Email sent successfully to: {to_emails}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
