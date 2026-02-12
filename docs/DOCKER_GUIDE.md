# Docker Development Guide

This guide covers the Docker-based development setup for the Trivia App.

## Overview

The Docker Compose setup provides a complete development environment with:
- **PostgreSQL 13**: Database with automatic migrations
- **Redis 7**: Cache and pub/sub for real-time features
- **Backend (FastAPI)**: Python 3.11 with hot reload
- **Frontend (React)**: Node 20 with Vite and hot reload

## Quick Start

```bash
# Start all services
docker compose up

# Start in background (detached mode)
docker compose up -d

# View logs
docker compose logs -f

# Stop all services
docker compose down
```

## Service Details

### Backend Service

**Container**: `trivia-backend`
**Port**: 8000
**Features**:
- Automatic database migrations on startup
- Hot reload enabled (uvicorn --reload)
- Volume-mounted source code
- Health checks every 30 seconds

**Key Files**:
- `backend/Dockerfile.dev`: Container definition
- `backend/docker-entrypoint.sh`: Startup script with migrations
- `backend/.dockerignore`: Excluded files during build

**Accessing**:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

### Frontend Service

**Container**: `trivia-frontend`
**Port**: 5173
**Features**:
- Vite dev server with hot module replacement (HMR)
- Volume-mounted source code
- Node modules in persistent volume

**Key Files**:
- `frontend/Dockerfile.dev`: Container definition
- `frontend/.dockerignore`: Excluded files during build

**Accessing**:
- Frontend: http://localhost:5173

### Infrastructure Services

**PostgreSQL**:
- Container: `trivia-postgres`
- Port: 5432
- Credentials: trivia_user / trivia_pass
- Database: trivia_db
- Data persistence via Docker volume

**Redis**:
- Container: `trivia-redis`
- Port: 6379
- Data persistence via Docker volume

## Common Commands

### Starting and Stopping

```bash
# Start all services
docker compose up

# Start specific service
docker compose up backend

# Start in background
docker compose up -d

# Stop all services (keeps containers)
docker compose stop

# Stop and remove containers
docker compose down

# Stop and remove containers + volumes (clean slate)
docker compose down -v
```

### Viewing Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend

# Last 100 lines
docker compose logs --tail=100 backend
```

### Building and Rebuilding

```bash
# Build all images
docker compose build

# Build specific service
docker compose build backend

# Build without cache (clean build)
docker compose build --no-cache

# Rebuild and restart
docker compose up --build
```

### Running Commands in Containers

```bash
# Open shell in backend container
docker compose exec backend bash

# Open shell in frontend container
docker compose exec frontend sh

# Run backend tests
docker compose exec backend pytest

# Run database migrations manually
docker compose exec backend alembic upgrade head

# Check Python version
docker compose exec backend python --version

# Run npm commands
docker compose exec frontend npm run lint
```

### Container Management

```bash
# List running containers
docker compose ps

# List all containers (including stopped)
docker compose ps -a

# Restart a service
docker compose restart backend

# Stop a service
docker compose stop frontend

# Start a stopped service
docker compose start frontend

# Remove a stopped service container
docker compose rm frontend
```

### Debugging

```bash
# Check service status
docker compose ps

# View detailed logs
docker compose logs --tail=100 backend

# Check container resource usage
docker stats

# Inspect a service configuration
docker compose config

# Check backend health endpoint
curl http://localhost:8000/health
```

## Development Workflow

### Making Backend Changes

1. Edit files in `backend/` directory
2. Uvicorn automatically reloads on file changes
3. View logs: `docker compose logs -f backend`
4. If imports change, restart: `docker compose restart backend`

### Making Frontend Changes

1. Edit files in `frontend/src/` directory
2. Vite HMR updates the browser automatically
3. View logs: `docker compose logs -f frontend`
4. If package.json changes: `docker compose restart frontend`

### Database Migrations

**Creating a new migration**:
```bash
# Enter backend container
docker compose exec backend bash

# Create migration
alembic revision --autogenerate -m "Add new table"

# Exit container
exit

# Migration file is now in backend/alembic/versions/
```

**Applying migrations**:
- Automatic on container startup (via docker-entrypoint.sh)
- Manual: `docker compose exec backend alembic upgrade head`

### Adding Dependencies

**Backend (Python)**:
```bash
# 1. Add package to backend/requirements.txt
echo "new-package==1.0.0" >> backend/requirements.txt

# 2. Rebuild container
docker compose build backend

# 3. Restart service
docker compose up -d backend
```

**Frontend (Node)**:
```bash
# 1. Add package via npm in container
docker compose exec frontend npm install new-package

# 2. The change will be reflected in package.json (mounted volume)

# 3. Rebuild for clean state (optional)
docker compose build frontend
```

## Customization

You can customize the Docker setup for your local environment:

1. Copy the example override file:
   ```bash
   cp docker-compose.override.yml.example docker-compose.override.yml
   ```

2. Edit `docker-compose.override.yml` to change ports, add services, etc.

3. Your changes will be automatically applied (file is gitignored)

## Performance Tips

### macOS/Windows Performance

Docker on macOS/Windows can be slower due to file system mounting:

1. **Reduce mounted files**: Keep node_modules in container volume
   ```yaml
   volumes:
     - ./frontend:/app
     - /app/node_modules  # Don't sync node_modules
   ```

2. **Enable file sharing**: Docker Desktop → Settings → Resources → File Sharing

3. **Allocate more resources**: Docker Desktop → Settings → Resources
   - CPUs: 4+
   - Memory: 4GB+

### Linux Performance

Docker on Linux has near-native performance:
- No special configuration needed
- File watching works out of the box

## Troubleshooting

See [README.md - Docker-Specific Issues](README.md#docker-specific-issues) for common problems and solutions.

### Quick Fixes

**Reset everything**:
```bash
docker compose down -v
docker system prune -f
docker compose up --build
```

**Check service health**:
```bash
docker compose ps
docker compose logs backend | grep -i error
curl http://localhost:8000/health
```

**Rebuild from scratch**:
```bash
docker compose build --no-cache
docker compose up
```

## Production vs Development

The current setup is for **development only**:

❌ **Do NOT use in production**:
- Uses dev Docker images
- Debug mode enabled
- Default credentials
- No SSL/TLS
- Hot reload overhead

✅ **For production**, create:
- `backend/Dockerfile` (not .dev)
- `frontend/Dockerfile` (multi-stage build)
- `docker-compose.prod.yml`
- Proper secrets management
- SSL/TLS certificates
- Health checks and monitoring

## Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI in Docker](https://fastapi.tiangolo.com/deployment/docker/)
- [Vite Docker Guide](https://vitejs.dev/guide/static-deploy.html)
- [PostgreSQL Docker Hub](https://hub.docker.com/_/postgres)
- [Redis Docker Hub](https://hub.docker.com/_/redis)
