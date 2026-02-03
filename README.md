# Trivia App

A multi-tenant trivia application for corporate training and team engagement.

> 📍 **New to the project?** See [FILE_LOCATIONS.md](FILE_LOCATIONS.md) for a complete guide to finding files in the repository.

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
- **Real-Time**: WebSocket infrastructure for live updates
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
- Docker & Docker Compose (PostgreSQL 13+, Redis 7+)
- Git
- OpenSSL (for JWT secret generation)

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

# Copy environment file and configure
cp ../.env.example .env

# IMPORTANT: Generate secure JWT secret
# Run this command and add the output to your .env file:
# openssl rand -hex 32

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
PYTHONPATH=.. pytest
PYTHONPATH=.. pytest --cov=backend --cov-report=html

# Run WebSocket integration tests
PYTHONPATH=.. pytest tests/integration/test_websocket.py -v

# Run all integration tests
PYTHONPATH=.. pytest tests/integration/ -v
```

Alternatively, run from project root:
```bash
pytest backend/tests --cov=backend --cov-report=html
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

**Current Sprint**: Epic 1 - Platform Foundation & Authentication

### ✅ Completed Stories (As of February 2, 2026)
- ✅ **Story 1.1**: Project Initialization & Development Environment Setup (9/9 ACs met)
- ✅ **Story 1.2**: Organization & User Data Models (9/9 ACs met)
- ✅ **Story 1.3**: User Registration with Email (10/10 ACs met - backend with tests)

