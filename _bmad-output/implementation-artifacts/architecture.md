---
stepsCompleted: [1, 2, 3, 4]
inputDocuments:
  - _bmad-output/implementation-artifacts/TRIVIA_APP_PRD.md
  - _bmad-output/implementation-artifacts/UI_UX_SPECIFICATIONS.md
  - _bmad-output/implementation-artifacts/QA_TEST_STRATEGY.md
workflowType: 'architecture'
project_name: 'trivia-app'
user_name: 'Tim_D'
date: '2026-01-19'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**
Trivia App provides a corporate training engagement platform with the following core capabilities:
- Real-time trivia sessions with team-based competition
- Multiple event types: opening energizers, knowledge assessments, coffee-break challenges, time-limited flash challenges
- Live scoring and immediate educational feedback
- Participation streaks and habit formation tracking
- Knowledge gap analysis with AI-powered recommendations
- Observer mode for low-pressure participation
- New hire onboarding specialized workflows
- Slack and Microsoft Teams bot integration for continuous engagement
- Session setup wizard with <2 minute deployment target
- Organization and team management with role-based access

**Non-Functional Requirements:**
- Performance: 99.5% uptime SLA, <500ms answer submission latency, <1s score updates, <2s mobile load time
- Scalability: Support 5000+ concurrent participants, stateless app servers, database connection pooling, Redis caching
- Security: HTTPS/TLS encryption, bcrypt password hashing, GDPR compliance, SOC 2 audit readiness
- Accessibility: WCAG 2.1 AA compliance, 48px touch targets, 4.5:1 color contrast, keyboard navigation
- Browser Support: Chrome, Safari, Firefox (latest 2 versions), mobile-first responsive design (320px-1920px)

**Scale & Complexity:**
- Primary domain: Full-stack web platform (React/Vue frontend, FastAPI backend, PostgreSQL + Redis)
- Complexity level: Medium-to-High (real-time systems, multi-tenancy, complex integrations)
- Estimated architectural components: 12-15 major subsystems (auth, session management, real-time scoring, analytics, integrations, etc.)
- Concurrent user load: 5000+ per event
- Multi-tenancy: Organization-based with team hierarchies

### Technical Constraints & Dependencies

**Technology Stack (Specified):**
- Backend: FastAPI (Python 3.10+), Celery for async tasks, Redis for caching and pub/sub
- Frontend: React or Vue.js, Tailwind CSS or Bootstrap, WebSocket client
- Database: PostgreSQL 13+, Redis cache layer
- Deployment: Docker, Kubernetes or managed container services (AWS ECS, Google Cloud Run)
- CI/CD: GitHub Actions or GitLab CI
- Third-party: Slack API, Microsoft Teams Bot Framework, optional Auth0/Okta for SSO

**External Dependencies:**
- Cloud infrastructure (AWS, GCP, or Azure)
- Slack/Teams API availability
- Optional: Video conferencing providers (Zoom, Teams)
- Optional: AI model providers (OpenAI, Anthropic, Azure OpenAI for enterprise tier)

### Cross-Cutting Concerns Identified

1. **Real-Time Data Flow**: WebSocket infrastructure must support live scoring, team updates, and feedback display with <1s latency across all connected participants
2. **Multi-Tenancy & Data Isolation**: Organization-based isolation required; session data, user data, and analytics must be properly scoped and secured
3. **AI Model Routing**: Enterprise feature requires flexible model selection routing based on subscription tier (free→Microsoft Copilot fixed, premium→org default fixed, enterprise→facilitator choice)
4. **Session State Management**: Complex state tracking across setup, active play, scoring, and completion phases with concurrent participant management
5. **Analytics & Reporting**: Real-time aggregation and persistence of session metrics, participation data, and knowledge tracking for analytics dashboards
6. **Integration Gateway**: Slack/Teams bots must maintain async communication while syncing with real-time session state
7. **Performance Under Load**: 5000+ concurrent participants demand efficient database queries, caching strategies, and async task processing

### Enterprise Features - AI Model Selection

The platform includes a new enterprise-tier feature for AI model customization:
- Facilitators at enterprise tier can select from approved AI models (including GPT-5.1-Codex-Max) per event
- Free/premium tiers locked to Microsoft Copilot or organization-selected default
- Organization admins can configure default models and whitelist approved options
- Custom AI provider integration (OpenAI, Anthropic, Azure OpenAI, etc.) with API credential management
- Model routing logic in API layer must transparently handle tier-based restrictions and fallback to Microsoft Copilot

