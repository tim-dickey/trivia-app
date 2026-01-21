# Trivia App - Architecture & Implementation Guide

A corporate training engagement platform providing real-time trivia sessions with team-based competition, AI-powered feedback, and Slack/Teams integration.

**Status:** ✅ Architecture Complete & Validated | Ready for Implementation

---

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [System Architecture](#system-architecture)
- [Core Features](#core-features)
- [Technology Stack](#technology-stack)
- [Key Architectural Patterns](#key-architectural-patterns)
- [Project Structure](#project-structure)
- [Development Setup](#development-setup)
- [Implementation Guide](#implementation-guide)
- [API Documentation](#api-documentation)

---

## 🎯 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 13+
- Redis 7+
- Docker & Docker Compose

### One-Command Setup
```bash
# Clone repository
git clone https://github.com/tim-dickey/trivia-app.git
cd trivia-app

# Start development environment
docker-compose up -d

# Backend initialization
cd backend
pip install -r requirements.txt
alembic upgrade head

# Frontend initialization
cd ../frontend
npm install
npm run dev
```

Backend runs on `http://localhost:8000` | Frontend runs on `http://localhost:5173`

---

## 🏗️ System Architecture

### High-Level System Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         TRIVIA APP PLATFORM                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌──────────────────┐        ┌──────────────────┐   ┌──────────────────┐ │
│  │   WEB FRONTEND   │        │  SLACK BOT       │   │  TEAMS BOT       │ │
│  │  React + Vite    │        │  (Thin Client)   │   │  (Thin Client)   │ │
│  │  TypeScript      │        │                  │   │                  │ │
│  └────────┬─────────┘        └────────┬─────────┘   └────────┬─────────┘ │
│           │                           │                      │            │
│           │ REST API                  │                      │            │
│           │ WebSocket (score updates) │ REST API             │ REST API   │
│           │                           │                      │            │
│           └───────────────────────────┼──────────────────────┘            │
│                                       │                                   │
│                    ┌──────────────────▼─────────────────┐                │
│                    │   FASTAPI BACKEND                  │                │
│                    │  - Sessions, Questions, Scoring   │                │
│                    │  - User Management, Analytics     │                │
│                    │  - WebSocket Gateway              │                │
│                    │  - AI Routing & Integration       │                │
│                    └──────────────────┬─────────────────┘                │
│                                       │                                   │
│           ┌───────────────────────────┼───────────────────────┐          │
│           │                           │                       │          │
│           ▼                           ▼                       ▼          │
│    ┌─────────────┐           ┌──────────────┐         ┌────────────┐   │
│    │ PostgreSQL  │           │    Redis     │         │  Celery    │   │
│    │ Database    │           │  Caching &   │         │  Tasks &   │   │
│    │ (Row-Level  │           │  Pub/Sub     │         │  Queue     │   │
│    │ Isolation)  │           │  Broadcasting│         │ (Async)    │   │
│    └─────────────┘           └──────────────┘         └────────────┘   │
│           │                           │                       │          │
│           └───────────────────────────┼───────────────────────┘          │
│                                       │                                   │
│                    ┌──────────────────▼─────────────────┐                │
│                    │   EXTERNAL INTEGRATIONS           │                │
│                    │  - OpenAI / Anthropic / Azure     │                │
│                    │  - SendGrid (Email)               │                │
│                    │  - Slack API                      │                │
│                    │  - Teams API                      │                │
│                    └──────────────────────────────────┘                │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

### Component Communication Diagram

```
                          CLIENT (Browser/Slack/Teams)
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
              REST Requests    WebSocket         REST Commands
           (CRUD operations)   (Real-time)    (Integrations)
                    │               │               │
                    ▼               ▼               ▼
            ┌─────────────────────────────────────────┐
            │         FastAPI Application             │
            │  /api/v1/sessions       /ws/sessions/  │
            │  /api/v1/questions                     │
            │  /api/v1/scores                        │
            └─────────────────────────────────────────┘
                    │               │               │
         ┌──────────┴───────┬───────┴───────┬──────┴──────┐
         │                  │               │             │
         ▼                  ▼               ▼             ▼
    Services Layer   WebSocket Handler  Celery Tasks  Integrations
    (Business Logic) (Connection Mgr)   (Background)  (External APIs)
         │                  │               │             │
         ▼                  ▼               ▼             ▼
    session_service  Redis Pub/Sub    score_calc   ai_service
    scoring_service  connection_mgr   notifications slack_bot
    question_service                  analytics    teams_bot
         │                  │               │
         └──────────────────┼───────────────┘
                            ▼
                    ┌──────────────────┐
                    │   CRUD Layer     │
                    │   db/crud/       │
                    │   (Row-level     │
                    │   filtering)     │
                    └─────────┬────────┘
                              ▼
                    ┌──────────────────┐
                    │  PostgreSQL DB   │
                    │  + Redis Cache   │
                    └──────────────────┘
```

### Real-Time Scoring Flow

```
Participant                   Backend                     Redis              Other Clients
    │                             │                         │                      │
    ├─ Submit Answer ────────────>│                         │                      │
    │                             │                         │                      │
    │                        [1] Validate                   │                      │
    │                        [2] Calculate Score            │                      │
    │                        [3] Broadcast                  │                      │
    │                             │                         │                      │
    │                             ├──────────────────────>  │                      │
    │                             │  PUBLISH               │                      │
    │                             │  session:123:scores    │                      │
    │                             │  {team_id, score,      │                      │
    │                             │   delta, v:1, ts}      │                      │
    │                             │                         │                      │
    │<──────────────────────────────────────────────────────├──────────────────────>│
    │  {data: {score: 150}}       │                         │     SUBSCRIBE       │
    │                             │                         │   → Receive Event   │
    │  [Optimistic update]        │                         │                      │
    │  [Show delta animation]     │                         │  [Local Update]    │
    │                             │                         │  [Show Delta]      │
    │                             │                         │  [Animate Score]   │
    │
    │ <1 second latency for all clients ✓
    │
```

### Multi-Tenancy & Row-Level Isolation

```
                    REQUEST WITH JWT TOKEN
                    {user_id: 42, org_id: 5}
                              │
                              ▼
                    ┌──────────────────────┐
                    │ FastAPI Dependency   │
                    │ get_current_user()   │
                    │ verify_org_access()  │
                    └──────────┬───────────┘
                              │ Extract org_id from token
                              ▼
                    ┌──────────────────────┐
                    │ Query Sessions       │
                    │ WHERE                │
                    │ organization_id = 5  │
                    │ (enforced before DB) │
                    └──────────┬───────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
    Org 5 Sessions       Org 12 Sessions      Org 8 Sessions
    (Visible)           (Filtered Out)       (Filtered Out)
    
    ✓ Isolation enforced at application layer BEFORE database query
    ✓ Every table has organization_id column + index
    ✓ Every query filtered by org_id via FastAPI dependencies
```

### Feature Implementation Mapping

```
FEATURE: Lightning Round
├─ Frontend
│  ├─ components/Question/QuestionDisplay.tsx
│  ├─ components/Scoring/ScoreDisplay.tsx
│  ├─ hooks/useWebSocket.ts
│  └─ store/scoringStore.ts (Zustand)
├─ API Endpoints
│  ├─ GET /api/v1/questions/random
│  ├─ POST /api/v1/scores
│  └─ GET /api/v1/sessions/{id}/scores
├─ Services
│  ├─ question_service.py (load questions)
│  ├─ scoring_service.py (calculate scores)
│  └─ realtime_service.py (broadcast scores)
├─ Database
│  ├─ questions table
│  ├─ question_options table
│  ├─ scores table
│  └─ participant_scores table
└─ Real-Time
   ├─ WebSocket: session.score.updated event
   ├─ Redis Pub/Sub: session:{id}:scores channel
   └─ <1 second score update to all clients

FEATURE: Enterprise AI Model Selection
├─ Frontend
│  └─ components/Admin/AIModelConfig.tsx
├─ API Endpoints
│  ├─ GET /api/v1/ai_models
│  ├─ POST /api/v1/ai_models/config
│  └─ PUT /api/v1/ai_models/config/{id}
├─ Services
│  ├─ ai_service.py (route to provider)
│  └─ question_service.py (fetch feedback)
├─ Database
│  ├─ ai_model_configs table
│  ├─ storage of API keys (AES-256 encrypted)
│  └─ provider selection per organization
└─ Tier-Based Routing
   ├─ Free: Microsoft Copilot (fixed)
   ├─ Premium: org-selected default (fixed)
   └─ Enterprise: facilitator choice (dynamic)
```

---

## ✨ Core Features

### 1. **Real-Time Trivia Sessions**
- Team-based competition with live scoring
- Multiple session types: opening energizers, knowledge assessments, coffee breaks, lightning rounds
- Support for 5000+ concurrent participants
- <1 second score updates across all clients

### 2. **Live Scoring & Feedback**
- Instant score calculation with multipliers
- AI-powered educational feedback (ChatGPT, Claude, Azure OpenAI)
- Visual score delta animations
- Participation streak tracking

### 3. **Multi-Organization Platform**
- Row-level data isolation (organization_id on all tables)
- Team hierarchies and role-based access control
- Analytics per organization
- Session management dashboards

### 4. **Slack & Teams Integration**
- Bot notifications for session updates
- Interactive slash commands for session management
- Session join links in chat
- Score announcements and leaderboards

### 5. **Enterprise AI Model Selection** 🆕
- Facilitators select AI model per event (enterprise tier)
- Support for GPT-5.1-Codex-Max, Claude, Azure OpenAI
- Tier-based routing (free → Copilot, premium → org default, enterprise → facilitator choice)
- Custom API credential management with AES-256 encryption

### 6. **Observer Mode**
- Low-pressure participation option
- Access to session content without scoring
- Analytics tracking for engagement metrics

---

## 🛠️ Technology Stack

### Backend
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | FastAPI | 0.100+ | Async HTTP & WebSocket server |
| **Runtime** | Python | 3.10+ | Backend application language |
| **ORM** | SQLAlchemy | 2.0+ | Database abstraction layer |
| **Validation** | Pydantic | 2.0+ | Request/response validation |
| **Async Jobs** | Celery | 5.3+ | Background task processing |
| **Migrations** | Alembic | 1.12+ | Database schema versioning |

### Frontend
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | React | 18+ | UI library |
| **Language** | TypeScript | 5+ | Type-safe JavaScript |
| **Build Tool** | Vite | 5+ | Fast development server & bundler |
| **State Mgmt** | Zustand | 4.4+ | Client state management |
| **Server Data** | TanStack Query | 5+ | Server state caching |
| **Styling** | Tailwind CSS | 3+ | Utility-first CSS framework |

### Infrastructure
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Database** | PostgreSQL | 13+ | Primary data store |
| **Cache & Pub/Sub** | Redis | 7+ | Caching & real-time broadcasting |
| **Container** | Docker | 24+ | Application containerization |
| **Orchestration** | Docker Compose | 2.0+ | Local development environment |
| **Deployment** | ECS / Cloud Run | Latest | Managed container services |

---

## 🔑 Key Architectural Patterns

### 1. Multi-Tenancy with Row-Level Isolation

Every database table includes `organization_id` column. FastAPI dependency injection filters queries before they reach the database:

```python
@app.get("/sessions")
async def get_sessions(
    current_user = Depends(get_current_user),  # Extracts org_id from JWT
    db = Depends(get_db)
):
    # Automatically filters: WHERE organization_id = current_user.org_id
    sessions = db.query(Session).filter(Session.organization_id == current_user.org_id)
    return sessions
```

### 2. Real-Time Scoring via WebSocket + Redis Pub/Sub

```
Client connects to /ws/sessions/{id}
    ↓
Answer submitted via POST /scores
    ↓
scoring_service.calculate_score()
    ↓
redis.publish("session:123:scores", {team_id, score, delta, v:1, ts})
    ↓
All connected clients receive event via WebSocket
    ↓
Frontend updates Zustand store + animates score delta
```

### 3. Optimistic UI with Server Confirmation

```javascript
// Frontend (React/TypeScript)
const submitAnswer = async (questionId, selectedOption) => {
  // 1. Optimistic update (local state immediately)
  scoringStore.updateLocalScore(+10)
  
  // 2. API call
  const response = await api.post("/scores", {question_id: questionId, option: selectedOption})
  
  // 3. Server confirmation
  if (response.ok) {
    scoringStore.confirmScore(response.data.score)  // Update from server
  } else {
    // 4. Error: revert to previous state
    scoringStore.revertScore()
    showToast("Failed to submit answer. Please try again.")
  }
}
```

### 4. Three-Layer Validation

1. **Frontend Validation** - Real-time user feedback (React schemas)
2. **Backend Validation** - Pydantic schemas enforce data contracts
3. **ORM Validation** - SQLAlchemy model constraints
4. **Database Constraints** - PRIMARY KEY, FOREIGN KEY, CHECK constraints

### 5. Feature-Based Code Organization

Both backend and frontend use feature-oriented structure:

```
backend/
  services/
    session_service.py     # Lightning Round session logic
    scoring_service.py     # Lightning Round scoring logic
    question_service.py    # Lightning Round questions
  db/crud/
    session_crud.py        # Lightning Round database ops
  api/endpoints/
    sessions.py            # Lightning Round REST routes

frontend/
  components/Session/      # Lightning Round UI
    SessionSetup.tsx
    SessionView.tsx
  hooks/
    useSession.ts          # Lightning Round data fetching
  services/
    sessionApi.ts          # Lightning Round API calls
```

### 6. Async Task Processing with Celery

Background tasks (score aggregation, notifications, analytics) processed asynchronously:

```python
@app.post("/sessions/{id}/end")
async def end_session(session_id: str, db = Depends(get_db)):
    session = db.query(Session).get(session_id)
    session.status = "ended"
    db.commit()
    
    # Trigger background tasks
    aggregation_task.delay(session_id)      # Celery task
    notification_task.delay(session_id)
    analytics_task.delay(session_id)
    
    return {"status": "ended"}
```

---

## 📁 Project Structure

```
trivia-app/
├── README.md                          # This file
├── LICENSE
├── docker-compose.yml                 # Local development environment
├── .github/
│   └── workflows/
│       ├── ci.yml                     # Test, lint, build pipeline
│       ├── deploy.yml                 # Deploy to ECS/Cloud Run
│       └── lint-security.yml          # Codacy analysis, security scanning
│
├── backend/                           # FastAPI application
│   ├── main.py                        # App entry point
│   ├── requirements.txt                # Python dependencies
│   ├── core/
│   │   ├── config.py                  # Pydantic-settings (env-based config)
│   │   ├── security.py                # JWT, encryption, password hashing
│   │   └── logging_config.py          # Structured logging to stdout
│   ├── api/v1/
│   │   ├── endpoints/
│   │   │   ├── sessions.py            # Session CRUD + WebSocket
│   │   │   ├── questions.py           # Question management
│   │   │   ├── scores.py              # Score endpoints
│   │   │   ├── teams.py               # Team management
│   │   │   ├── users.py               # User management
│   │   │   ├── ai_models.py           # AI model configuration
│   │   │   └── organizations.py       # Organization admin
│   │   └── dependencies.py            # FastAPI dependency injection (access control)
│   ├── models/                        # SQLAlchemy ORM models
│   │   ├── base.py                    # Base model with org_id + timestamps
│   │   ├── user.py
│   │   ├── session.py
│   │   ├── question.py
│   │   ├── score.py
│   │   └── ai_model_config.py
│   ├── schemas/                       # Pydantic validation schemas
│   │   ├── responses.py               # APIResponse, ErrorResponse
│   │   ├── session.py
│   │   ├── question.py
│   │   └── score.py
│   ├── services/                      # Business logic layer
│   │   ├── session_service.py         # Session orchestration
│   │   ├── scoring_service.py         # Score calculation + broadcasting
│   │   ├── question_service.py        # Question loading + AI feedback
│   │   ├── ai_service.py              # AI provider routing
│   │   ├── realtime_service.py        # WebSocket broadcasting
│   │   ├── slack_service.py           # Slack notifications
│   │   └── teams_service.py           # Teams notifications
│   ├── db/
│   │   ├── base.py                    # SQLAlchemy engine + session factory
│   │   ├── crud/
│   │   │   ├── session_crud.py
│   │   │   ├── score_crud.py
│   │   │   └── question_crud.py
│   │   └── seed.py                    # Database seeding (dev)
│   ├── websocket/
│   │   ├── connection_manager.py      # WebSocket connection pooling
│   │   ├── handlers.py                # Connect/disconnect/message logic
│   │   ├── events.py                  # Event payload definitions
│   │   └── router.py                  # WebSocket routes
│   ├── integrations/
│   │   ├── redis_pubsub.py            # Redis pub/sub wrapper
│   │   ├── slack_bot.py               # Slack event listener
│   │   ├── teams_bot.py               # Teams event listener
│   │   ├── ai_providers.py            # LLM client wrapper
│   │   └── email_provider.py          # Email notifications
│   ├── tasks/
│   │   ├── celery_app.py              # Celery configuration
│   │   ├── score_calculation.py       # Async score aggregation
│   │   ├── notifications.py           # Async notifications
│   │   └── analytics.py               # Async analytics
│   ├── alembic/                       # Database migrations
│   │   ├── alembic.ini
│   │   └── versions/
│   │       ├── 001_initial_schema.py
│   │       ├── 002_questions_schema.py
│   │       └── 003_ai_config_schema.py
│   └── tests/
│       ├── unit/
│       ├── integration/
│       └── e2e/
│
├── frontend/                          # React + TypeScript application
│   ├── package.json
│   ├── vite.config.ts                 # Build configuration
│   ├── tsconfig.json                  # TypeScript configuration
│   ├── src/
│   │   ├── main.tsx                   # React entry point
│   │   ├── App.tsx                    # Root component
│   │   ├── components/
│   │   │   ├── Session/
│   │   │   │   ├── SessionSetup.tsx   # Setup wizard
│   │   │   │   ├── SessionView.tsx    # Main session display
│   │   │   │   ├── SessionLeaderboard.tsx
│   │   │   │   └── SessionControls.tsx
│   │   │   ├── Question/
│   │   │   │   ├── QuestionDisplay.tsx
│   │   │   │   ├── QuestionOptions.tsx
│   │   │   │   └── QuestionFeedback.tsx
│   │   │   ├── Scoring/
│   │   │   │   ├── ScoreDisplay.tsx
│   │   │   │   └── ScoreDelta.tsx
│   │   │   ├── Admin/
│   │   │   │   ├── Dashboard.tsx
│   │   │   │   └── AIModelConfig.tsx
│   │   │   ├── Auth/
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   ├── SignupForm.tsx
│   │   │   │   └── PrivateRoute.tsx
│   │   │   └── Common/
│   │   │       ├── Header.tsx
│   │   │       ├── Sidebar.tsx
│   │   │       ├── Toast.tsx
│   │   │       └── ErrorBoundary.tsx
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useSession.ts
│   │   │   ├── useWebSocket.ts
│   │   │   └── useScoring.ts
│   │   ├── store/
│   │   │   ├── authStore.ts           # Zustand auth store
│   │   │   ├── sessionStore.ts        # Zustand session store
│   │   │   ├── scoringStore.ts        # Zustand scoring store
│   │   │   └── uiStore.ts
│   │   ├── services/
│   │   │   ├── api.ts                 # Axios instance + interceptors
│   │   │   ├── sessionApi.ts
│   │   │   ├── questionApi.ts
│   │   │   ├── scoreApi.ts
│   │   │   ├── authApi.ts
│   │   │   ├── aiModelApi.ts
│   │   │   └── websocketService.ts
│   │   ├── types/
│   │   │   ├── index.ts               # Type exports
│   │   │   ├── api.ts                 # API response types
│   │   │   ├── session.ts
│   │   │   ├── score.ts
│   │   │   └── events.ts
│   │   ├── styles/
│   │   │   ├── globals.css            # Tailwind setup
│   │   │   └── animations.css
│   │   └── lib/
│   │       ├── formatters.ts
│   │       ├── validators.ts
│   │       └── constants.ts
│   └── tests/
│       ├── __tests__/
│       │   ├── components/
│       │   ├── hooks/
│       │   └── services/
│       └── e2e/
│
├── docs/
│   ├── API.md                         # API endpoint documentation
│   ├── DEVELOPMENT.md                 # Development setup guide
│   ├── DEPLOYMENT.md                  # Deployment procedures
│   └── ARCHITECTURE.md                # Complete architecture document
│
└── _bmad-output/
    └── implementation-artifacts/
        ├── architecture.md            # Complete architecture decision document
        ├── TRIVIA_APP_PRD.md          # Product requirements
        ├── UI_UX_SPECIFICATIONS.md    # UI/UX design specs
        └── QA_TEST_STRATEGY.md        # QA testing strategy
```

---

## 🚀 Development Setup

### Environment Variables

**Backend** (`.env.local`):
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/trivia_app

# Redis
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# AI Providers (optional)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...
AZURE_OPENAI_API_KEY=...

# External Services
SLACK_BOT_TOKEN=xoxb-...
TEAMS_BOT_ID=...
```

**Frontend** (`.env.local`):
```bash
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

### Local Development Commands

```bash
# Backend
cd backend
python -m pip install -r requirements.txt
alembic upgrade head                    # Run migrations
uvicorn main:app --reload              # Start dev server (port 8000)

# Frontend
cd frontend
npm install
npm run dev                              # Start dev server (port 5173)

# Database (via Docker Compose)
docker-compose up -d postgres redis    # Start services

# Run tests
python -m pytest                         # Backend tests
npm run test                             # Frontend tests
```

---

## 📚 Implementation Guide

### For AI Code Agents

1. **Read** the complete [Architecture Decision Document](./docs/ARCHITECTURE.md)
2. **Review** implementation patterns section for naming conventions, structure rules, and communication formats
3. **Follow** the project structure exactly as defined
4. **Use** provided type definitions and validation schemas
5. **Test** each feature against the test suite before proceeding

### For Development Teams

1. **Assign stories** from the backlog in priority order
2. **Reference** the architecture document for decisions on technology/patterns
3. **Review** PRs using the patterns section as a checklist
4. **Validate** that code follows naming conventions and structure rules
5. **Test** according to the test organization (unit/integration/e2e)

### Implementation Checklist

- [ ] Backend project scaffold (FastAPI app, models, schemas, services)
- [ ] Database schema with Alembic migrations
- [ ] Authentication system (JWT + refresh tokens)
- [ ] REST endpoints for core features
- [ ] WebSocket gateway for real-time updates
- [ ] Frontend React/TypeScript scaffold
- [ ] Component hierarchy and routing
- [ ] State management (Zustand stores)
- [ ] API client layer (TanStack Query)
- [ ] Real-time WebSocket integration
- [ ] Slack/Teams bot integration
- [ ] AI provider integration (OpenAI/Anthropic/Azure)
- [ ] Background task processing (Celery)
- [ ] Docker containerization
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Deployment to ECS/Cloud Run

---

## 📖 API Documentation

### REST Endpoints

**Sessions**
```
POST   /api/v1/sessions              Create session
GET    /api/v1/sessions/{id}         Get session details
PUT    /api/v1/sessions/{id}         Update session
GET    /api/v1/sessions/{id}/scores  Get session scores
```

**Questions**
```
GET    /api/v1/questions             Get questions for session
POST   /api/v1/questions/random      Get random question
GET    /api/v1/question_banks        List question banks
```

**Scores**
```
POST   /api/v1/scores                Submit answer + calculate score
GET    /api/v1/teams/{id}/scores     Get team leaderboard
```

**Users**
```
POST   /api/v1/users/register        User registration
POST   /api/v1/users/login           User login
GET    /api/v1/users/me              Current user profile
```

**AI Models** (Enterprise)
```
GET    /api/v1/ai_models             List available models
POST   /api/v1/ai_models/config      Set org AI model config
```

### WebSocket Events

**Session Events**
```javascript
// Client connects
ws.connect("/ws/sessions/{session_id}?token={jwt_token}")

// Server sends real-time updates
{
  "event": "session.score.updated",
  "data": {
    "session_id": "123",
    "team_id": "team-1",
    "score": 150,
    "delta": 10,
    "v": 1,
    "ts": "2026-01-20T12:00:00Z"
  }
}

// Participant joined
{
  "event": "session.participant.joined",
  "data": {
    "participant_id": "user-42",
    "session_id": "123"
  }
}
```

---

## 🔒 Security Considerations

- ✅ **Row-level isolation** via organization_id filtering in FastAPI dependencies
- ✅ **JWT authentication** with 15-minute access tokens + 7-day refresh tokens
- ✅ **HTTPS/TLS** encryption in transit (enforced in production)
- ✅ **bcrypt password hashing** with salt (min 12 rounds)
- ✅ **AES-256 encryption** for stored API keys and credentials
- ✅ **GDPR compliance** via audit logging (event_log table)
- ✅ **CORS configuration** for cross-origin requests
- ✅ **Input validation** at four layers (frontend → backend → ORM → DB)

---

## 📊 Performance Targets

| Metric | Target | Implementation |
|--------|--------|-----------------|
| **API Latency** | <500ms | FastAPI async, Redis caching |
| **Score Updates** | <1s (99th percentile) | WebSocket + Redis Pub/Sub |
| **Mobile Load Time** | <2s | Vite optimization, code splitting |
| **Concurrent Users** | 5000+ | Stateless servers, connection pooling |
| **Uptime SLA** | 99.5% | Managed container services, auto-scaling |
| **Database Queries** | <100ms (95th percentile) | Connection pooling, indexes on org_id |

---

## 📝 Contributing

See [DEVELOPMENT.md](./docs/DEVELOPMENT.md) for contribution guidelines, coding standards, and PR review checklist.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 📞 Contact & Support

For questions about architecture or implementation:
- 📧 Review [Architecture Decision Document](./docs/ARCHITECTURE.md)
- 🔍 Check [API Documentation](./docs/API.md)
- 💬 See [Development Guide](./docs/DEVELOPMENT.md)

**Architecture Status:** ✅ Complete & Validated (January 20, 2026)
**Implementation Status:** Ready to Begin
