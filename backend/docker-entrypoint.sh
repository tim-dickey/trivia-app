#!/bin/bash
# Entrypoint script for backend Docker container
# Runs database migrations before starting the application

set -e

echo "==================================="
echo "Starting Trivia App Backend..."
echo "==================================="

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h postgres -U trivia_user -d trivia_db; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done
echo "PostgreSQL is ready!"

# Run database migrations
echo "Running database migrations..."
alembic upgrade head
echo "Migrations completed!"

# Start the application
echo "Starting FastAPI application..."
exec uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
