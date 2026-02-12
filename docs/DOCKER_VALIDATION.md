# Docker Setup Validation Checklist

This checklist helps verify the Docker Compose setup is working correctly.

## Pre-Flight Checks

- [ ] Docker is installed: `docker --version`
- [ ] Docker Compose is installed: `docker compose version`
- [ ] Docker daemon is running: `docker ps`
- [ ] Ports are available (8000, 5173, 5432, 6379)

## Configuration Validation

```bash
# Validate docker-compose.yml syntax
docker compose config

# List all services
docker compose config --services
# Expected output: postgres, redis, backend, frontend
```

## Build Verification

```bash
# Build all images (may take 5-10 minutes first time)
docker compose build

# Expected: No errors, images built successfully
```

## Startup Validation

```bash
# Start all services
docker compose up -d

# Check all containers are running
docker compose ps
# Expected: All services with state "Up" or "Up (healthy)"
```

## Service Health Checks

### PostgreSQL
```bash
# Should return "postgres is ready"
docker compose exec postgres pg_isready -U trivia_user -d trivia_db

# Alternative: Check from host
docker compose exec postgres psql -U trivia_user -d trivia_db -c "\dt"
```

### Redis
```bash
# Should return "PONG"
docker compose exec redis redis-cli ping
```

### Backend
```bash
# Check logs for successful startup
docker compose logs backend | grep "Application startup complete"

# Test health endpoint
curl http://localhost:8000/health
# Expected: {"status":"healthy","app":"trivia-app"}

# Test API documentation
curl -I http://localhost:8000/docs
# Expected: HTTP/1.1 200 OK
```

### Frontend
```bash
# Check logs for Vite server startup
docker compose logs frontend | grep "Local:"

# Test frontend is accessible
curl -I http://localhost:5173
# Expected: HTTP/1.1 200 OK
```

## Database Migration Validation

```bash
# Check migration logs in backend startup
docker compose logs backend | grep "Running database migrations"
docker compose logs backend | grep "Migrations completed"

# Verify migrations were applied
docker compose exec backend alembic current
# Should show current migration hash

# List all migrations
docker compose exec backend alembic history
```

## Hot Reload Validation

### Backend Hot Reload
```bash
# 1. Modify a backend file (e.g., add a comment to backend/main.py)
echo "# Test change" >> backend/main.py

# 2. Watch logs for reload message
docker compose logs -f backend
# Expected: "Reloading..." message within 2-3 seconds

# 3. Revert change
git checkout backend/main.py
```

### Frontend Hot Reload
```bash
# 1. Modify a frontend file
echo "// Test change" >> frontend/src/App.tsx

# 2. Check browser or logs for HMR update
docker compose logs -f frontend
# Expected: HMR update message

# 3. Revert change
git checkout frontend/src/App.tsx
```

## Volume Mounting Validation

```bash
# Backend: Verify source code is mounted
docker compose exec backend ls -la /app | head -10
# Expected: backend/, alembic/, main.py, requirements.txt, etc.

# Frontend: Verify source code is mounted
docker compose exec frontend ls -la /app | head -10
# Expected: src/, package.json, node_modules/, etc.

# Frontend: Verify node_modules is in container (not from host)
docker compose exec frontend ls -la /app/node_modules | wc -l
# Expected: > 100 (many packages)
```

## Network Connectivity

```bash
# Backend can reach PostgreSQL
docker compose exec backend pg_isready -h postgres -U trivia_user

# Backend can reach Redis
docker compose exec backend redis-cli -h redis ping

# Frontend can reach Backend (from container)
docker compose exec frontend wget -O- http://backend:8000/health 2>/dev/null
```

## Performance & Resource Usage

```bash
# Check resource usage
docker stats --no-stream

# Expected reasonable values:
# - postgres: < 100MB RAM
# - redis: < 50MB RAM
# - backend: < 200MB RAM
# - frontend: < 500MB RAM (Node + Vite)
```

## Cleanup & Restart

```bash
# Stop all services
docker compose down

# Clean restart
docker compose down -v
docker compose up -d

# Verify everything starts successfully again
docker compose ps
```

## Common Issues to Check

### Issue: Containers exit immediately
```bash
# Check container logs for errors
docker compose logs backend
docker compose logs frontend

# Common causes:
# - Missing dependencies in requirements.txt or package.json
# - Syntax errors in code
# - Port conflicts
# - Permission issues with entrypoint script
```

### Issue: Database connection fails
```bash
# Verify PostgreSQL is healthy
docker compose ps postgres
# State should be "Up (healthy)"

# Check PostgreSQL logs
docker compose logs postgres | tail -50

# Test connection
docker compose exec postgres psql -U trivia_user -d trivia_db -c "SELECT 1;"
```

### Issue: Migrations don't run
```bash
# Check backend logs during startup
docker compose logs backend | grep -A 10 "Running database migrations"

# Manually run migrations
docker compose exec backend alembic upgrade head

# Check for migration errors
docker compose exec backend alembic current
```

### Issue: Hot reload doesn't work
```bash
# For backend:
# 1. Check uvicorn is running with --reload flag
docker compose logs backend | grep "reload"

# 2. Verify volume mount
docker compose exec backend pwd
# Should be: /app

# For frontend:
# 1. Check Vite dev server is running
docker compose logs frontend | grep "dev server running"

# 2. On Windows/Mac, ensure file sharing is enabled in Docker Desktop
```

## Validation Script

Create a script to automate validation:

```bash
#!/bin/bash
# validate-docker-setup.sh

set -e

echo "🔍 Validating Docker setup..."

# Check Docker
docker --version || { echo "❌ Docker not found"; exit 1; }
docker compose version || { echo "❌ Docker Compose not found"; exit 1; }

# Validate config
echo "✓ Validating docker-compose.yml..."
docker compose config > /dev/null || { echo "❌ Invalid docker-compose.yml"; exit 1; }

# Build images
echo "✓ Building images..."
docker compose build --quiet

# Start services
echo "✓ Starting services..."
docker compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
# Note: Using fixed sleep for simplicity. For production, use health check polling.
sleep 30

# Check health
echo "✓ Checking PostgreSQL..."
docker compose exec -T postgres pg_isready -U trivia_user -d trivia_db

echo "✓ Checking Redis..."
docker compose exec -T redis redis-cli ping

echo "✓ Checking Backend..."
curl -f http://localhost:8000/health

echo "✓ Checking Frontend..."
curl -f -I http://localhost:5173

echo "✅ All validations passed!"
echo ""
echo "Access the application:"
echo "  Frontend: http://localhost:5173"
echo "  Backend: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
```

## Success Criteria

The Docker setup is working correctly when:

✅ All containers start and stay running
✅ All health checks pass
✅ Database migrations run automatically on backend startup
✅ Backend API is accessible at http://localhost:8000
✅ Frontend is accessible at http://localhost:5173
✅ Hot reload works for both backend and frontend code changes
✅ Services can restart without errors
✅ Logs show no critical errors

## Next Steps After Validation

1. Stop services: `docker compose down`
2. Read [Docker Development Guide](DOCKER_GUIDE.md) for detailed usage
3. Configure custom settings in `docker-compose.override.yml` if needed
4. Start developing!

## Troubleshooting

If validation fails, see:
- [Docker Development Guide - Troubleshooting](DOCKER_GUIDE.md#troubleshooting)
- [README - Docker-Specific Issues](../README.md#docker-specific-issues)
