# Copilot Instructions for Trivia App

## Project Overview

This is a multi-tenant trivia application built for corporate training and team engagement. The application consists of:

- **Backend**: FastAPI (Python 3.11+) with PostgreSQL and Redis
- **Frontend**: React 18+ with TypeScript, Vite, and Tailwind CSS
- **Architecture**: Multi-tenant with row-level isolation via `organization_id`

### Current Implementation Status (Updated: February 2, 2026)

**✅ Implemented (Epic 1 Complete)**:
- Backend API with FastAPI (auth endpoints, user/org models)
- PostgreSQL database with Alembic migrations
- JWT authentication with refresh tokens
- pytest test suite with 80%+ coverage
- CI/CD workflows (Codacy, CodeQL)
- Comprehensive documentation

**⏳ Planned (Not Yet Implemented)**:
- WebSocket infrastructure (structure exists, no handlers)
- Redis Pub/Sub (Redis running, not used)
- Multi-tenant middleware (no automatic organization scoping yet)
- Frontend React components (structure exists, no components)
- Session management features
- Real-time scoring

**🔴 Critical Gaps to Address**:
1. Multi-tenant middleware missing (security risk - manual filtering required)
2. WebSocket handlers not implemented (required for Epic 3+)
3. Frontend CI/CD pipeline missing
4. CodeQL only scans GitHub Actions (not Python/TypeScript)

See `_bmad-output/implementation-artifacts/action-items-2026-02-02.md` for complete action items.

## Repository Structure

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
│   └── tests/           # Backend tests
├── frontend/            # React frontend
│   └── src/
│       ├── components/  # React components
│       ├── hooks/       # Custom hooks
│       ├── store/       # Zustand state management
│       ├── services/    # API services
│       ├── pages/       # Page components
│       └── types/       # TypeScript types
└── docs/                # Documentation
```

## Development Guidelines

### Backend (Python/FastAPI)

#### Code Style
- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Write docstrings for all modules, classes, and public functions
- Use async/await for I/O operations
- Format code with `black` before committing
- Lint code with `ruff check .`

#### Database
- Always use Alembic for schema changes - NEVER modify models without creating migrations
- Include `organization_id` in all tenant-scoped tables for multi-tenant isolation
- Create indexes for frequently queried columns (especially foreign keys and organization_id)
- Use proper database constraints for data integrity

#### Security
- Never commit secrets or sensitive data to the repository
- Use environment variables for configuration
- JWT tokens should use httpOnly cookies for refresh tokens
- Password hashing uses bcrypt (12 rounds by default via passlib's `CryptContext` in `backend/core/security.py`)
- Always validate and sanitize user inputs using Pydantic schemas

#### Testing
- Write pytest tests for all new features
- Target 80%+ test coverage
- Run tests with: `cd backend && pytest`
- Run with coverage: `pytest --cov=backend --cov-report=html`
- Tests should be independent and use fixtures from conftest.py

#### API Standards
- All endpoints must be under `/api/v1/` prefix
- Success responses: Return Pydantic schemas directly (no wrapper)
- Error responses: `{"error": {"code": "ERROR_CODE", "message": "description"}}`
- Use proper HTTP status codes (200, 201, 400, 401, 403, 404, 500)

### Frontend (React/TypeScript)

#### Code Style
- Use TypeScript strict mode - avoid `any` types
- Use functional components with hooks
- One component per file with PascalCase naming
- Use camelCase for functions and variables
- Format with Prettier and lint with ESLint
- Run linter: `npm run lint`

#### State Management
- Use Zustand for global application state
- Use TanStack Query for server state
- Keep state minimal and derived data computed

#### Components
- Create reusable, composable components
- Props should have explicit TypeScript interfaces
- Use Tailwind CSS utility classes for styling
- Follow existing component patterns in the codebase

#### Testing
- Write tests using Vitest and React Testing Library
- Test user interactions and component behavior
- Run tests: `npm test`
- Coverage: `npm run test:coverage`

### Multi-Tenancy

**CRITICAL**: This application uses row-level multi-tenancy:
- All tenant-scoped database queries MUST filter by `organization_id`
- Never expose data across organizational boundaries
- Always validate organization access in endpoints
- Test multi-tenant isolation thoroughly

### Git Workflow

#### Branch Naming
- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation
- `test/description` - Tests only
- `refactor/description` - Code refactoring

#### Commit Messages
Write clear, descriptive commit messages:
```
Brief summary (50 chars or less)

- Detailed explanation with bullet points
- What changed and why
- Reference related issues

