# Technology Stack and Development

## Programming Languages and Versions

### Frontend
- **TypeScript**: ^5.6.3 - Type-safe JavaScript with modern ES features
- **JavaScript**: ES2022+ - Modern JavaScript features and syntax
- **CSS**: CSS3 with Tailwind utility classes
- **HTML**: HTML5 with Astro templating

### Backend
- **Python**: 3.11+ - Modern Python with type hints and async support
- **SQL**: None (zero database storage for security)

## Core Frameworks and Libraries

### Frontend Stack
- **Astro**: ^4.16.12 - Static site generator with island architecture
- **Vue**: ^3.4.38 - Progressive JavaScript framework for components
- **Tailwind CSS**: ^3.4.14 - Utility-first CSS framework
- **Stripe.js**: ^4.8.0 - Official Stripe JavaScript library

### Backend Stack
- **FastAPI**: 0.115.4 - Modern Python web framework
- **Uvicorn**: 0.32.0 - ASGI server with standard extras
- **Pydantic**: 2.9.2 - Data validation using Python type annotations
- **Stripe Python**: 11.2.0 - Official Stripe Python library

## Build Systems and Tools

### Frontend Build System
- **Astro Build**: Static site generation with optimized output
- **Vite**: Fast build tool and development server
- **TypeScript Compiler**: Type checking and compilation
- **Tailwind CLI**: CSS processing and optimization

### Backend Build System
- **Python Package Management**: pip with requirements.txt
- **FastAPI**: Built-in OpenAPI documentation generation
- **Uvicorn**: Production ASGI server

### Containerization
- **Docker**: Multi-stage builds for optimized images
- **Docker Compose**: Service orchestration and networking
- **Nginx**: Reverse proxy and static file serving (frontend)

## Development Dependencies and Tools

### Frontend Development
```json
{
  "@types/node": "^22.8.7",
  "astro": "^4.16.12",
  "typescript": "^5.6.3"
}
```

### Backend Development
```txt
pytest==8.3.3
pytest-asyncio==0.24.0
httpx==0.27.2
```

### Additional Services
- **Email**: aiosmtplib 3.0.2 with Jinja2 3.1.4 templating
- **Validation**: email-validator 2.2.0
- **HTTP Client**: httpx 0.27.2 for external API calls

## Development Commands

### Frontend Commands
```bash
# Development server
npm run dev

# Production build
npm run build

# Preview production build
npm run preview

# Start development (alias)
npm start
```

### Backend Commands
```bash
# Development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production server
uvicorn main:app --host 0.0.0.0 --port 8000

# Run tests
python -m pytest tests/ -v --cov=app

# Run specific test file
python -m pytest tests/test_payments.py -v
```

### Docker Commands
```bash
# Development environment
docker compose -f docker-compose.dev.yml up --build

# Production environment
docker compose up -d --build

# View logs
docker compose logs -f

# Restart services
docker compose restart
```

## Configuration Management

### Environment Variables
```bash
# Stripe Configuration
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Email Configuration
NOTIFICATION_EMAILS=admin@ezyba.com
SMTP_HOST=mailpit
SMTP_PORT=1025

# Security
TURNSTILE_SECRET_KEY=...
PUBLIC_TURNSTILE_SITE_KEY=...

# Environment
ENVIRONMENT=development|production
```

### Astro Configuration
```javascript
// astro.config.mjs
export default defineConfig({
  integrations: [tailwind(), vue()],
  i18n: {
    defaultLocale: "pt",
    locales: ["pt", "en"],
    routing: { prefixDefaultLocale: false }
  },
  server: { host: '0.0.0.0', port: 3000 }
});
```

### FastAPI Configuration
```python
# config.py
class Settings(BaseSettings):
    stripe_secret_key: str
    stripe_publishable_key: str
    notification_emails: str
    environment: str = "development"
```

## Testing Framework

### Frontend Testing
- **Framework**: Built-in Astro testing capabilities
- **Type Checking**: TypeScript compiler validation
- **Linting**: ESLint configuration (implicit)

### Backend Testing
- **Framework**: pytest with asyncio support
- **Coverage**: pytest-cov for coverage reporting
- **HTTP Testing**: httpx for API endpoint testing
- **Mocking**: Built-in unittest.mock for external services

### Test Structure
```
tests/
├── models/          # Pydantic model tests
├── routers/         # API endpoint tests
├── services/        # Business logic tests
└── utils/           # Utility function tests
```

## Deployment Technology

### Container Technology
- **Base Images**: Python 3.11-slim, Node 18-alpine
- **Multi-stage Builds**: Optimized production images
- **Health Checks**: Built-in container health monitoring
- **Volume Mounting**: Log persistence and data management

### Networking
- **Docker Networks**: Isolated service communication
- **Port Mapping**: 3000 (frontend), 8000 (backend)
- **Reverse Proxy**: Nginx for frontend static serving
- **CORS**: Configured for cross-origin requests

### Monitoring and Logging
- **Structured Logging**: JSON format with multiple levels
- **Log Rotation**: File-based logging with external volumes
- **Health Endpoints**: /health for service monitoring
- **Error Tracking**: Comprehensive error logging and reporting