**Recent Updates (PR #21 - Feb 2, 2026)**:
- ✅ Comprehensive CI/CD workflows (Codacy, CodeQL, dependency review)
- ✅ Authentication endpoints fully implemented with JWT
- ✅ Comprehensive test suite (pytest with 80%+ coverage)
- ✅ Code quality tooling (Codacy CLI, linting configurations)
- ✅ BMAD agent framework integration (23 custom agents)
- ✅ Complete documentation suite (README, CONTRIBUTING, architecture docs)
- ✅ **Multi-tenant middleware** (organization scoping, security isolation)

**Recent Updates (PR #29 - Feb 3, 2026)**:
- ✅ **WebSocket Infrastructure** implemented for real-time features
  - Connection manager with session-based tracking
  - JWT authentication for WebSocket connections
  - Message broadcasting and session isolation
  - Frontend WebSocket service with auto-reconnection
  - 6 integration tests (100% pass rate)
  - Complete documentation in `docs/websocket-infrastructure.md`

**Validation Report**: See [`docs/validation/epic-1-validation-report.md`](docs/validation/epic-1-validation-report.md)

**Quality Metrics**:
- Acceptance Criteria: 28/28 (100%)
- Implementation Quality: 96.3%
- Architecture Compliance: 92%
- Test Coverage: 80%+ (backend)

### 🔄 In Progress
- 🔄 Story 1.4: User Login with JWT Authentication (implementation complete, needs frontend integration)
- 🔄 Story 1.5: Session Management & Token Refresh (ready for development)

### 📋 Upcoming Stories
- Story 1.6: Multi-Tenant Access Control
- Story 1.7: User Profile Management

### ⚠️ Known Technical Debt & Action Items

**Critical (Must Address Before Feature Work)**:
1. **CI/CD Optimization**: Consolidate duplicate test runs (Codacy + CodeQL both run tests on every PR)
2. ~~**Multi-Tenant Middleware**: Implement organization scoping middleware for automatic data isolation~~ ✅ **COMPLETED**
3. ~~**WebSocket Infrastructure**: Real-time features not yet implemented (required for Epic 3)~~ ✅ **COMPLETED** (PR #29)
4. **Frontend CI Pipeline**: No automated testing for frontend changes

**High Priority**:
5. Frontend components not yet implemented (placeholders exist)
6. CodeQL only scans GitHub Actions files (needs Python/TypeScript configuration)
7. Test database uses SQLite in CI vs PostgreSQL in production (potential compatibility issues)

**Medium Priority**:
8. Dependency updates available (FastAPI, Pydantic, React, Vite)
9. No seed data script for development organizations
10. Security headers middleware not implemented

See [`_bmad-output/implementation-artifacts/action-items-2026-02-02.md`](_bmad-output/implementation-artifacts/action-items-2026-02-02.md) for complete action items and [`_bmad-output/implementation-artifacts/code-review-2026-02-02.md`](_bmad-output/implementation-artifacts/code-review-2026-02-02.md) for detailed code review findings.

## CI/CD Workflows

The project uses GitHub Actions for continuous integration and code quality. Current workflows:

### Active Workflows

**Codacy Workflow** (`.github/workflows/codacy.yml`)
- **Triggers**: Pull requests, pushes to main, weekly schedule (Thursday 5:33 PM UTC)
- **Purpose**: Code quality analysis, security scanning, test coverage
- **What it does**:
  - Runs backend tests with pytest
  - Generates coverage reports (XML format)
  - Uploads coverage to Codacy
  - Runs Codacy CLI security analysis
- **Requirements**: `CODACY_PROJECT_TOKEN` secret (for external contributors, maintainers will handle this)

**CodeQL Workflow** (`.github/workflows/codeql.yml`)
- **Triggers**: Pull requests, pushes to main, weekly schedule (Saturday 11:21 AM UTC)
- **Purpose**: Security vulnerability scanning
- **What it does**:
  - Analyzes GitHub Actions files for security issues
  - Uploads results to GitHub Security tab
- **Note**: Currently only analyzes GitHub Actions. Python/TypeScript analysis to be added.

**Other Workflows**:
- **Greetings**: Welcomes new contributors on their first issue/PR
- **Summary**: AI-powered issue summarization
- **Dependency Review** (disabled): Planned for dependency vulnerability scanning

### Known CI/CD Issues

⚠️ **Duplicate Test Runs**: Both Codacy and CodeQL workflows run tests, causing redundancy. See action items for consolidation plan.

⚠️ **No Frontend CI**: Frontend tests are not currently run in CI. This is planned for implementation.

## Architecture

- **Multi-tenancy**: Row-level isolation via `organization_id`
- **Authentication**: JWT access tokens (15min) + refresh tokens (7 days)
- **Real-time**: WebSocket + Redis Pub/Sub (planned, not yet implemented)
- **API Response Format**: 
  - Success: `{data: {...}}`
  - Error: `{error: {code, message}}`

### Current Implementation Status
- ✅ Backend API with FastAPI
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ JWT authentication with refresh tokens
- ✅ Multi-tenant data models
- ✅ Alembic migrations
- ✅ pytest test infrastructure
- ⏳ WebSocket handlers (structure exists, not implemented)
- ⏳ Redis Pub/Sub (infrastructure ready, not used yet)
- ⏳ Frontend React app (structure exists, components not implemented)

## Environment Variables

See `.env.example` for required environment variables.

**⚠️ SECURITY CRITICAL**: Before running in any environment:
1. Generate a secure JWT secret:
   ```bash
   openssl rand -hex 32
   ```
2. Add the generated secret to your `.env` file:
   ```
   SECRET_KEY=your-generated-secret-here
   ```
3. Never commit `.env` to version control

## API Documentation

Once the backend is running, access interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Available Endpoints (Epic 1)
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login (returns JWT access token)
- `POST /api/v1/auth/logout` - User logout (clears refresh token)

## Validation & Quality Assurance

The project undergoes architectural validation at each epic milestone. Current validation status:

**Epic 1 (Stories 1.1-1.3)**: ✅ **APPROVED** - 96.3% Quality Score

Key achievements:
- ✅ Multi-tenant row-level isolation implemented correctly
- ✅ Security-first authentication (bcrypt 12 rounds, httpOnly cookies)
- ✅ Clean architecture with proper separation of concerns
- ✅ Comprehensive Pydantic validation schemas
- ✅ Production-ready database design with migrations

See [`docs/validation/epic-1-validation-report.md`](docs/validation/epic-1-validation-report.md) for detailed analysis.

## Troubleshooting

### Common Issues

#### Database Connection Errors

**Problem**: `FATAL: database "trivia_db" does not exist` or connection refused errors

**Solutions**:
1. Ensure Docker containers are running:
   ```bash
   docker-compose ps
   ```
2. If containers aren't running:
   ```bash
   docker-compose up -d
   ```
3. Check PostgreSQL logs:
   ```bash
   docker-compose logs postgres
   ```
4. Verify database connection settings in `.env`:
   ```
   DATABASE_URL=postgresql://trivia_user:trivia_pass@localhost:5432/trivia_db
   ```

#### Alembic Migration Errors

**Problem**: `Target database is not up to date` or migration conflicts

**Solutions**:
1. Check current migration status:
   ```bash
   cd backend
   alembic current
   alembic history
   ```
2. Reset to head:
   ```bash
   alembic upgrade head
   ```
3. If corrupted, drop and recreate database:
   ```bash
   docker-compose down -v
   docker-compose up -d
   alembic upgrade head
   ```

#### Test Failures

**Problem**: Tests fail with import errors or database issues

**Solutions**:
1. Ensure PYTHONPATH is set when running tests:
   ```bash
   # From backend directory
   PYTHONPATH=.. pytest
   
   # Or from project root
   pytest backend/tests
   ```
2. Check pytest.ini configuration is present in backend/
3. Verify test database is configured (uses SQLite automatically)
4. Clear pytest cache if needed:
   ```bash
   rm -rf .pytest_cache __pycache__
   ```

#### JWT Token Issues

**Problem**: 401 Unauthorized errors or token validation failures

**Solutions**:
1. Ensure SECRET_KEY is set in `.env` and is at least 32 characters
2. Generate a secure key:
   ```bash
   openssl rand -hex 32
   ```
3. Restart the backend server after changing SECRET_KEY
4. Check token expiration (access tokens expire after 15 minutes)

#### Port Already in Use

**Problem**: `Address already in use` when starting services

**Solutions**:
1. Check what's using the port:
   ```bash
   # For backend (port 8000)
   lsof -i :8000
   
   # For frontend (port 5173)
   lsof -i :5173
   
   # For PostgreSQL (port 5432)
   lsof -i :5432
   ```
2. Kill the process or use a different port:
   ```bash
   # Kill process by PID
   kill -9 <PID>
   
   # Or change port in .env or vite.config.ts
   ```

#### Frontend Dependencies Issues

**Problem**: `npm install` fails or module not found errors

**Solutions**:
1. Clear npm cache:
   ```bash
   cd frontend
   rm -rf node_modules package-lock.json
   npm cache clean --force
   npm install
   ```
2. Ensure Node.js version is 18+:
   ```bash
   node --version
   ```
3. Try using npm instead of yarn or vice versa

#### CI/CD Workflow Failures

**Problem**: GitHub Actions workflows fail

**Common Issues**:
1. **Missing secrets**: Some workflows use `CODACY_PROJECT_TOKEN` for coverage uploads
   - For external contributors: **This is normal** – workflows treat `CODACY_PROJECT_TOKEN` as optional and skip coverage upload steps gracefully
   - For maintainers: `CODACY_PROJECT_TOKEN` is optional for PR CI but recommended if you want coverage reports uploaded from main/default-branch runs. See [CI/CD Setup in CONTRIBUTING.md](CONTRIBUTING.md#for-maintainers-github-secrets-setup) for setup details.
2. **Test failures**: Check workflow logs for specific test errors
3. **Coverage below 80%**: Add more tests to meet the coverage threshold
4. **Linting/style issues (Codacy or local checks)**: The main PR CI workflow runs backend tests and coverage only, but Codacy and local tools may report style problems. Run `ruff check .` and `black .` locally to fix these before pushing.

**For detailed CI/CD documentation and local testing instructions**, see the [CI/CD section in CONTRIBUTING.md](CONTRIBUTING.md#-cicd-and-github-actions).

### Getting Additional Help

If you encounter issues not covered here:
1. Check existing [GitHub Issues](https://github.com/tim-dickey/trivia-app/issues)
2. Review documentation in `docs/` directory
3. Check validation reports for architectural guidance
4. Open a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Error messages/logs
   - Environment details (OS, Python version, Node version)

## Contributing

We welcome contributions from the development community! This is an **open source project** aimed at helping organizations create engaging learning experiences through gamified trivia.

**📖 For complete contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md)**

**🔧 For CI/CD setup and running tests locally, see [CI/CD Setup in CONTRIBUTING.md](CONTRIBUTING.md#-cicd-and-github-actions)**

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch** from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Follow existing code structure and conventions**
   - Backend: Follow FastAPI patterns, use type hints, maintain 80%+ test coverage
   - Frontend: Follow React best practices, use TypeScript
   - Write descriptive commit messages
4. **Write tests for new features**
   - Backend: pytest with comprehensive test cases
   - Frontend: Vitest + React Testing Library
5. **Ensure all tests pass**
   ```bash
   # Backend (from project root)
   pytest backend/tests
   
   # Or from backend directory
   cd backend && PYTHONPATH=.. pytest
   
   # Frontend
   cd frontend && npm test
   ```
6. **Update documentation** as needed
7. **Submit a pull request** with a clear description of changes

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Focus on what is best for the community

### Areas for Contribution

- 🐛 **Bug Fixes**: Help resolve issues and improve stability
- ✨ **New Features**: Implement features from the roadmap
- 📝 **Documentation**: Improve guides, API docs, and examples
- 🧪 **Testing**: Increase test coverage and quality
- ♿ **Accessibility**: Enhance WCAG compliance and usability
- 🌐 **Internationalization**: Add i18n support and translations
- 🎨 **UX/UI**: Design and implementation improvements
- 🚀 **Performance**: Optimization and scalability enhancements

### Getting Help

- Review existing issues and pull requests
- Check documentation in `docs/` directory
- Review validation reports for architectural guidance
- Open an issue for questions or discussions

## Development Roadmap

### Phase 1: MVP (Month 1-3)
- **Epic 1**: Platform Foundation & Authentication ← *Current*
- **Epic 2**: Session Creation & Management
- **Epic 3**: Live Trivia Gameplay & Real-Time Scoring
- **Epic 4**: Educational Feedback & Knowledge Assessment
- **Epic 5**: Chat Platform Integration

### Phase 2: Market Fit Validation (Month 4-6)
- Epic 6: Advanced Engagement Mechanics
- Epic 7: Flexible Participation Modes
- Epic 8: Enterprise Features & AI Customization

### Phase 3: Scale & Expansion (Month 7+)
- Epic 9: New Hire Onboarding Specialization

See [`_bmad-output/planning-artifacts/epics.md`](_bmad-output/planning-artifacts/epics.md) for complete epic breakdown.

## Support & Documentation

- **📍 File Locations Guide**: `FILE_LOCATIONS.md` - Complete index of all files
- **Architecture Document**: `_bmad-output/implementation-artifacts/architecture.md`
- **CI/CD Workflows**: `docs/CI_CD.md` - Complete workflow documentation
- **🔒 Multi-Tenancy Guide**: `docs/MULTI_TENANCY.md` - Organization scoping and security
- **PRD**: `_bmad-output/implementation-artifacts/TRIVIA_APP_PRD.md`
- **UX Specifications**: `_bmad-output/implementation-artifacts/UI_UX_SPECIFICATIONS.md`
- **QA Test Strategy**: `_bmad-output/implementation-artifacts/QA_TEST_STRATEGY.md`
- **Dev Implementation Record**: `_bmad-output/implementation-artifacts/dev-agent-record.md`
- **Validation Reports**: `docs/validation/`

## License

This project is licensed under the **MIT License** - see the [`LICENSE`](LICENSE) file for full details.

### MIT License Summary

✅ **Permissions**:
- ✓ Commercial use
- ✓ Modification
- ✓ Distribution
- ✓ Private use

⚠️ **Conditions**:
- License and copyright notice must be included

❌ **Limitations**:
- No warranty
- No liability

Copyright (c) 2026 trivia-app Contributors

---

**Built with ❤️ by the open source community for learning and development teams everywhere**
