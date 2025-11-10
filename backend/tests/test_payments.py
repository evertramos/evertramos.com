import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import app
from app.models.payment import PaymentRequest, PaymentType, Currency

client = TestClient(app)


class TestPayments:
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_get_stripe_config(self):
        """Test Stripe configuration endpoint"""
        response = client.get("/api/v1/payments/config")
        assert response.status_code == 200
        data = response.json()
        assert "publishable_key" in data
        assert "supported_currencies" in data
        assert "supported_payment_types" in data
    
    @patch('app.services.stripe_service.StripeService.create_customer')
    @patch('app.services.stripe_service.StripeService.create_payment_intent')
    @patch('app.services.mailtrap_service.MailtrapService.send_payment_confirmation')
    def test_create_one_time_payment_success(self, mock_email, mock_payment, mock_customer):
        """Test successful one-time payment creation"""
        
        # Mock responses
        mock_customer.return_value = {
            "success": True,
            "customer": type('Customer', (), {"id": "cus_test123"})()
        }
        
        mock_payment.return_value = {
            "success": True,
            "payment_intent": type('PaymentIntent', (), {
                "id": "pi_test123",
                "client_secret": "pi_test123_secret"
            })(),
            "client_secret": "pi_test123_secret"
        }
        
        mock_email.return_value = True
        
        # Test data
        payment_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "amount": 1000,  # $10.00
            "currency": "usd",
            "payment_type": "one_time",
            "turnstile_token": "test_token",
            "language": "en"
        }
        
        response = client.post("/api/v1/payments/create", json=payment_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["payment_id"] == "pi_test123"
        assert data["client_secret"] == "pi_test123_secret"
        assert "Payment intent created successfully" in data["message"]
    
    def test_create_payment_invalid_amount(self):
        """Test payment creation with invalid amount"""
        payment_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "amount": 10,  # Too low
            "currency": "usd",
            "payment_type": "one_time",
            "turnstile_token": "test_token",
            "language": "en"
        }
        
        response = client.post("/api/v1/payments/create", json=payment_data)
        assert response.status_code == 422  # Validation error
    
    def test_create_payment_invalid_email(self):
        """Test payment creation with invalid email"""
        payment_data = {
            "name": "John Doe",
            "email": "invalid-email",
            "amount": 1000,
            "currency": "usd",
            "payment_type": "one_time",
            "turnstile_token": "test_token",
            "language": "en"
        }
        
        response = client.post("/api/v1/payments/create", json=payment_data)
        assert response.status_code == 422  # Validation error
    
    @patch('app.services.stripe_service.StripeService.create_customer_portal_session')
    def test_create_customer_portal_success(self, mock_portal):
        """Test successful customer portal creation"""
        
        mock_portal.return_value = {
            "success": True,
            "url": "https://billing.stripe.com/session/test123"
        }
        
        portal_data = {
            "customer_id": "cus_test123",
            "return_url": "https://evertramos.com/success"
        }
        
        response = client.post("/api/v1/payments/customer-portal", json=portal_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["portal_url"] == "https://billing.stripe.com/session/test123"
    
    def test_create_customer_portal_invalid_url(self):
        """Test customer portal creation with invalid return URL"""
        portal_data = {
            "customer_id": "cus_test123",
            "return_url": "invalid-url"
        }
        
        response = client.post("/api/v1/payments/customer-portal", json=portal_data)
        assert response.status_code == 422  # Validation error


class TestPaymentModels:
    
    def test_payment_request_validation(self):
        """Test PaymentRequest model validation"""
        
        # Valid request
        valid_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "amount": 1000,
            "currency": Currency.USD,
            "payment_type": PaymentType.ONE_TIME
        }
        
        request = PaymentRequest(**valid_data)
        assert request.name == "John Doe"
        assert request.amount == 1000
        assert request.currency == Currency.USD
    
    def test_payment_request_minimum_amount_validation(self):
        """Test minimum amount validation"""
        
        with pytest.raises(ValueError, match="Minimum amount"):
            PaymentRequest(
                name="John Doe",
                email="john@example.com",
                amount=10,  # Too low
                currency=Currency.USD,
                payment_type=PaymentType.ONE_TIME
            )
    
    def test_payment_request_phone_validation(self):
        """Test phone number validation"""
        
        with pytest.raises(ValueError, match="Phone number must have"):
            PaymentRequest(
                name="John Doe",
                email="john@example.com",
                phone="123",  # Too short
                amount=1000,
                currency=Currency.USD,
                payment_type=PaymentType.ONE_TIME
            )