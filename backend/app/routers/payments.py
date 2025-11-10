from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials
import logging
from typing import Dict, Any

from app.models.payment import (
    PaymentRequest, 
    PaymentResponse, 
    CustomerPortalRequest, 
    CustomerPortalResponse,
    PaymentType
)
from app.services.stripe_service import StripeService
from app.services.email_factory import get_email_service
from app.services.turnstile_service import TurnstileService
from app.utils.logging import log_payment_attempt, log_error
from app.middleware.api_auth import SecureAPIAuth
import uuid

router = APIRouter(prefix="/payments", tags=["payments"])
api_auth = SecureAPIAuth()
logger = logging.getLogger(__name__)


def get_stripe_service() -> StripeService:
    return StripeService()


def get_email_service_instance():
    return get_email_service()


def get_turnstile_service() -> TurnstileService:
    return TurnstileService()


@router.post("/create", response_model=PaymentResponse)
async def create_payment(
    payment_request: PaymentRequest,
    request: Request,
    stripe_service: StripeService = Depends(get_stripe_service),
    email_service = Depends(get_email_service_instance),
    turnstile_service: TurnstileService = Depends(get_turnstile_service)
) -> PaymentResponse:
    """Create a payment (one-time or subscription)"""
    
    request_id = str(uuid.uuid4())[:8]
    
    try:
        # Validate session key from frontend
        session_key = request.headers.get("X-Session-Key")
        if not session_key:
            raise HTTPException(status_code=401, detail="Session key required")
        
        from app.services.session_service import session_service
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "")
        
        if not session_service.validate_session_key(session_key, client_ip, user_agent):
            raise HTTPException(status_code=401, detail="Invalid or expired session")
        
        sanitized_email = payment_request.email.replace('\n', '').replace('\r', '')[:50]
        logger.info(f"[{request_id}] Processing payment request for {sanitized_email}")
        
        # Verify Turnstile token first
        client_ip = request.client.host if request.client else None
        turnstile_result = await turnstile_service.verify_token(
            payment_request.turnstile_token, 
            client_ip
        )
        
        if not turnstile_result["success"]:
            logger.warning(f"[{request_id}] Turnstile verification failed: {turnstile_result.get('error')}")
            raise HTTPException(status_code=400, detail="Security verification failed")
        
        logger.info(f"[{request_id}] Turnstile verification successful")
        log_payment_attempt(request_id, payment_request.email, payment_request.amount, payment_request.currency.value, False)
        
        # Create or get customer
        customer_result = await stripe_service.create_customer(
            name=payment_request.name,
            email=payment_request.email,
            phone=payment_request.phone
        )
        
        if not customer_result["success"]:
            raise HTTPException(status_code=400, detail=customer_result["error"])
        
        customer = customer_result["customer"]
        
        # Create payment based on type
        if payment_request.payment_type == PaymentType.ONE_TIME:
            payment_result = await stripe_service.create_payment_intent(
                payment_request, customer.id
            )
            
            if payment_result["success"]:
                # Send confirmation emails
                await email_service.send_payment_confirmation(
                    payment_request, 
                    payment_result["payment_intent"].id, 
                    True
                )
                
                log_payment_attempt(request_id, payment_request.email, payment_request.amount, payment_request.currency.value, True)
                logger.info(f"[{request_id}] Payment successful: {payment_result['payment_intent'].id}")
                
                return PaymentResponse(
                    success=True,
                    payment_id=payment_result["payment_intent"].id,
                    client_secret=payment_result["client_secret"],
                    customer_id=customer.id,
                    message="Payment intent created successfully"
                )
        
        else:  # Monthly or Yearly subscription
            subscription_result = await stripe_service.create_subscription(
                payment_request, customer.id
            )
            
            if subscription_result["success"]:
                # Send confirmation emails
                await email_service.send_payment_confirmation(
                    payment_request, 
                    subscription_result["subscription"].id, 
                    True
                )
                
                return PaymentResponse(
                    success=True,
                    payment_id=subscription_result["subscription"].id,
                    client_secret=subscription_result["client_secret"],
                    customer_id=customer.id,
                    subscription_id=subscription_result["subscription"].id,
                    message="Subscription created successfully"
                )
        
        # If we get here, something went wrong
        error_msg = payment_result.get("error") if payment_request.payment_type == PaymentType.ONE_TIME else subscription_result.get("error")
        
        # Send failure email
        await email_service.send_payment_confirmation(
            payment_request, 
            "N/A", 
            False
        )
        
        raise HTTPException(status_code=400, detail=error_msg)
        
    except HTTPException:
        raise
    except Exception as e:
        sanitized_email = payment_request.email.replace('\n', '').replace('\r', '')[:50]
        log_error(request_id, e, f"Payment creation for {sanitized_email}")
        logger.error(f"[{request_id}] Unexpected error in create_payment: {e}")
        
        # Send failure email
        try:
            await email_service.send_payment_confirmation(payment_request, "N/A", False)
        except Exception as email_error:
            log_error(request_id, email_error, "Failed to send failure notification email")
        
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/customer-portal", response_model=CustomerPortalResponse)
async def create_customer_portal(
    portal_request: CustomerPortalRequest,
    request: Request,
    stripe_service: StripeService = Depends(get_stripe_service)
) -> CustomerPortalResponse:
    """Create customer portal session for subscription management"""
    
    try:
        # Validate session key from frontend
        session_key = request.headers.get("X-Session-Key")
        if not session_key:
            raise HTTPException(status_code=401, detail="Session key required")
        
        from app.services.session_service import session_service
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "")
        
        if not session_service.validate_session_key(session_key, client_ip, user_agent):
            raise HTTPException(status_code=401, detail="Invalid or expired session")
        
        logger.info(f"Creating portal session for customer: {portal_request.customer_id}")
        
        portal_result = await stripe_service.create_customer_portal_session(
            portal_request.customer_id,
            portal_request.return_url
        )
        
        if portal_result["success"]:
            return CustomerPortalResponse(
                success=True,
                portal_url=portal_result["url"],
                message="Portal session created successfully"
            )
        else:
            raise HTTPException(status_code=400, detail=portal_result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in create_customer_portal: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/config")
async def get_stripe_config(request: Request) -> Dict[str, Any]:
    """Get Stripe publishable key and session token for frontend"""
    from app.config import settings
    from app.services.session_service import session_service
    
    # Validate origin first
    if not await api_auth.validate_request(request):
        raise HTTPException(status_code=403, detail="Unauthorized request")
    
    # Generate session key for this client
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "")
    session_key = session_service.generate_session_key(client_ip, user_agent)
    
    return {
        "publishable_key": settings.stripe_publishable_key,
        "session_key": session_key,
        "supported_currencies": ["brl", "usd"],
        "supported_payment_types": ["one_time", "monthly", "yearly"]
    }