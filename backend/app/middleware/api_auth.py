"""
Secure API Authentication Middleware
- API key never exposed to frontend
- Server-side validation only
- Multiple layers of security
"""

from fastapi import HTTPException, Request, status
from typing import Optional
import logging
import hashlib
import hmac
import time
from urllib.parse import urlparse

from app.config import settings
from app.utils.logging import log_security_event

logger = logging.getLogger(__name__)


class SecureAPIAuth:
    """Secure API authentication without exposing keys to frontend"""
    
    def __init__(self):
        self.api_key = settings.api_key
    
    async def validate_request(self, request: Request) -> bool:
        """
        Multi-layer validation:
        1. Origin validation (primary)
        2. Rate limiting (via middleware)
        3. Turnstile (via endpoint)
        4. Request signature (optional future enhancement)
        """
        
        # 1. Validate Origin Header
        if not self._validate_origin(request):
            client_ip = self._get_client_ip(request)
            log_security_event("INVALID_ORIGIN", client_ip, 
                             f"Origin: {request.headers.get('origin', 'none')}")
            return False
        
        # 2. Validate Referer as fallback
        if not self._validate_referer(request):
            client_ip = self._get_client_ip(request)
            log_security_event("INVALID_REFERER", client_ip,
                             f"Referer: {request.headers.get('referer', 'none')}")
            return False
        
        # 3. Check for suspicious patterns
        if self._is_suspicious_request(request):
            client_ip = self._get_client_ip(request)
            log_security_event("SUSPICIOUS_REQUEST", client_ip, "Pattern detected")
            return False
        
        return True
    
    def _validate_origin(self, request: Request) -> bool:
        """Validate request origin against allowed hosts"""
        origin = request.headers.get("origin")
        
        # Allow requests without origin in development
        if not origin and settings.environment == "development":
            return True
        
        if not origin:
            return False
        
        try:
            parsed = urlparse(origin)
            return parsed.hostname in settings.allowed_hosts_list
        except Exception:
            return False
    
    def _validate_referer(self, request: Request) -> bool:
        """Validate referer header as additional check"""
        referer = request.headers.get("referer")
        
        # If no referer, rely on origin validation
        if not referer:
            return True
        
        try:
            parsed = urlparse(referer)
            return parsed.hostname in settings.allowed_hosts_list
        except Exception:
            return False
    
    def _is_suspicious_request(self, request: Request) -> bool:
        """Detect suspicious request patterns"""
        user_agent = request.headers.get("user-agent", "")
        
        # Block obvious bots/scrapers
        suspicious_agents = [
            "curl", "wget", "python-requests", "postman", 
            "insomnia", "bot", "crawler", "spider"
        ]
        
        return any(agent in user_agent.lower() for agent in suspicious_agents)
    
    def _get_client_ip(self, request: Request) -> str:
        """Get real client IP"""
        # Check for forwarded headers (behind proxy)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        return request.client.host if request.client else "unknown"


# Future enhancement: Request signing
class RequestSigner:
    """Optional: Sign requests with HMAC for extra security"""
    
    @staticmethod
    def generate_signature(payload: str, secret: str, timestamp: str) -> str:
        """Generate HMAC signature for request"""
        message = f"{timestamp}.{payload}"
        signature = hmac.new(
            secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    @staticmethod
    def verify_signature(payload: str, signature: str, secret: str, timestamp: str) -> bool:
        """Verify request signature"""
        expected = RequestSigner.generate_signature(payload, secret, timestamp)
        return hmac.compare_digest(signature, expected)