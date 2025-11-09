from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import stripe
import logging
from contextlib import asynccontextmanager

from app.config import settings
from app.routers import payments
from app.middleware.security import rate_limit_middleware, security_headers_middleware
from app.utils.logging import setup_logging


# Configure logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    stripe.api_key = settings.stripe_secret_key
    logger.info(f"Starting Ezyba API in {settings.environment} mode")
    yield
    # Shutdown
    logger.info("Shutting down Ezyba API")


app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    lifespan=lifespan
)

# Security Middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.allowed_hosts_list + ["127.0.0.1"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Security middleware
app.middleware("http")(rate_limit_middleware)
app.middleware("http")(security_headers_middleware)

# Include routers
app.include_router(payments.router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "environment": settings.environment}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )