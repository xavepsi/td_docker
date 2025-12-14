#!/bin/bash
set -e

echo "=== Building Docker images ==="
docker build -t td_api:latest ./api
docker build -t td_front:latest ./front

echo ""
echo "=== Image sizes ==="
docker images td_api:latest --format "API: {{.Size}}"
docker images td_front:latest --format "Front: {{.Size}}"

echo ""
echo "=== Validating docker-compose ==="
docker compose config

echo ""
echo "=== Starting stack ==="
docker compose up -d

echo ""
echo "=== Stack started ==="
echo "API: http://localhost:8000/status"
echo "Frontend: http://localhost:8080"
echo ""
echo "To view logs: docker compose logs -f"
