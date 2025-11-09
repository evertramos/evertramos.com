# Project Structure and Architecture

## Directory Organization

### Root Level
```
ezyba/
├── frontend/           # Astro frontend application
├── backend/            # FastAPI backend application
├── scripts/            # Deployment and utility scripts
├── docs/              # Project documentation
├── .amazonq/          # Amazon Q configuration and rules
├── docker-compose.yml # Production deployment
└── docker-compose.dev.yml # Development environment
```

### Frontend Structure (`frontend/`)
```
frontend/
├── src/
│   ├── components/    # Vue components (PaymentForm.vue)
│   ├── layouts/       # Astro layouts (Layout.astro)
│   ├── pages/         # Route pages with i18n structure
│   │   ├── en/        # English pages (/en/*)
│   │   └── *.astro    # Portuguese pages (default)
│   ├── i18n/          # Internationalization configuration
│   ├── styles/        # Global CSS styles
│   └── utils/         # Utility functions
├── public/            # Static assets (images, robots.txt)
├── astro.config.mjs   # Astro configuration
├── package.json       # Dependencies and scripts
└── Dockerfile         # Container configuration
```

### Backend Structure (`backend/`)
```
backend/
├── app/
│   ├── models/        # Pydantic data models
│   ├── routers/       # FastAPI route handlers
│   ├── services/      # Business logic services
│   ├── middleware/    # Security middleware
│   ├── utils/         # Utility functions
│   └── config.py      # Application configuration
├── tests/             # Test files mirroring app structure
├── main.py            # FastAPI application entry point
├── requirements.txt   # Python dependencies
└── Dockerfile         # Container configuration
```

## Core Components and Relationships

### Frontend Architecture
- **Astro Framework**: Static site generation with dynamic islands
- **Vue Components**: Interactive payment forms and UI elements
- **Tailwind CSS**: Utility-first styling with responsive design
- **i18n Integration**: Route-based localization (PT default, EN prefixed)

### Backend Architecture
- **FastAPI**: Modern Python web framework with automatic API documentation
- **Pydantic Models**: Type-safe data validation and serialization
- **Service Layer**: Business logic separation (Stripe, Email, Turnstile)
- **Middleware**: Security headers and request processing

### Integration Points
- **Stripe Elements**: Secure card input integration in frontend
- **Payment API**: Backend endpoints for payment processing
- **Email Service**: Notification system for payment events
- **Turnstile**: Cloudflare bot protection integration

## Architectural Patterns

### Security-First Design
- Zero sensitive data storage on platform
- All payment processing delegated to Stripe
- Environment-based configuration management
- Comprehensive input validation and sanitization

### Microservice-Ready Structure
- Clear separation between frontend and backend
- Service-oriented backend architecture
- Docker containerization for deployment
- Network isolation with Docker Compose

### Internationalization Pattern
- Route-based localization (`/` for PT, `/en/` for EN)
- Shared component structure across languages
- Centralized translation management
- SEO-optimized with proper hreflang tags

### Responsive Design Pattern
- Mobile-first CSS approach
- Breakpoint-based design (320px, 768px, 1024px, 1440px)
- Touch-friendly interface elements
- Cross-device compatibility testing

## Data Flow Architecture

### Payment Processing Flow
1. **Frontend**: User fills payment form with Stripe Elements
2. **Backend**: Creates Payment Intent/Subscription via Stripe API
3. **Stripe**: Handles secure payment processing and 3D Secure
4. **Backend**: Receives confirmation and sends email notifications
5. **Frontend**: Displays success/error states to user

### Configuration Management
- Environment variables for all sensitive data
- Separate configurations for development/production
- Docker environment variable injection
- Secure secret management practices

## Deployment Architecture

### Development Environment
- Hot reload for both frontend and backend
- Mailpit for email testing
- Local Docker network for service communication
- Development-specific environment variables

### Production Environment
- Optimized Docker images with multi-stage builds
- External log volume mounting
- Production email service integration (AWS SES)
- Health check endpoints for monitoring
- Restart policies for high availability