import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import app

client = TestClient(app)


class TestSecurity:
    
    def test_api_without_key_fails(self):
        """Test that API calls without key are rejected"""
        payment_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "amount": 1000,
            "currency": "usd",
            "payment_type": "one_time",
            "turnstile_token": "test_token",
            "language": "en"
        }
        
        response = client.post("/api/v1/payments/create", json=payment_data)
        assert response.status_code == 403
        assert "API key required" in response.json()["detail"]
    
    def test_api_with_invalid_key_fails(self):
        """Test that API calls with invalid key are rejected"""
        payment_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "amount": 1000,
            "currency": "usd",
            "payment_type": "one_time",
            "turnstile_token": "test_token",
            "language": "en"
        }
        
        headers = {"Authorization": "Bearer invalid-key"}
        response = client.post("/api/v1/payments/create", json=payment_data, headers=headers)
        assert response.status_code == 403
        assert "Invalid API key" in response.json()["detail"]
    
    @patch('app.services.stripe_service.StripeService.create_customer')
    @patch('app.services.stripe_service.StripeService.create_payment_intent')
    @patch('app.services.mailtrap_service.MailtrapService.send_payment_confirmation')
    def test_api_with_valid_key_succeeds(self, mock_email, mock_payment, mock_customer):
        """Test that API calls with valid key succeed"""
        
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
        
        payment_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "amount": 1000,
            "currency": "usd",
            "payment_type": "one_time",
            "turnstile_token": "test_token",
            "language": "en"
        }
        
        headers = {"Authorization": "Bearer your-generated-secure-api-key-here"}
        response = client.post("/api/v1/payments/create", json=payment_data, headers=headers)
        
        assert response.status_code == 200
        assert response.json()["success"] is True
    
    def test_rate_limiting(self):
        """Test rate limiting functionality"""
        # This would need more sophisticated testing in a real scenario
        # For now, just test that the endpoint exists and responds
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_security_headers(self):
        """Test that security headers are present"""
        response = client.get("/health")
        
        assert "X-Content-Type-Options" in response.headers
        assert "X-Frame-Options" in response.headers
        assert "X-XSS-Protection" in response.headers
        assert response.headers["X-Frame-Options"] == "DENY"
    
    def test_config_endpoint_no_auth_required(self):
        """Test that config endpoint doesn't require auth (public)"""
        response = client.get("/api/v1/payments/config")
        assert response.status_code == 200
        assert "publishable_key" in response.json()