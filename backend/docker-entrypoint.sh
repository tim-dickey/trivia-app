#!/bin/bash
# Entrypoint script for backend Docker container
# Runs database migrations before starting the application

set -e

echo "==================================="
echo "Starting Trivia App Backend..."
echo "==================================="

# Extract database connection details from DATABASE_URL or use defaults
DB_HOST="${PGHOST:-postgres}"
DB_USER="${PGUSER:-trivia_user}"
DB_NAME="${PGDATABASE:-trivia_db}"

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME"; do
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
