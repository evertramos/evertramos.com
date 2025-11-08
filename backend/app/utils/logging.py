import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path
from app.config import settings


def setup_logging():
    """Configure logging for both console and file output"""
    
    # Create logs directory if it doesn't exist
    log_dir = Path("/tmp/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Console handler (for Docker logs)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler for all logs (rotating)
    if settings.environment == "production":
        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / "ezyba.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(file_handler)
        
        # Error file handler (errors only)
        error_handler = logging.handlers.RotatingFileHandler(
            log_dir / "ezyba_errors.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(error_handler)
        
        # Security events handler
        security_handler = logging.handlers.RotatingFileHandler(
            log_dir / "ezyba_security.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=10
        )
        security_handler.setLevel(logging.WARNING)
        security_handler.setFormatter(detailed_formatter)
        
        # Create security logger
        security_logger = logging.getLogger("security")
        security_logger.addHandler(security_handler)
        security_logger.setLevel(logging.WARNING)
        security_logger.propagate = False


def log_request(request_id: str, method: str, path: str, ip: str, user_agent: str = None):
    """Log incoming requests"""
    logger = logging.getLogger("ezyba.requests")
    logger.info(f"Request {request_id}: {method} {path} from {ip} - {user_agent}")


def log_payment_attempt(request_id: str, email: str, amount: int, currency: str, success: bool):
    """Log payment attempts"""
    logger = logging.getLogger("ezyba.payments")
    status = "SUCCESS" if success else "FAILED"
    logger.info(f"Payment {request_id}: {status} - {email} - {amount/100:.2f} {currency.upper()}")


def log_security_event(event_type: str, ip: str, details: str):
    """Log security events"""
    security_logger = logging.getLogger("security")
    security_logger.warning(f"SECURITY: {event_type} from {ip} - {details}")


def log_error(request_id: str, error: Exception, context: str = None):
    """Log errors with context"""
    logger = logging.getLogger("ezyba.errors")
    context_str = f" - Context: {context}" if context else ""
    logger.error(f"Error {request_id}: {type(error).__name__}: {str(error)}{context_str}", exc_info=True)