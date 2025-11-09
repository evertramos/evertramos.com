# Ezyba Development Commands

.PHONY: help dev restart restart-smart stop logs clean

# Default target
help:
	@echo "🚀 Ezyba Development Commands"
	@echo "============================="
	@echo ""
	@echo "📦 Environment:"
	@echo "  dev           - Start development environment"
	@echo "  restart       - Simple restart (always rebuilds)"
	@echo "  restart-smart - Smart restart (cache-aware)"
	@echo "  stop          - Stop all containers"
	@echo ""
	@echo "📊 Monitoring:"
	@echo "  logs          - View all logs"
	@echo "  logs-fe       - View frontend logs"
	@echo "  logs-be       - View backend logs"
	@echo ""
	@echo "🧹 Cleanup:"
	@echo "  clean         - Remove containers and images"
	@echo "  clean-all     - Full cleanup (including volumes)"

# Start development environment
dev:
	@echo "🚀 Starting development environment..."
	docker compose -f docker-compose.dev.yml up -d
	@echo "✅ Environment started!"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend:  http://localhost:8000"
	@echo "Mailpit:  http://localhost:8025"

# Simple restart
restart:
	@./scripts/restart.sh

# Smart restart with cache optimization
restart-smart:
	@./scripts/dev-restart.sh

# Stop containers
stop:
	@echo "🛑 Stopping containers..."
	docker compose -f docker-compose.dev.yml down
	@echo "✅ Containers stopped"

# View logs
logs:
	docker compose -f docker-compose.dev.yml logs -f

logs-fe:
	docker compose -f docker-compose.dev.yml logs -f frontend

logs-be:
	docker compose -f docker-compose.dev.yml logs -f backend

# Cleanup
clean:
	@echo "🧹 Cleaning up containers and images..."
	docker compose -f docker-compose.dev.yml down --rmi all
	@echo "✅ Cleanup completed"

clean-all:
	@echo "🧹 Full cleanup (containers, images, volumes)..."
	docker compose -f docker-compose.dev.yml down --rmi all --volumes
	docker system prune -f
	@echo "✅ Full cleanup completed"