Resolves #123
```

### Running the Application

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
alembic upgrade head
python main.py
```
Backend runs at: http://localhost:8000
API docs: http://localhost:8000/docs

#### Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at: http://localhost:5173

#### Infrastructure
```bash
docker-compose up -d  # Starts PostgreSQL and Redis
```

### Testing Commands

**Backend:**
```bash
cd backend
pytest                                    # Run all tests
pytest tests/api/test_auth.py           # Run specific file
pytest --cov=backend --cov-report=html  # With coverage
```

**Frontend:**
```bash
cd frontend
npm test                 # Run all tests
npm run test:coverage    # With coverage
```

### Code Quality

**Backend:**
```bash
cd backend
black .                  # Format code
ruff check .            # Lint code
```

**Frontend:**
```bash
cd frontend
npm run lint            # Lint code
```

### CI/CD Workflows

**Active Workflows**:
1. **Codacy**: Code quality, security scanning, test coverage (runs on PRs, main pushes, weekly)
2. **CodeQL**: Security vulnerability detection (runs on PRs, main pushes, weekly)
3. **Greetings**: Welcome messages for first-time contributors
4. **Summary**: AI-powered issue summarization

**Important Notes**:
- External contributors don't need to set up secrets
- Maintainers need `CODACY_PROJECT_TOKEN` for coverage uploads
- Tests run automatically on all PRs
- See `docs/CI_CD.md` for detailed workflow documentation

**Known Issues**:
- Duplicate test runs (Codacy + CodeQL both run tests)
- No frontend CI pipeline yet
- CodeQL only scans GitHub Actions files (Python/TypeScript config needed)

**Running CI Checks Locally**:
```bash
# Backend (same as CI)
cd backend
PYTHONPATH=.. pytest --cov=backend --cov-report=term-missing

# Linting
black --check .
ruff check .
mypy backend/
```

## Common Tasks

### Adding a New API Endpoint

1. Define Pydantic schemas in `backend/schemas/`
2. Create database models in `backend/models/` if needed
3. Create migration: `alembic revision --autogenerate -m "description"`
4. Add CRUD operations in `backend/db/crud/`
5. Implement business logic in `backend/services/`
6. Create endpoint in `backend/api/v1/endpoints/`
7. Write tests in `backend/tests/`
8. Update API documentation if needed

### Creating a Database Migration

```bash
cd backend
alembic revision --autogenerate -m "Add user profile fields"
alembic upgrade head
```

### Adding a New React Component

1. Create component file in `frontend/src/components/`
2. Define TypeScript interfaces for props
3. Implement component using functional syntax
4. Add tests in co-located `.test.tsx` file
5. Export from index file if creating reusable component

## Architecture Patterns

### Backend Patterns
- **Dependency Injection**: Use FastAPI's `Depends()` for dependencies
- **Repository Pattern**: CRUD operations in `db/crud/`
- **Service Layer**: Business logic in `services/`
- **Schema Validation**: Pydantic schemas for all I/O

### Frontend Patterns
- **Custom Hooks**: Reusable logic in `hooks/`
- **API Layer**: Centralized API calls in `services/`
- **Type Safety**: TypeScript interfaces in `types/`

## Environment Variables

Required environment variables (see `.env.example`):
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string  
- `SECRET_KEY` - JWT secret (generate with `openssl rand -hex 32`)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration
- `CORS_ORIGINS` - Allowed CORS origins

## Documentation

- Project README: `/README.md`
- Contributing Guide: `/CONTRIBUTING.md`
- Architecture Doc: `/_bmad-output/implementation-artifacts/architecture.md`
- PRD: `/_bmad-output/implementation-artifacts/TRIVIA_APP_PRD.md`
- Validation Reports: `/docs/validation/`

## Important Notes

### What NOT to Do
- ❌ Don't modify database schema without Alembic migrations
- ❌ Don't commit `.env` files or secrets
- ❌ Don't use `any` type in TypeScript
- ❌ Don't skip writing tests for new features
- ❌ Don't expose data across organizational boundaries
- ❌ Don't hardcode configuration values

### Best Practices
- ✅ Write descriptive commit messages
- ✅ Run tests before submitting changes
- ✅ Keep functions small and focused
- ✅ Use meaningful variable names
- ✅ Document complex logic with comments
- ✅ Follow existing code patterns
- ✅ Update documentation when changing APIs

## Getting Help

- Review existing code for patterns and examples
- Check documentation in `/docs/` directory
- Review validation reports for architectural guidance
- See `CONTRIBUTING.md` for detailed guidelines
- API documentation available at http://localhost:8000/docs when backend is running
