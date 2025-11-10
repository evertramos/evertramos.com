from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import time
from typing import Dict, Optional
import logging
from urllib.parse import urlparse

from app.config import settings
from app.utils.logging import log_security_event

logger = logging.getLogger(__name__)

# In-memory rate limiting (use Redis in production)
rate_limit_storage: Dict[str, Dict[str, int]] = {}

class APIKeyAuth(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(APIKeyAuth, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        # Validate origin first
        if not self.validate_origin(request):
            client_ip = get_client_ip(request)
            origin = request.headers.get('origin', 'none').replace('\n', '').replace('\r', '')[:100]
            log_security_event("INVALID_ORIGIN", client_ip, f"Origin: {origin}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid origin"
            )
        
        credentials: HTTPAuthorizationCredentials = await super(APIKeyAuth, self).__call__(request)
        
        if credentials:
            if not self.verify_api_key(credentials.credentials, request):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid API key"
                )
            return credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="API key required"
            )

    def validate_origin(self, request: Request) -> bool:
        """Validate request origin against allowed domains"""
        origin = request.headers.get("origin")
        referer = request.headers.get("referer")
        
        # Allow requests without origin/referer for direct API calls (development)
        if not origin and not referer:
            return settings.environment == "development"
        
        # Check origin header
        if origin:
            parsed = urlparse(origin)
            return parsed.hostname in settings.allowed_hosts_list
        
        # Check referer as fallback
        if referer:
            parsed = urlparse(referer)
            return parsed.hostname in settings.allowed_hosts_list
        
        return False
    
    def verify_api_key(self, api_key: str, request: Request) -> bool:
        """Verify API key"""
        is_valid = api_key == settings.api_key
        if not is_valid:
            client_ip = get_client_ip(request)
            sanitized_key = api_key[:10].replace('\n', '').replace('\r', '')
            log_security_event("INVALID_API_KEY", client_ip, f"Key: {sanitized_key}...")
        return is_valid


def get_client_ip(request: Request) -> str:
    """Get client IP address"""
    # Check for forwarded headers (behind proxy)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    return request.client.host if request.client else "unknown"


def check_rate_limit(request: Request) -> bool:
    """Check if request is within rate limit"""
    client_ip = get_client_ip(request)
    current_time = int(time.time())
    window_start = current_time - settings.rate_limit_window
    
    # Clean old entries
    if client_ip in rate_limit_storage:
        rate_limit_storage[client_ip] = {
            timestamp: count for timestamp, count in rate_limit_storage[client_ip].items()
            if int(timestamp) > window_start
        }
    else:
        rate_limit_storage[client_ip] = {}
    
    # Count requests in current window
    total_requests = sum(rate_limit_storage[client_ip].values())
    
    if total_requests >= settings.rate_limit_requests:
        sanitized_ip = client_ip.replace('\n', '').replace('\r', '')
        logger.warning(f"Rate limit exceeded for IP: {sanitized_ip}")
        log_security_event("RATE_LIMIT_EXCEEDED", client_ip, f"Requests: {total_requests}")
        return False
    
    # Add current request
    current_minute = str(current_time // 60)  # Group by minute
    rate_limit_storage[client_ip][current_minute] = rate_limit_storage[client_ip].get(current_minute, 0) + 1
    
    return True


async def rate_limit_middleware(request: Request, call_next):
    """Rate limiting middleware"""
    # Skip rate limiting for health check
    if request.url.path == "/health":
        return await call_next(request)
    
    if not check_rate_limit(request):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Try again later."
        )
    
    return await call_next(request)


async def security_headers_middleware(request: Request, call_next):
    """Add security headers"""
    response = await call_next(request)
    
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    
    return response