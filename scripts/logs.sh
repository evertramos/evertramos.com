#!/bin/bash

# View Ezyba logs
echo "📋 Ezyba Log Viewer"

if [ ! -d "../data/logs" ]; then
    echo "❌ Log directory not found. Make sure production is running."
    exit 1
fi

case "${1:-all}" in
    "all")
        echo "📄 All logs:"
        tail -f ../data/logs/ezyba.log
        ;;
    "errors")
        echo "🚨 Error logs:"
        tail -f ../data/logs/ezyba_errors.log
        ;;
    "security")
        echo "🔒 Security logs:"
        tail -f ../data/logs/ezyba_security.log
        ;;
    "docker")
        echo "🐳 Docker container logs:"
        docker compose logs -f backend
        ;;
    *)
        echo "Usage: $0 [all|errors|security|docker]"
        echo ""
        echo "Options:"
        echo "  all      - View all application logs (default)"
        echo "  errors   - View error logs only"
        echo "  security - View security events"
        echo "  docker   - View Docker container logs"
        ;;
esac