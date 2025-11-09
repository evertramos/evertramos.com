# Development Guidelines and Patterns

## Code Quality Standards

### Python Backend Standards
- **Type Hints**: MANDATORY on all functions, parameters, and return values
- **Async/Await**: Use async functions for all I/O operations (database, API calls, email)
- **Pydantic Models**: All data validation through Pydantic with custom validators
- **Logging**: Structured logging with request IDs for traceability
- **Error Handling**: Try-catch blocks with specific exception types and proper logging

### TypeScript Frontend Standards
- **Type Safety**: Explicit types for all variables, functions, and interfaces
- **Export Patterns**: Named exports for utilities, default exports for components
- **Const Assertions**: Use `as const` for immutable data structures
- **Function Types**: Arrow functions for utilities, regular functions for components

## Structural Conventions

### File Organization Pattern
```
app/
├── models/          # Pydantic models with validation
├── routers/         # FastAPI route handlers
├── services/        # Business logic classes
├── middleware/      # Security and request processing
└── utils/           # Pure utility functions
```

### Import Organization (Python)
1. Standard library imports
2. Third-party imports (FastAPI, Pydantic, etc.)
3. Local app imports (models, services, utils)
4. Blank lines between groups

### Import Organization (TypeScript)
1. External libraries
2. Internal utilities and types
3. Component imports
4. Relative imports last

## Naming Conventions

### Python Naming
- **Functions**: `snake_case` with descriptive verbs (`create_payment`, `send_email`)
- **Classes**: `PascalCase` with descriptive nouns (`EmailService`, `PaymentRequest`)
- **Constants**: `UPPER_SNAKE_CASE` (`STRIPE_SECRET_KEY`, `DEFAULT_CURRENCY`)
- **Variables**: `snake_case` with meaningful names (`request_id`, `customer_result`)

### TypeScript Naming
- **Functions**: `camelCase` with descriptive verbs (`getLangFromUrl`, `useTranslations`)
- **Interfaces**: `PascalCase` with descriptive nouns (`PaymentData`, `TranslationKey`)
- **Constants**: `UPPER_SNAKE_CASE` or `camelCase` for objects (`languages`, `defaultLang`)
- **Variables**: `camelCase` with meaningful names (`clientSecret`, `paymentIntent`)

## Documentation Standards

### Function Documentation (Python)
```python
async def create_payment(
    payment_request: PaymentRequest,
    stripe_service: StripeService = Depends(get_stripe_service)
) -> PaymentResponse:
    """Create a payment (one-time or subscription)"""
```

### Function Documentation (TypeScript)
```typescript
export function getLangFromUrl(url: URL) {
  // Extract language from URL path
  const [, lang] = url.pathname.split('/');
  if (lang in languages) return lang as keyof typeof languages;
  return defaultLang;
}
```

## Security Patterns

### Input Validation Pattern
- **Backend**: Pydantic models with custom validators for all inputs
- **Frontend**: Client-side validation + server-side confirmation
- **Email Validation**: Regex pattern + length checks + header injection prevention
- **Amount Validation**: Minimum thresholds + integer conversion (cents)

### Error Handling Pattern
```python
try:
    # Business logic
    result = await service.process()
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
except HTTPException:
    raise  # Re-raise HTTP exceptions
except Exception as e:
    log_error(request_id, e, "Context description")
    raise HTTPException(status_code=500, detail="Internal server error")
```

### Logging Pattern
```python
request_id = str(uuid.uuid4())[:8]
logger.info(f"[{request_id}] Processing request for {user_email}")
log_payment_attempt(request_id, email, amount, currency, success)
```

## API Design Patterns

### Dependency Injection Pattern
```python
def get_stripe_service() -> StripeService:
    return StripeService()

@router.post("/create")
async def create_payment(
    payment_request: PaymentRequest,
    stripe_service: StripeService = Depends(get_stripe_service)
):
```

### Response Model Pattern
```python
@router.post("/create", response_model=PaymentResponse)
async def create_payment(...) -> PaymentResponse:
    return PaymentResponse(
        success=True,
        payment_id=payment_intent.id,
        client_secret=client_secret,
        message="Payment intent created successfully"
    )
```

### Service Layer Pattern
```python
class EmailService:
    def __init__(self):
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
    
    async def send_email(self, to_emails: List[str], subject: str, html_content: str):
        # Implementation with validation and error handling
```

## Testing Patterns

### Test Organization
- **Test Classes**: Group related tests (`TestPayments`, `TestPaymentModels`)
- **Mock Pattern**: Use `@patch` decorators for external service mocking
- **Test Data**: Realistic test data with edge cases
- **Assertions**: Specific assertions for each test case

### Mock Pattern Example
```python
@patch('app.services.stripe_service.StripeService.create_customer')
@patch('app.services.email_service.EmailService.send_payment_confirmation')
def test_create_payment_success(self, mock_email, mock_customer):
    mock_customer.return_value = {"success": True, "customer": mock_object}
    # Test implementation
```

## Internationalization Patterns

### Translation Key Structure
```typescript
export const translations = {
  pt: {
    'section.key': 'Valor em Português',
    'validation.field_required': 'Campo obrigatório'
  },
  en: {
    'section.key': 'English Value',
    'validation.field_required': 'Field required'
  }
};
```

### Translation Usage Pattern
```typescript
export function useTranslations(lang: keyof typeof translations) {
  return function t(key: keyof typeof translations[typeof defaultLang]) {
    return translations[lang][key] || translations[defaultLang][key];
  }
}
```

## Configuration Patterns

### Environment Configuration
```python
class Settings(BaseSettings):
    stripe_secret_key: str
    stripe_publishable_key: str
    environment: str = "development"
    
    @property
    def notification_email_list(self) -> List[str]:
        return [email.strip() for email in self.notification_emails.split(',')]
```

### Frontend Configuration
```javascript
export default defineConfig({
  integrations: [tailwind(), vue()],
  i18n: {
    defaultLocale: "pt",
    locales: ["pt", "en"],
    routing: { prefixDefaultLocale: false }
  }
});
```

## Common Code Idioms

### Request ID Generation
```python
request_id = str(uuid.uuid4())[:8]  # Short unique identifier
```

### Amount Formatting
```python
amount_display = f"${amount / 100:.2f}" if currency == "usd" else f"R${amount / 100:.2f}"
```

### Email Validation
```python
def _validate_email(self, email: str) -> bool:
    if not email or len(email) > 254:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

### Template Rendering
```python
template = Template(html_content)
rendered_html = template.render(
    success=success,
    name=payment_request.name,
    amount_display=amount_display
)
```

## Frequently Used Annotations

### Python Annotations
- `@router.post("/endpoint", response_model=ResponseModel)`
- `@patch('module.Class.method')` for testing
- `async def function_name(...) -> ReturnType:`
- `field: str = Field(..., min_length=2, max_length=100)`

### TypeScript Annotations
- `export const languages = {...} as const;`
- `function t(key: keyof typeof translations[typeof defaultLang])`
- `lang as keyof typeof languages`
- `url: URL` for function parameters

## Security Implementation Patterns

### Header Sanitization
```python
def _sanitize_subject(self, subject: str) -> str:
    return re.sub(r'[\r\n]', '', subject)[:200]
```

### Middleware Pattern
```python
app.middleware("http")(rate_limit_middleware)
app.middleware("http")(security_headers_middleware)
```

### Authentication Dependency
```python
credentials: HTTPAuthorizationCredentials = Depends(api_key_auth)
```

These patterns are consistently applied across the codebase and should be followed for all new development to maintain code quality, security, and maintainability standards.