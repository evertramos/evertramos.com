from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Stripe Configuration
    stripe_publishable_key: str
    stripe_secret_key: str
    
    # Turnstile Configuration
    turnstile_secret_key: str
    
    # Email Configuration
    notification_emails: str  # Comma-separated emails
    
    # Mailtrap Configuration (Production)
    mailtrap_api_token: Optional[str] = None
    sender_email: Optional[str] = None
    sender_name: Optional[str] = None
    
    # SMTP Configuration (Development - Mailpit)
    smtp_host: Optional[str] = None
    smtp_port: int = 1025
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    
    # Email Display Configuration
    company_name: str
    support_email: str
    usd_symbol: str = "$"
    brl_symbol: str = "R$"
    
    # Application Configuration
    environment: str  # Required - development/production
    api_title: str = "Ezyba Payment API"
    api_version: str = "1.0.0"
    
    # Security
    cors_origins: str  # Required - comma-separated origins
    allowed_hosts: str  # Required - comma-separated hosts
    
    # Internal API Security (Never expose to frontend)
    api_key: str  # Server-side only - for internal auth
    
    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600  # 1 hour
    
    @property
    def notification_email_list(self) -> List[str]:
        return [email.strip() for email in self.notification_emails.split(",")]
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    @property
    def allowed_hosts_list(self) -> List[str]:
        return [host.strip() for host in self.allowed_hosts.split(",")]
    
    class Config:
        env_file = ".env"


settings = Settings()