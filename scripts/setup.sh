#!/bin/bash

# Ezyba Setup Script
echo "🚀 Setting up Ezyba development environment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please install Docker with Compose plugin."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env file with your Stripe keys and email configuration"
    echo "   You can get test keys from: https://dashboard.stripe.com/test/apikeys"
fi

# Build and start development environment
echo "🏗️  Building development environment..."
export DOCKER_BUILDKIT=1
docker compose -f docker-compose.dev.yml build --build-arg BUILDKIT_INLINE_CACHE=1

echo "🎉 Setup complete!"
echo ""
echo "✅ Fixed dependency conflicts in requirements.txt"
echo "✅ Updated Dockerfiles to handle missing package-lock.json"
echo ""
echo "Next steps:"
echo "1. Update .env file with your configuration"
echo "2. Run: ./scripts/dev.sh to start development"
echo "3. Access frontend at: http://localhost:3000"
echo "4. Access backend at: http://localhost:8000"
echo "5. Access Mailpit (email testing): http://localhost:8025"
echo ""