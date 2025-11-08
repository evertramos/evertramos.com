# Technology Stack - Ezyba

## Programming Languages
- **TypeScript**: Frontend development with type safety
- **Python 3.11+**: Backend API development
- **JavaScript**: Client-side interactivity
- **HTML/CSS**: Markup and styling

## Frontend Stack

### Core Framework
- **Astro 4.16.12**: Static site generator with component islands
- **Vue 3.4.38**: Interactive components for payment forms
- **TypeScript 5.6.3**: Type-safe development

### Styling & UI
- **Tailwind CSS 3.4.14**: Utility-first CSS framework
- **Responsive Design**: Mobile-first approach (320px, 768px, 1024px, 1440px)

### Payment Integration
- **@stripe/stripe-js 4.8.0**: Stripe Elements for secure payment forms
- **Stripe Elements**: PCI-compliant card input components

### Build Tools
- **Vite**: Fast build tool (via Astro)
- **Node.js**: Runtime environment
- **npm**: Package management

## Backend Stack

### Core Framework
- **FastAPI 0.115.4**: Modern Python web framework
- **Uvicorn 0.32.0**: ASGI server with standard extras
- **Pydantic 2.9.2**: Data validation and settings management

### Payment Processing
- **Stripe 11.2.0**: Payment processing SDK
- **Webhook Validation**: Secure event handling

### Email & Communication
- **aiosmtplib 3.0.2**: Async SMTP client
- **Jinja2 3.1.4**: Email template engine
- **email-validator 2.2.0**: Email format validation

### Development & Testing
- **pytest 8.3.3**: Testing framework
- **pytest-asyncio 0.24.0**: Async test support
- **httpx 0.27.2**: HTTP client for testing
- **python-multipart 0.0.12**: Form data handling

## Infrastructure & Deployment

### Containerization
- **Docker**: Application containerization
- **Docker Compose**: Multi-service orchestration
- **Nginx**: Reverse proxy and static file serving

### Development Environment
- **Hot Reload**: Automatic code reloading
- **Mailpit**: Email testing interface
- **Volume Mounting**: Live code updates

### Production Environment
- **AWS SES**: Email delivery service
- **HTTPS**: SSL/TLS encryption
- **Environment Variables**: Secure configuration

## Development Commands

### Frontend Development
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Backend Development
```bash
# Install dependencies
pip install -r requirements.txt

# Start development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run tests
python -m pytest tests/ -v --cov=app

# Run specific test
python -m pytest tests/test_payments.py -v
```

### Docker Development
```bash
# Start development environment
docker compose -f docker-compose.dev.yml up --build

# Start production environment
docker compose up -d --build

# View logs
docker compose logs -f

# Stop services
docker compose down
```

## Build System

### Frontend Build Process
1. **TypeScript Compilation**: Type checking and transpilation
2. **Astro Build**: Static site generation with component islands
3. **Tailwind Processing**: CSS utility compilation
4. **Asset Optimization**: Image and resource optimization

### Backend Build Process
1. **Dependency Installation**: Python package management
2. **FastAPI Application**: ASGI application setup
3. **Environment Configuration**: Settings validation
4. **Container Packaging**: Docker image creation

## Configuration Management

### Environment Variables
- **STRIPE_PUBLISHABLE_KEY**: Frontend Stripe configuration
- **STRIPE_SECRET_KEY**: Backend Stripe API access
- **SMTP_***: Email service configuration
- **ENVIRONMENT**: Development/production mode

### Configuration Files
- **astro.config.mjs**: Astro framework settings
- **tailwind.config.mjs**: CSS framework customization
- **config.py**: Python application settings
- **docker-compose.yml**: Service orchestration

## Security Technologies

### Frontend Security
- **Content Security Policy**: XSS protection
- **HTTPS Enforcement**: Secure communication
- **Stripe Elements**: PCI-compliant payment forms

### Backend Security
- **Pydantic Validation**: Input sanitization
- **Type Hints**: Runtime type checking
- **CORS Configuration**: Cross-origin request control
- **Rate Limiting**: API abuse prevention

## Monitoring & Logging

### Logging Framework
- **Python Logging**: Structured application logs
- **Request Tracking**: Unique request IDs
- **Error Handling**: Comprehensive error logging

### Development Tools
- **FastAPI Docs**: Automatic API documentation
- **Pytest Coverage**: Code coverage reporting
- **Docker Logs**: Container log aggregation