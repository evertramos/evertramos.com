#!/bin/bash

# Deploy to production
echo "🚀 Deploying Ezyba to production..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please create it with production values."
    exit 1
fi

# Verify production environment variables
if grep -q "pk_test_" .env || grep -q "sk_test_" .env; then
    echo "⚠️  WARNING: Test Stripe keys detected in .env"
    echo "   Make sure to use live keys for production!"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Build and deploy
echo "🏗️  Building production containers..."
export DOCKER_BUILDKIT=1
docker compose build --no-cache --build-arg BUILDKIT_INLINE_CACHE=1

echo "🚀 Starting production services..."
docker compose up -d

echo "🎉 Production deployment complete!"
echo "Services are running in background."
echo "Check logs with: docker compose logs -f"