## Starter Template Evaluation

### Primary Technology Domain

Full-Stack Web Platform: FastAPI backend with React frontend, PostgreSQL database, Redis caching, Docker containerization, and WebSocket real-time capabilities.

### Starter Options Considered

**Backend Starters:**
1. Full-Stack FastAPI + PostgreSQL (tiangolo/full-stack-fastapi-postgresql) - Official reference implementation, production-ready
2. Aegis Stack (lbedner/aegis-stack) - Modular CLI-based scaffolding for FastAPI projects
3. FastAPI Starter Boilerplate (MahmudJewel/fastapi-starter-boilerplate) - Professional project structure

**Frontend Starters:**
- Vite + React + TypeScript - Modern, lightweight, excellent WebSocket support
- Create React App - Established option, comprehensive tooling

### Selected Starter Approach: Full-Stack Integration Pattern

**Rationale:**
Given the real-time requirements (WebSocket scoring, live team updates), integration complexity (Slack/Teams bots, custom AI model routing), and scale requirements (5000+ concurrent participants), we recommend a **custom full-stack setup following tiangolo's patterns** rather than a single all-in-one starter.

This approach gives us:
- Battle-tested FastAPI backend patterns
- Proper separation of concerns
- Clear migration path from MVP to production
- Flexibility to customize for real-time WebSocket architecture

### Initialization Commands

