#!/bin/bash

# Build without provenance to avoid metadata resolution issues
echo "🔨 Building without provenance..."

export DOCKER_BUILDKIT=1
export BUILDKIT_PROGRESS=plain

# Build with no provenance
docker compose -f docker-compose.dev.yml build \
  --build-arg BUILDKIT_INLINE_CACHE=1 \
  --no-cache

echo "✅ Build completed without provenance!"