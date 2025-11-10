#!/bin/bash

# Simple restart script for Ezyba development
echo "🔄 Restarting Ezyba development environment..."

# Stop containers
docker compose -f docker-compose.dev.yml down

# Start with fresh build if needed
DOCKER_BUILDKIT=1 docker compose -f docker-compose.dev.yml up -d --build

echo "✅ Environment restarted!"
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:8000"
echo "Mailpit:  http://localhost:8025"