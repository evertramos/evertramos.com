# Development Guidelines - Ezyba

## Code Quality Standards

### Type Safety (100% Coverage)
- **ALWAYS** use type hints on all function parameters and return types
- **ALWAYS** use Pydantic models for data validation and serialization
- **ALWAYS** use Enum classes for constants (Currency, PaymentType)
- **ALWAYS** use Optional[] for nullable fields
- **ALWAYS** use Literal types for restricted string values

### Input Validation Patterns
- **ALWAYS** use Pydantic Field() with constraints (min_length, max_length, gt, pattern)
- **ALWAYS** implement custom validators with @validator decorator
- **ALWAYS** validate email formats with EmailStr type
- **ALWAYS** sanitize user inputs (email subjects, phone numbers)
- **ALWAYS** use regex patterns for phone and URL validation

### Error Handling Standards
- **ALWAYS** use structured logging with request IDs (uuid4()[:8])
- **ALWAYS** catch specific exceptions before generic Exception
- **ALWAYS** re-raise HTTPException for API errors
- **ALWAYS** log errors with context using log_error() utility
- **ALWAYS** return user-friendly error messages, never expose internals

## Security Implementation Patterns

### Authentication & Authorization
- **ALWAYS** use HTTPBearer for API key authentication
- **ALWAYS** implement custom __call__ method for auth classes
- **ALWAYS** verify credentials in middleware before processing
- **ALWAYS** log security events (invalid keys, rate limits)
- **ALWAYS** use environment variables for sensitive configuration

### Rate Limiting Implementation
- **ALWAYS** implement per-IP rate limiting with time windows
- **ALWAYS** clean expired entries from rate limit storage
- **ALWAYS** skip rate limiting for health check endpoints
- **ALWAYS** return 429 status for rate limit violations
- **ALWAYS** log rate limit violations with IP addresses

### Security Headers Pattern
```python
response.headers["X-Content-Type-Options"] = "nosniff"
response.headers["X-Frame-Options"] = "DENY"
response.headers["X-XSS-Protection"] = "1; mode=block"
response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
```

## Service Layer Architecture

### Dependency Injection Pattern
- **ALWAYS** use FastAPI Depends() for service injection
- **ALWAYS** create factory functions (get_stripe_service, get_email_service)
- **ALWAYS** inject services into route handlers, not instantiate directly
- **ALWAYS** use constructor injection for service dependencies

### Service Class Structure
- **ALWAYS** initialize service configuration in __init__
- **ALWAYS** use private methods (_validate_email, _sanitize_subject) for internal logic
- **ALWAYS** return structured dictionaries with "success" and "error" keys
- **ALWAYS** implement async methods for I/O operations
- **ALWAYS** validate inputs at service layer before external API calls

### Email Service Patterns
- **ALWAYS** validate email addresses before sending
- **ALWAYS** sanitize email subjects to prevent header injection
- **ALWAYS** use Jinja2 templates for HTML email content
- **ALWAYS** send both customer and admin notifications
- **ALWAYS** handle SMTP configuration differences (dev vs prod)

## API Design Standards

### Route Handler Structure
```python
@router.post("/endpoint", response_model=ResponseModel)
async def handler_name(
    request_model: RequestModel,
    credentials: HTTPAuthorizationCredentials = Depends(api_key_auth),
    service: ServiceClass = Depends(get_service)
) -> ResponseModel:
```

### Request Processing Pattern
1. **Generate request ID** for tracking
2. **Log request start** with user identifier
3. **Process business logic** through service layer
4. **Send notifications** (email, webhooks)
5. **Log success/failure** with request ID
6. **Return structured response**

### Error Response Pattern
- **ALWAYS** catch HTTPException and re-raise
- **ALWAYS** catch generic Exception and log with request ID
- **ALWAYS** send failure notifications when appropriate
- **ALWAYS** return 500 status for unexpected errors
- **ALWAYS** use generic error messages for security

## Configuration Management

