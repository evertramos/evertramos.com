from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Literal
from enum import Enum


class Currency(str, Enum):
    BRL = "brl"
    USD = "usd"


class PaymentType(str, Enum):
    ONE_TIME = "one_time"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class PaymentRequest(BaseModel):
    # Customer Information
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, pattern=r'^\+?[\d\s\-\(\)]{10,20}$')
    
    # Payment Information
    amount: int = Field(..., gt=0, description="Amount in cents")
    currency: Currency
    payment_type: PaymentType
    
    # Security
    turnstile_token: str = Field(..., min_length=1, description="Cloudflare Turnstile token")
    
    # Localization
    language: Optional[str] = Field("pt", pattern=r'^(pt|en)$', description="User interface language")
    
    @validator('amount')
    def validate_amount(cls, v, values):
        # Minimum amounts based on Stripe requirements
        currency = values.get('currency')
        if currency == Currency.USD and v < 50:  # $0.50 minimum
            raise ValueError('Minimum amount for USD is $0.50')
        elif currency == Currency.BRL and v < 50:  # R$0.50 minimum
            raise ValueError('Minimum amount for BRL is R$0.50')
        return v
    
    @validator('phone')
    def validate_phone(cls, v):
        if v and len(v.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')) < 10:
            raise ValueError('Phone number must have at least 10 digits')
        return v


class PaymentResponse(BaseModel):
    success: bool
    payment_id: Optional[str] = None
    client_secret: Optional[str] = None
    customer_id: Optional[str] = None
    subscription_id: Optional[str] = None
    message: str
    

class CustomerPortalRequest(BaseModel):
    customer_id: str = Field(..., min_length=1)
    return_url: str = Field(..., pattern=r'^https?://.+')


class CustomerPortalResponse(BaseModel):
    success: bool
    portal_url: Optional[str] = None
    message: str