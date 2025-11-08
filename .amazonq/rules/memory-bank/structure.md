# Project Structure - Ezyba

## Directory Organization

### Root Level
```
ezyba/
├── frontend/          # Astro frontend application
├── backend/           # FastAPI backend API
├── scripts/           # Development and deployment scripts
├── docs/              # Documentation files
├── .amazonq/          # Amazon Q configuration and rules
├── docker-compose.yml # Production deployment
└── docker-compose.dev.yml # Development environment
```

## Frontend Structure (Astro)
```
frontend/
├── src/
│   ├── components/    # Reusable Vue/Astro components
│   ├── layouts/       # Page layout templates
│   ├── pages/         # Route-based pages
│   │   ├── en/        # English localized pages
│   │   └── *.astro    # Portuguese pages (default)
│   ├── i18n/          # Internationalization configuration
│   ├── styles/        # Global CSS styles
│   └── utils/         # Frontend utilities
├── public/            # Static assets
└── astro.config.mjs   # Astro configuration
```

### Page Structure
- **Portuguese Routes**: `/`, `/pagamento`, `/gerador`, `/privacidade`, `/termos`
- **English Routes**: `/en/`, `/en/payment`, `/en/generator`, `/en/privacy`, `/en/terms`
- **Shared Components**: PaymentForm.vue for payment processing

## Backend Structure (FastAPI)
```
backend/
├── app/
│   ├── models/        # Pydantic data models
│   ├── routers/       # API route handlers
│   ├── services/      # Business logic services
│   ├── middleware/    # Security and request middleware
│   ├── utils/         # Backend utilities
│   └── config.py      # Application configuration
├── tests/             # Test suite
└── main.py            # FastAPI application entry point
```

### API Architecture
- **Payment Router**: `/api/v1/payments/` - Payment processing endpoints
- **Health Check**: `/health` - Service status monitoring
- **Services Layer**: Stripe integration, email notifications
- **Middleware**: Security headers, CORS, request logging

## Core Components

### Frontend Components
- **Layout.astro**: Base page template with SEO and security headers
- **PaymentForm.vue**: Stripe Elements integration for secure payments
- **Language Switcher**: Automatic PT/EN localization

### Backend Services
- **StripeService**: Payment processing and subscription management
- **EmailService**: Notification system for payment events
- **SecurityMiddleware**: CSP headers and security enforcement

## Architectural Patterns

### Security-First Design
- Zero sensitive data storage
- Stripe handles all payment data
- Environment-based configuration
- Comprehensive input validation

### Multi-Language Architecture
- Route-based localization (/en/ prefix)
- Shared component logic with localized content
- SEO optimization with hreflang tags

### Container Architecture
- **Development**: Hot reload, Mailpit for email testing
- **Production**: Nginx proxy, AWS SES integration
- **Shared**: Environment variable configuration

## Configuration Files

### Frontend Configuration
- `astro.config.mjs`: Astro framework configuration
- `tailwind.config.mjs`: Tailwind CSS customization
- `package.json`: Dependencies and scripts

### Backend Configuration
- `requirements.txt`: Python dependencies
- `config.py`: Environment-based settings
- `Dockerfile`: Container build instructions

### Deployment Configuration
- `docker-compose.yml`: Production deployment
- `docker-compose.dev.yml`: Development environment
- `.env.example`: Environment variable template

## Data Flow

### Payment Processing Flow
1. **Frontend**: Customer fills payment form
2. **Stripe Elements**: Secure card data collection
3. **Backend API**: Payment Intent/Subscription creation
4. **Stripe**: Payment processing and confirmation
5. **Email Service**: Notification delivery
6. **Frontend**: Success/error handling

### Development Workflow
1. **Local Development**: Docker Compose with hot reload
2. **Testing**: Automated test suite execution
3. **Security Validation**: Amazon Q rule enforcement
4. **Deployment**: Container-based production deployment