### Settings Pattern
- **ALWAYS** use Pydantic BaseSettings for configuration
- **ALWAYS** load from environment variables
- **ALWAYS** provide sensible defaults for development
- **ALWAYS** validate configuration on startup
- **ALWAYS** separate development and production configs

### Environment Variable Naming
- **ALWAYS** use UPPER_CASE for environment variables
- **ALWAYS** prefix with service name (STRIPE_, SMTP_)
- **ALWAYS** use descriptive names (NOTIFICATION_EMAILS vs EMAILS)
- **ALWAYS** document required vs optional variables

## Logging Standards

### Structured Logging Pattern
```python
logger.info(f"[{request_id}] Processing payment request for {email}")
log_payment_attempt(request_id, email, amount, currency, success)
log_error(request_id, exception, context_description)
log_security_event(event_type, client_ip, details)
```

### Log Message Format
- **ALWAYS** include request ID in brackets [req_id]
- **ALWAYS** include user identifier (email, IP)
- **ALWAYS** log both start and completion of operations
- **ALWAYS** use appropriate log levels (INFO, WARNING, ERROR)
- **ALWAYS** include relevant context in error logs

## Testing Patterns

### Test Structure (Inferred from imports)
- **ALWAYS** use pytest for test framework
- **ALWAYS** use pytest-asyncio for async test support
- **ALWAYS** use httpx for HTTP client testing
- **ALWAYS** organize tests by module (models/, routers/, services/)
- **ALWAYS** mock external services (Stripe, SMTP)

## FastAPI Application Patterns

### Application Lifecycle
- **ALWAYS** use @asynccontextmanager for lifespan events
- **ALWAYS** configure external services on startup
- **ALWAYS** log application start/stop events
- **ALWAYS** set up global exception handlers

### Middleware Order (Critical)
1. **TrustedHostMiddleware** - Host validation
2. **CORSMiddleware** - Cross-origin requests
3. **rate_limit_middleware** - Rate limiting
4. **security_headers_middleware** - Security headers

### Router Organization
- **ALWAYS** use APIRouter with prefix and tags
- **ALWAYS** group related endpoints in same router
- **ALWAYS** include routers with versioned prefix (/api/v1)
- **ALWAYS** implement health check endpoint

## Data Model Patterns

### Pydantic Model Structure
- **ALWAYS** inherit from BaseModel
- **ALWAYS** use Field() for validation constraints
- **ALWAYS** implement custom validators for complex logic
- **ALWAYS** use descriptive field names and docstrings
- **ALWAYS** group related fields with comments

### Validation Patterns
- **ALWAYS** validate minimum values for financial amounts
- **ALWAYS** check currency-specific requirements
- **ALWAYS** validate phone number formats and lengths
- **ALWAYS** use regex patterns for format validation
- **ALWAYS** provide clear error messages in validators

## Common Code Idioms

### Request ID Generation
```python
request_id = str(uuid.uuid4())[:8]
```

### Service Result Pattern
```python
result = await service.method()
if result["success"]:
    # Handle success
else:
    raise HTTPException(status_code=400, detail=result["error"])
```

### Email Template Pattern
```python
template = Template("""HTML template with {{ variables }}""")
html_content = template.render(variable=value)
```

### Rate Limiting Cleanup
```python
rate_limit_storage[client_ip] = {
    timestamp: count for timestamp, count in rate_limit_storage[client_ip].items()
    if int(timestamp) > window_start
}
```

## Frequently Used Annotations

### FastAPI Decorators
- `@router.post("/path", response_model=Model)` - API endpoints
- `@validator('field')` - Pydantic field validation
- `@asynccontextmanager` - Application lifespan management

### Type Annotations
- `Optional[str]` - Nullable string fields
- `List[str]` - String arrays
- `Dict[str, Any]` - Generic dictionaries
- `HTTPAuthorizationCredentials` - API authentication
- `Depends(factory_function)` - Dependency injection

### Common Imports Pattern
```python
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
import logging
import uuid
```