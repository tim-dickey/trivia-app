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

**Current Sprint**: Epic 1 - Platform Foundation & Authentication

### ✅ Completed Stories (Validated 2026-01-26)
- ✅ **Story 1.1**: Project Initialization & Development Environment Setup (9/9 ACs met)
- ✅ **Story 1.2**: Organization & User Data Models (9/9 ACs met)
- ✅ **Story 1.3**: User Registration with Email (10/10 ACs met - backend)

**Validation Report**: See [`docs/validation/epic-1-validation-report.md`](docs/validation/epic-1-validation-report.md)

**Quality Metrics**:
- Acceptance Criteria: 28/28 (100%)
- Implementation Quality: 96.3%
- Architecture Compliance: 92%

### 🔄 In Progress
- 🔄 Story 1.3: Frontend implementation + tests
- 🔄 Story 1.4: User Login with JWT Authentication (50% complete)

### 📋 Upcoming Stories
- Story 1.5: Session Management & Token Refresh
- Story 1.6: Multi-Tenant Access Control
- Story 1.7: User Profile Management

### ⚠️ Known Technical Debt
**Critical (Must Address Before Story 1.4)**:
1. No unit tests implemented - test structure exists but no test cases written
2. Placeholder JWT secret key - needs secure generation (see setup instructions)

**High Priority**:
3. Frontend components not yet implemented
4. No seed data script for development organizations
5. `verify_org_access()` dependency not implemented

See validation report for complete technical debt analysis.

## Architecture

- **Multi-tenancy**: Row-level isolation via `organization_id`
- **Authentication**: JWT access tokens (15min) + refresh tokens (7 days)
- **Real-time**: WebSocket + Redis Pub/Sub
- **API Response Format**: 
  - Success: `{data: {...}}`
  - Error: `{error: {code, message}}`

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

## Contributing

We welcome contributions from the development community! This is an **open source project** aimed at helping organizations create engaging learning experiences through gamified trivia.

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
   # Backend
   cd backend && pytest
   
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

- **Architecture Document**: `_bmad-output/implementation-artifacts/architecture.md`
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