**Backend (FastAPI + PostgreSQL + Redis):**

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install "fastapi[standard]" uvicorn[standard] celery redis psycopg[binary] pydantic-settings
```

**Frontend (React + Vite + TypeScript):**

```bash
npm create vite@latest trivia-app-frontend -- --template react-ts
cd trivia-app-frontend
npm install axios zustand @tanstack/react-query @tanstack/react-query-devtools tailwindcss postcss autoprefixer
npm install -D @tailwindcss/forms
```

**Infrastructure (Docker Compose for local development):**

```bash
# Create docker-compose.yml for PostgreSQL, Redis, and local development
```

### Architectural Decisions Provided by Starter Pattern

**Language & Runtime:**
- Python 3.10+ backend with async/await patterns
- JavaScript/TypeScript frontend with React
- Type hints throughout backend for IDE support and validation

**Styling Solution:**
- Tailwind CSS on frontend for rapid UI development
- CSS-in-JS support via styled-components (optional)
- WCAG 2.1 AA compliance through Tailwind accessibility utilities

**Build Tooling:**
- Vite for frontend (fast HMR, optimized bundling)
- FastAPI development server (uvicorn) with auto-reload
- Docker for containerization and deployment

**Testing Framework:**
- Backend: pytest with FastAPI TestClient
- Frontend: Vitest or Jest with React Testing Library
- E2E: Playwright or Cypress

**Code Organization (Backend):**
```
app/
├── api/
│   ├── endpoints/
│   │   ├── sessions.py
│   │   ├── questions.py
│   │   ├── scores.py
│   │   └── teams.py
│   └── dependencies.py
├── models/
│   ├── session.py
│   ├── question.py
│   ├── team.py
│   └── user.py
├── schemas/
│   ├── session.py
│   ├── question.py
│   └── team.py
├── services/
│   ├── session_service.py
│   ├── scoring_service.py
│   └── realtime_service.py
├── db/
│   ├── base.py
│   ├── session.py
│   └── crud/
│       ├── session.py
│       └── question.py
├── core/
│   ├── config.py
│   ├── security.py
│   └── constants.py
└── main.py
```

**Code Organization (Frontend):**
```
src/
├── components/
│   ├── Session/
│   ├── Question/
│   ├── Scoring/
│   ├── Team/
│   └── Common/
├── hooks/
│   ├── useSession.ts
│   ├── useWebSocket.ts
│   └── useScoring.ts
├── services/
│   ├── api.ts
│   ├── websocket.ts
│   └── auth.ts
├── store/
│   ├── sessionStore.ts
│   ├── userStore.ts
│   └── uiStore.ts
├── pages/
│   ├── Home.tsx
│   ├── Session.tsx
│   ├── Admin.tsx
│   └── Analytics.tsx
├── types/
│   └── index.ts
├── App.tsx
└── main.tsx
```

**Development Experience:**
- FastAPI auto-generated API docs at /docs
- Vite hot module reloading for instant frontend feedback
- Docker Compose for consistent local development environment
- Integrated debugging with VS Code or PyCharm
- Python type hints with mypy for backend type checking
- TypeScript strict mode for frontend type safety

## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions (Block Implementation):**
- Multi-tenancy isolation: Row-level isolation (organization_id on all tables)
- Real-time communication: Hybrid REST + WebSocket
- Event broadcasting: Redis Pub/Sub per session channel
- Authentication: JWT + Refresh Tokens
- Access control: FastAPI Dependency Injection for org/user validation

**Important Decisions (Shape Architecture):**
- Migrations: Alembic (SQLAlchemy)
- Validation: Layered (Frontend schemas, Backend Pydantic models, ORM checks, DB constraints)
- Bots: Slack/Teams as thin clients calling main API
- Frontend state: Zustand + TanStack Query
- Component organization: Feature-based folders
- UI update pattern: Optimistic + Server-authoritative

**Deferred Decisions (Post-MVP):**
- OAuth 2.0 / SSO (Okta/Auth0) for enterprise
- RabbitMQ (or similar) for guaranteed messaging
- Cloud key management (Secrets Manager / Key Vault)
- Kubernetes (K8s) for larger-scale orchestration

### Data Architecture

- Multi-tenancy: Row-level isolation via `organization_id` on all relevant tables for MVP; access enforced at API layer.
- Migrations: Alembic for versioned schema changes across environments.
- Validation Strategy: Defense-in-depth across four layers:
  - Frontend Pydantic schemas for immediate UX feedback
  - Backend Pydantic request/response models (primary validation, OpenAPI)
  - ORM-level business rules pre-insert/update
  - PostgreSQL constraints (FKs, unique, NOT NULL) for integrity

### Authentication & Security

- Auth: Stateless JWT with refresh tokens for web/mobile and WebSockets; plan OAuth 2.0 in Phase 2.
- Access Control: FastAPI dependency injection to verify `organization_id` and user roles per endpoint.
- Enterprise AI Keys: Application-layer AES-256 encryption (python-cryptography); keys in environment vars; upgrade path to cloud key vault.

### API & Communication Patterns

- REST API: Session management, questions retrieval, analytics, profiles.
- WebSocket: Real-time answer submission, score updates, facilitator signals, countdowns.
- Broadcasting: Redis Pub/Sub channels per session (e.g., `session:{id}:scores`, `session:{id}:events`) for cross-instance updates; REST fallback for state recovery.
- Bots: Slack/Teams operate as thin clients; all state centralized in main API and database.

### Frontend Architecture

- State Management: Zustand for UI/session state; TanStack Query for server state (fetching/caching).
- Component Organization: Feature-based folders (Common, Session, Question, Team, Scoring, Admin).
- Real-Time UI: Optimistic local updates with server-authoritative confirmations; error reversal on failure.

### Infrastructure & Deployment

- Config Management: Pydantic-settings with environment variables; type-safe and validated; secrets out of code.
- Logging & Monitoring: Structured JSON logging (python-json-logger) to stdout for aggregation; log session/auth/performance events.
- Deployment: Docker on managed container service (e.g., AWS ECS or Google Cloud Run); frontend via S3/CloudFront; DB via managed PostgreSQL; cache via managed Redis.
- CI/CD: GitHub Actions for test/build/deploy pipeline.

### Decision Impact Analysis

**Implementation Sequence:**
1. Establish config management (`pydantic-settings`), secrets, and logging foundation
2. Define DB schema with row-level isolation; create Alembic migrations
3. Implement auth (JWT + refresh) and access control dependencies
4. Build core REST endpoints (sessions, questions, teams)
5. Implement WebSocket gateway and Redis Pub/Sub broadcasting
6. Scaffold frontend with Vite + React TS; set up Zustand + TanStack Query
7. Implement optimistic UI flows and feature-based components
8. Integrate Slack/Teams bots as thin clients with scheduled tasks
9. Set up Docker-based deployment targets and GitHub Actions CI/CD

**Cross-Component Dependencies:**
- Access control depends on row-level isolation and JWT claims
- WebSocket broadcasting depends on Redis configuration
- Optimistic UI depends on reliable server confirmations and error handling
- Bot flows depend on REST endpoints and scheduled job infrastructure

