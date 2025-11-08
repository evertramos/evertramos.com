#!/bin/bash

# Start development environment
echo "🚀 Starting Ezyba development environment..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Run ./scripts/setup.sh first."
    exit 1
fi

# Start development containers
docker compose -f docker-compose.dev.yml up --build

echo "🎉 Development environment started!"
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "Mailpit (Email): http://localhost:8025"