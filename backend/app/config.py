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
    smtp_host: str
    smtp_port: int = 587
    smtp_user: str
    smtp_password: str
    
    # Application Configuration
    environment: str  # Required - development/production
    api_title: str = "Ezyba Payment API"
    api_version: str = "1.0.0"
    
    # Security
    cors_origins: str  # Required - comma-separated origins
    allowed_hosts: str  # Required - comma-separated hosts
    
    # API Security
    api_key: str  # Required - generate with scripts/generate-api-key.py
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