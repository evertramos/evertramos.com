#!/bin/bash

# Ezyba Development Restart Script
# Intelligently restarts dev environment with cache optimization

set -e

echo "🔄 Ezyba Development Restart"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "docker-compose.dev.yml" ]; then
    echo -e "${RED}❌ Error: docker-compose.dev.yml not found. Run from project root.${NC}"
    exit 1
fi

# Function to check if containers are running
check_containers() {
    if docker compose -f docker-compose.dev.yml ps --services --filter "status=running" | grep -q .; then
        return 0
    else
        return 1
    fi
}

# Step 1: Stop existing containers
echo -e "${YELLOW}📦 Stopping containers...${NC}"
if check_containers; then
    docker compose -f docker-compose.dev.yml down
    echo -e "${GREEN}✅ Containers stopped${NC}"
else
    echo -e "${BLUE}ℹ️  No running containers found${NC}"
fi

# Step 2: Check for changes that require rebuild
echo -e "${YELLOW}🔍 Checking for changes...${NC}"

REBUILD_NEEDED=false

# Check if Dockerfiles changed
if [ -n "$(find . -name "Dockerfile*" -newer .last-build 2>/dev/null)" ]; then
    echo -e "${BLUE}📝 Dockerfile changes detected${NC}"
    REBUILD_NEEDED=true
fi

# Check if package files changed
if [ -n "$(find . -name "package*.json" -newer .last-build 2>/dev/null)" ] || \
   [ -n "$(find . -name "requirements.txt" -newer .last-build 2>/dev/null)" ]; then
    echo -e "${BLUE}📦 Dependency changes detected${NC}"
    REBUILD_NEEDED=true
fi

# Check if .env files changed
if [ -n "$(find . -name ".env*" -newer .last-build 2>/dev/null)" ]; then
    echo -e "${BLUE}⚙️  Environment changes detected${NC}"
    REBUILD_NEEDED=true
fi

# Check if no previous build exists
if [ ! -f ".last-build" ]; then
    echo -e "${BLUE}🆕 No previous build found${NC}"
    REBUILD_NEEDED=true
fi

# Step 3: Build or use cache
if [ "$REBUILD_NEEDED" = true ]; then
    echo -e "${YELLOW}🔨 Building with changes...${NC}"
    DOCKER_BUILDKIT=1 docker compose -f docker-compose.dev.yml build --no-cache
    touch .last-build
    echo -e "${GREEN}✅ Build completed${NC}"
else
    echo -e "${GREEN}⚡ Using cached images (no changes detected)${NC}"
fi

# Step 4: Start containers
echo -e "${YELLOW}🚀 Starting development environment...${NC}"
DOCKER_BUILDKIT=1 docker compose -f docker-compose.dev.yml up -d

# Step 5: Wait for services to be ready
echo -e "${YELLOW}⏳ Waiting for services...${NC}"
sleep 3

# Check if services are healthy
echo -e "${YELLOW}🏥 Health check...${NC}"

# Check frontend
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend ready: http://localhost:3000${NC}"
else
    echo -e "${RED}❌ Frontend not responding${NC}"
fi

# Check backend
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend ready: http://localhost:8000${NC}"
else
    echo -e "${RED}❌ Backend not responding${NC}"
fi

# Check mailpit
if curl -s http://localhost:8025 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Mailpit ready: http://localhost:8025${NC}"
else
    echo -e "${RED}❌ Mailpit not responding${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Development environment restarted!${NC}"
echo ""
echo -e "${BLUE}📋 Available services:${NC}"
echo -e "   Frontend:  ${YELLOW}http://localhost:3000${NC}"
echo -e "   Backend:   ${YELLOW}http://localhost:8000${NC}"
echo -e "   API Docs:  ${YELLOW}http://localhost:8000/docs${NC}"
echo -e "   Mailpit:   ${YELLOW}http://localhost:8025${NC}"
echo ""
echo -e "${BLUE}📊 View logs:${NC}"
echo -e "   All:       ${YELLOW}docker compose -f docker-compose.dev.yml logs -f${NC}"
echo -e "   Frontend:  ${YELLOW}docker compose -f docker-compose.dev.yml logs -f frontend${NC}"
echo -e "   Backend:   ${YELLOW}docker compose -f docker-compose.dev.yml logs -f backend${NC}"
echo ""
echo -e "${GREEN}✨ Happy coding!${NC}"