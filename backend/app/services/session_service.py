"""
Session-based API Key Service
- Generates temporary API keys for frontend
- Keys expire after short time
- Tied to specific sessions/IPs
"""

import secrets
import time
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class SessionAPIService:
    """Manages temporary API keys for frontend sessions"""
    
    def __init__(self):
        # In-memory storage (use Redis in production)
        self.active_sessions: Dict[str, Dict] = {}
        self.cleanup_interval = 300  # 5 minutes
        self.last_cleanup = time.time()
    
    def generate_session_key(self, client_ip: str, user_agent: str) -> str:
        """Generate temporary API key for a session"""
        
        # Cleanup old sessions periodically
        self._cleanup_expired_sessions()
        
        # Generate secure session key
        session_key = f"sess_{secrets.token_urlsafe(32)}"
        
        # Store session info
        self.active_sessions[session_key] = {
            "created_at": time.time(),
            "expires_at": time.time() + 1800,  # 30 minutes
            "client_ip": client_ip,
            "user_agent": user_agent,
            "requests_count": 0,
            "max_requests": 50  # Rate limit per session
        }
        
        logger.info(f"Generated session key for IP: {client_ip}")
        return session_key
    
    def validate_session_key(self, session_key: str, client_ip: str, user_agent: str) -> bool:
        """Validate session key and context"""
        
        if not session_key or session_key not in self.active_sessions:
            return False
        
        session = self.active_sessions[session_key]
        
        # Check expiration
        if time.time() > session["expires_at"]:
            del self.active_sessions[session_key]
            return False
        
        # Check IP consistency
        if session["client_ip"] != client_ip:
            logger.warning(f"IP mismatch for session {session_key}: {session['client_ip']} vs {client_ip}")
            return False
        
        # Check rate limit
        if session["requests_count"] >= session["max_requests"]:
            logger.warning(f"Rate limit exceeded for session {session_key}")
            return False
        
        # Update usage
        session["requests_count"] += 1
        
        return True
    
    def _cleanup_expired_sessions(self):
        """Remove expired sessions"""
        current_time = time.time()
        
        # Only cleanup every 5 minutes
        if current_time - self.last_cleanup < self.cleanup_interval:
            return
        
        expired_keys = [
            key for key, session in self.active_sessions.items()
            if current_time > session["expires_at"]
        ]
        
        for key in expired_keys:
            del self.active_sessions[key]
        
        self.last_cleanup = current_time
        
        if expired_keys:
            logger.info(f"Cleaned up {len(expired_keys)} expired sessions")


# Global instance
session_service = SessionAPIService()