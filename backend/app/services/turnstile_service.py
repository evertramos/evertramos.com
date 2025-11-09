import httpx
import logging
from typing import Dict, Any
from app.config import settings

logger = logging.getLogger(__name__)


class TurnstileService:
    """Service for validating Cloudflare Turnstile tokens"""
    
    VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
    
    def __init__(self):
        self.secret_key = getattr(settings, 'turnstile_secret_key', None)
        logger.info(f"Turnstile secret key loaded: {self.secret_key[:10]}..." if self.secret_key else "No secret key")
        if not self.secret_key:
            logger.warning("Turnstile secret key not configured")
    
    async def verify_token(self, token: str, remote_ip: str = None) -> Dict[str, Any]:
        """
        Verify Turnstile token with Cloudflare
        
        Args:
            token: Turnstile token from frontend
            remote_ip: Client IP address (optional)
            
        Returns:
            Dict with success status and details
        """
        if not self.secret_key:
            logger.error("Turnstile verification failed: secret key not configured")
            return {
                "success": False,
                "error": "Turnstile not configured"
            }
        
        # Development bypass for test keys
        logger.info(f"Checking bypass: secret_key={self.secret_key}")
        if self.secret_key in ['1x0000000000000000000000000000000AA', '0x4AAAAAAABkMYinukE_NVJt']:
            logger.info("Turnstile verification bypassed for development")
            return {
                "success": True,
                "challenge_ts": "2024-01-01T00:00:00.000Z",
                "hostname": "localhost"
            }
        
        if not token or token.strip() == "":
            return {
                "success": False,
                "error": "Missing turnstile token"
            }
        
        try:
            data = {
                "secret": self.secret_key,
                "response": token
            }
            
            if remote_ip:
                data["remoteip"] = remote_ip
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.VERIFY_URL,
                    data=data,
                    timeout=10.0
                )
                
                if response.status_code != 200:
                    logger.error(f"Turnstile API error: {response.status_code}")
                    return {
                        "success": False,
                        "error": "Turnstile verification failed"
                    }
                
                result = response.json()
                
                if result.get("success", False):
                    logger.info("Turnstile verification successful")
                    return {
                        "success": True,
                        "challenge_ts": result.get("challenge_ts"),
                        "hostname": result.get("hostname")
                    }
                else:
                    error_codes = result.get("error-codes", [])
                    logger.warning(f"Turnstile verification failed: {error_codes}")
                    return {
                        "success": False,
                        "error": "Invalid turnstile token",
                        "error_codes": error_codes
                    }
                    
        except httpx.TimeoutException:
            logger.error("Turnstile verification timeout")
            return {
                "success": False,
                "error": "Turnstile verification timeout"
            }
        except Exception as e:
            logger.error(f"Turnstile verification error: {e}")
            return {
                "success": False,
                "error": "Turnstile verification failed"
            }