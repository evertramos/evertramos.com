# Ezyba - Secure Payment Platform

A secure payment processing platform built with Astro (frontend) and FastAPI (backend), integrated with Stripe for maximum security and PCI compliance.

## 🏗️ Architecture

- **Frontend**: Astro + TypeScript + Tailwind CSS
- **Backend**: Python + FastAPI + Pydantic
- **Payments**: Stripe Elements + Payment Intents/Subscriptions
- **Deployment**: Docker + Docker Compose
- **Security**: Zero data storage, Stripe handles all sensitive data

## 🚀 Quick Start

### Development Environment

1. **Clone and setup**:
```bash
git clone <repository>
cd ezyba
cp .env.example .env
```

2. **Configure environment variables** in `.env`:
```bash
# Stripe (use test keys for development)
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Email configuration (Mailpit for development)
NOTIFICATION_EMAILS=admin@ezyba.com,finance@ezyba.com
SMTP_HOST=mailpit
SMTP_PORT=1025
SMTP_USER=
SMTP_PASSWORD=

ENVIRONMENT=development
```

3. **Start development environment**:
```bash
docker compose -f docker-compose.dev.yml up --build
```

4. **Access the application**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Mailpit (Email testing): http://localhost:8025

### Production Deployment

1. **Update environment variables** for production:
```bash
# Use live Stripe keys
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...

# AWS SES configuration
SMTP_HOST=email-smtp.us-east-1.amazonaws.com
SMTP_PORT=587
SMTP_USER=your-aws-ses-access-key
SMTP_PASSWORD=your-aws-ses-secret-key

ENVIRONMENT=production
```

2. **Deploy with production compose**:
```bash
docker compose up -d --build
```

## 🔒 Security Features

### Frontend Security
- ✅ Content Security Policy (CSP) configured for Stripe
- ✅ XSS protection headers
- ✅ HTTPS enforcement
- ✅ No sensitive data in client-side code
- ✅ Stripe Elements for secure card input

### Backend Security
- ✅ Input validation with Pydantic models
- ✅ Type hints on all functions
- ✅ Rate limiting ready
- ✅ CORS properly configured
- ✅ No SQL injection (no database)
- ✅ Secure environment variable handling

### Payment Security
- ✅ PCI DSS compliance through Stripe
- ✅ No card data storage
- ✅ Secure tokenization
- ✅ Payment confirmation flow
- ✅ Error handling and logging

## 🌍 Multi-language Support

The platform supports Portuguese (default) and English:

- **Portuguese**: `evertramos.com.br` (/)
- **English**: `evertramos.com` (/en)

URLs are automatically localized:
- `/pagamento` → `/en/payment`
- `/gerenciar` → `/en/manage`
- `/privacidade` → `/en/privacy`

## 💳 Payment Flow

1. **Customer fills form**: Name, email, phone (optional)
2. **Payment details**: Amount, currency (BRL/USD), type (one-time/monthly/yearly)
3. **Stripe Elements**: Secure card input
4. **Backend processing**: Creates Payment Intent or Subscription
5. **Stripe confirmation**: 3D Secure if required
6. **Email notifications**: Sent to customer and admin emails

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/ -v --cov=app
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Manual Testing Checklist

#### Responsiveness (Required breakpoints)
- [ ] 320px (Mobile portrait)
- [ ] 768px (Tablet)
- [ ] 1024px (Desktop)
- [ ] 1440px (Large desktop)

#### Security Testing
- [ ] CSP headers present
- [ ] No sensitive data in browser
- [ ] HTTPS redirects working
- [ ] Form validation working
- [ ] Error handling secure

#### Multi-language Testing
- [ ] PT/EN translations complete
- [ ] URL localization working
- [ ] Language switcher functional
- [ ] SEO hreflang tags present

## 📁 Project Structure

```
ezyba/
├── frontend/                 # Astro frontend
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── layouts/         # Page layouts
│   │   ├── pages/           # Route pages
│   │   │   ├── en/         # English pages
│   │   │   └── *.astro     # Portuguese pages (default)
│   │   ├── i18n/           # Internationalization
│   │   └── styles/         # Global styles
│   └── Dockerfile
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── models/         # Pydantic models
│   │   ├── services/       # Business logic
│   │   ├── routers/        # API routes
│   │   └── config.py       # Configuration
│   ├── tests/              # Test files
│   └── Dockerfile
├── .amazonq/
│   └── rules/              # Development rules
├── docker-compose.yml       # Production
├── docker-compose.dev.yml   # Development
└── .env.example            # Environment template
```

## 🔧 API Endpoints

### Payment Endpoints
- `POST /api/v1/payments/create` - Create payment
- `POST /api/v1/payments/customer-portal` - Customer portal
- `GET /api/v1/payments/config` - Stripe configuration

### Health Check
- `GET /health` - Service health status

## 📧 Email Notifications

Automatic email notifications are sent for:
- ✅ Successful payments (customer + admin)
- ✅ Failed payments (customer + admin)
- ✅ Subscription confirmations
- ✅ Payment errors

## 🚨 Monitoring & Logging

### Log Files (Production)
- **All logs**: `../data/logs/ezyba.log`
- **Errors only**: `../data/logs/ezyba_errors.log`
- **Security events**: `../data/logs/ezyba_security.log`

### Log Viewing
```bash
# View all logs
./scripts/logs.sh all

# View errors only
./scripts/logs.sh errors

# View security events
./scripts/logs.sh security

# View Docker logs
./scripts/logs.sh docker
```

### Logged Events
- Payment attempts (success/failure)
- Security violations (invalid API keys, rate limiting)
- Application errors with context
- Request tracking with unique IDs
- Email sending failures

## 🔄 Development Workflow

1. **Make changes** to code
2. **Run tests**: `npm test` / `pytest`
3. **Check security**: Automatic via Amazon Q rules
4. **Test responsiveness**: All breakpoints
5. **Verify translations**: PT/EN both working
6. **Deploy**: Docker Compose

## 📞 Support

For technical support or questions:
- Email: admin@ezyba.com
- Documentation: This README
- API Docs: `/docs` endpoint

---

**Security Notice**: This platform is designed with security-first principles. All payment processing is handled by Stripe, ensuring PCI DSS compliance without requiring certification on our end.