import stripe
import logging
from typing import Dict, Any, Optional
from app.models.payment import PaymentRequest, PaymentType, Currency
from app.config import settings

logger = logging.getLogger(__name__)


class StripeService:
    def __init__(self):
        stripe.api_key = settings.stripe_secret_key
    
    async def create_customer(self, name: str, email: str, phone: Optional[str] = None) -> Dict[str, Any]:
        """Create or retrieve Stripe customer"""
        try:
            # Check if customer already exists
            customers = stripe.Customer.list(email=email, limit=1)
            
            if customers.data:
                customer = customers.data[0]
                logger.info(f"Retrieved existing customer: {customer.id}")
            else:
                # Create new customer
                customer_data = {
                    "name": name,
                    "email": email,
                }
                if phone:
                    customer_data["phone"] = phone
                
                customer = stripe.Customer.create(**customer_data)
                logger.info(f"Created new customer: {customer.id}")
            
            return {"success": True, "customer": customer}
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe customer error: {e}")
            return {"success": False, "error": str(e)}
    
    async def create_payment_intent(self, payment_request: PaymentRequest, customer_id: str) -> Dict[str, Any]:
        """Create one-time payment intent"""
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=payment_request.amount,
                currency=payment_request.currency.value,
                customer=customer_id,
                automatic_payment_methods={"enabled": True},
                metadata={
                    "customer_name": payment_request.name,
                    "customer_email": payment_request.email,
                    "payment_type": payment_request.payment_type.value
                }
            )
            
            logger.info(f"Created payment intent: {payment_intent.id}")
            return {
                "success": True,
                "payment_intent": payment_intent,
                "client_secret": payment_intent.client_secret
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Payment intent error: {e}")
            return {"success": False, "error": str(e)}
    
    async def create_subscription(self, payment_request: PaymentRequest, customer_id: str) -> Dict[str, Any]:
        """Create recurring subscription"""
        try:
            # Create price for the subscription
            interval = "month" if payment_request.payment_type == PaymentType.MONTHLY else "year"
            
            price = stripe.Price.create(
                unit_amount=payment_request.amount,
                currency=payment_request.currency.value,
                recurring={"interval": interval},
                product_data={
                    "name": f"Ezyba Service - {payment_request.name}",
                }
            )
            
            # Create subscription
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{"price": price.id}],
                payment_behavior="default_incomplete",
                payment_settings={"save_default_payment_method": "on_subscription"},
                expand=["latest_invoice.payment_intent"],
                metadata={
                    "customer_name": payment_request.name,
                    "customer_email": payment_request.email,
                    "payment_type": payment_request.payment_type.value
                }
            )
            
            logger.info(f"Created subscription: {subscription.id}")
            return {
                "success": True,
                "subscription": subscription,
                "client_secret": subscription.latest_invoice.payment_intent.client_secret
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Subscription error: {e}")
            return {"success": False, "error": str(e)}
    
    async def create_customer_portal_session(self, customer_id: str, return_url: str) -> Dict[str, Any]:
        """Create customer portal session for subscription management"""
        try:
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url,
            )
            
            logger.info(f"Created portal session for customer: {customer_id}")
            return {"success": True, "url": session.url}
            
        except stripe.error.StripeError as e:
            logger.error(f"Portal session error: {e}")
            return {"success": False, "error": str(e)}