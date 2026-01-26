# Trivia App

A multi-tenant trivia application for corporate training and team engagement.

## Project Structure

```
trivia-app/
├── backend/              # FastAPI backend
│   ├── api/             # API endpoints
│   ├── core/            # Core configuration
│   ├── db/              # Database CRUD operations
│   ├── models/          # SQLAlchemy ORM models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   ├── websocket/       # WebSocket handlers
│   ├── integrations/    # External integrations
│   ├── tasks/           # Background tasks
│   ├── alembic/         # Database migrations
│   └── main.py          # Application entry point
├── frontend/            # React frontend
│   └── src/
│       ├── components/  # React components
│       ├── hooks/       # Custom hooks
│       ├── store/       # Zustand state management
│       ├── services/    # API services
│       ├── pages/       # Page components
│       ├── types/       # TypeScript types
│       ├── styles/      # CSS/styles
│       └── lib/         # Utilities
└── docker-compose.yml   # Local development services

```

## Tech Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Database**: PostgreSQL 13+
- **Cache/PubSub**: Redis 7+
- **ORM**: SQLAlchemy 2.0+
- **Migrations**: Alembic
- **Authentication**: JWT with refresh tokens
- **Testing**: pytest with 80%+ coverage target

### Frontend
- **Framework**: React 18+
- **Build Tool**: Vite
- **State Management**: Zustand
- **Server State**: TanStack Query
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Testing**: Vitest + React Testing Library

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd trivia-app
```

### 2. Start Infrastructure Services

```bash
docker-compose up -d
```

This starts PostgreSQL and Redis containers.

### 3. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp ../.env.example .env

# Initialize database with Alembic
alembic upgrade head

# Run development server
python main.py
```

Backend will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

### 4. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at: http://localhost:5173

## Development

### Running Tests

**Backend:**
```bash
cd backend
pytest
pytest --cov=backend --cov-report=html
```

**Frontend:**
```bash
cd frontend
npm test
npm run test:coverage
```

### Database Migrations

Create a new migration:
```bash
cd backend
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

### Code Quality

**Backend:**
```bash
ruff check .
black .
```

**Frontend:**
```bash
npm run lint
```

## Project Status

Current Sprint: Epic 1 - Platform Foundation & Authentication

### Completed Stories
- ✅ Story 1.1: Project Initialization & Development Environment Setup

### In Progress
- 🔄 Story 1.2: Organization & User Data Models
- 🔄 Story 1.3: User Registration with Email

## Architecture

- **Multi-tenancy**: Row-level isolation via `organization_id`
- **Authentication**: JWT access tokens (15min) + refresh tokens (7 days)
- **Real-time**: WebSocket + Redis Pub/Sub
- **API Response Format**: 
  - Success: `{data: {...}}`
  - Error: `{error: {code, message}}`

## Environment Variables

See `.env.example` for required environment variables.

## Contributing

1. Create feature branch from `main`
2. Follow existing code structure and conventions
3. Write tests for new features
4. Ensure all tests pass
5. Submit pull request

## License

[Your License Here]
