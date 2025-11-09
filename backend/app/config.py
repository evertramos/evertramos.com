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
    environment: str = "development"
    api_title: str = "Ezyba Payment API"
    api_version: str = "1.0.0"
    
    # Security
    cors_origins: List[str] = [
        "https://evertramos.com",
        "https://evertramos.com.br",
        "http://localhost:3000"
    ]
    
    # API Security
    api_key: str = "ezyba-secure-api-key-2024"
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600  # 1 hour
    
    @property
    def notification_email_list(self) -> List[str]:
        return [email.strip() for email in self.notification_emails.split(",")]
    
    class Config:
        env_file = ".env"


settings = Settings()