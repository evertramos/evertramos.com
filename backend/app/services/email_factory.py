"""Email service factory - chooses between Mailpit (dev) and Mailtrap (prod)"""

import logging
from app.config import settings
from app.services.email_service import EmailService
from app.services.mailtrap_service import MailtrapService

logger = logging.getLogger(__name__)

def get_email_service():
    """Factory function to return appropriate email service based on environment"""
    if settings.environment == "development":
        logger.info(f"Using EmailService (Mailpit) for environment: {settings.environment}")
        return EmailService()
    else:
        # Validate Mailtrap configuration
        if not settings.mailtrap_api_token:
            logger.error("MAILTRAP_API_TOKEN is required for production environment")
            raise ValueError("Missing Mailtrap configuration for production")
        
        logger.info(f"Using MailtrapService (API) for environment: {settings.environment}")
        return MailtrapService()