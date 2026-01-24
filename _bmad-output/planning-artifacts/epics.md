---
stepsCompleted: ['step-01-validate-prerequisites', 'step-02-design-epics', 'step-03-create-stories']
inputDocuments:
  - PRD: _bmad-output/implementation-artifacts/TRIVIA_APP_PRD.md
  - Architecture: _bmad-output/implementation-artifacts/architecture.md
  - UX Design: _bmad-output/implementation-artifacts/UI_UX_SPECIFICATIONS.md
  - QA Test Strategy: _bmad-output/implementation-artifacts/QA_TEST_STRATEGY.md
sprint1Stories: 12
sprint1Epics: 2
totalEpics: 9
approach: 'agile-incremental'
---

# trivia-app - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for trivia-app, decomposing the requirements from the PRD, UX Design, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

**FR-1.1: Lightning Round Opening Trivia**
- US-1.1.1: Facilitator can create 3-5 question lightning round in <2 minutes
- US-1.1.2: Participant can answer opening trivia on mobile device in <10 seconds per question
- US-1.1.3: Facilitator can see real-time team winning status

**FR-1.2: Post-Session Knowledge Check Trivia**
- US-1.2.1: Facilitator can add knowledge check at training end to assess learning
- US-1.2.2: Participant can see immediate feedback on answers
- US-1.2.3: Facilitator can see which topics group struggled with

**FR-2.1: Video Conferencing Integration (Shallow/Mobile-First)**
- US-2.1.1: In-person participant can answer on phone while seeing questions on screen
- US-2.1.2: Remote participant has same experience as in-person participants
- US-2.1.3: Facilitator can manage hybrid sessions with minimal complexity

**FR-2.2: Coffee Break Trivia (Chat Bot Integration)**
- US-2.2.1: Team member can answer daily trivia in Slack without leaving workflow
- US-2.2.2: Facilitator can schedule trivia to drop into team channels automatically
- US-2.2.3: Team sees coffee break trivia as part of learning culture

**FR-3.1: Streak Tracking**
- US-3.1.1: Participant can see participation streak and feel motivated to maintain it
- US-3.1.2: Facilitator can see team participation streaks to understand engagement patterns

**FR-3.2: AI-Powered Knowledge Gap Analysis**
- US-3.2.1: Team receives trivia recommendations based on struggle areas
- US-3.2.2: Facilitator can see which topics team should focus on

**FR-3.3: Time-Limited Challenges (FOMO Mechanics)**
- US-3.3.1: Team knows about special time-limited challenges and feels motivated to participate
- US-3.3.2: Facilitator can launch special challenges to drive engagement spikes

**FR-3.4: Progress Tracking Over Time**
- US-3.4.1: Organization can see that training improves knowledge retention over time
- US-3.4.2: Individual can see learning progress
- US-3.4.3: Trainer can prove training effectiveness to executives

**FR-4.1: Frictionless Onboarding**
- US-4.1.1: Trainer with minimal tech skills can create and launch trivia session in <2 minutes
- US-4.1.2: Facilitator can use pre-built question banks without creating custom questions
- US-4.1.3: Participant receives clear instructions on how to join and participate

**FR-4.2: Real-Time Educational Feedback**
- US-4.2.1: Participant immediately understands why answer was right or wrong
- US-4.2.2: Facilitator can verbally discuss answers while feedback displays

**FR-5.1: New Hire Onboarding Module**
- US-5.1.1: New hire learns company culture and values through trivia with onboarding cohort
- US-5.1.2: Onboarding manager can track new hire learning progress

**FR-6.1: Peer-Led Session Mode**
- US-6.1.1: Team member (not official trainer) can launch trivia session for team
- US-6.1.2: Organization can see peer-led sessions in analytics

**FR-6.2: Async-Before-Sync Workflow**
- US-6.2.1: Team member can practice alone before team competition
- US-6.2.2: Team can compare practice results before live competition

**FR-6.3: Observer Mode**
- US-6.3.1: Participant concerned about competition can observe first before competing
- US-6.3.2: Facilitator can encourage observers to participate

**FR-6.4: Enterprise AI Model Selection**
- US-6.4.1: Enterprise facilitator can select from approved AI models when creating trivia events
- US-6.4.2: Enterprise admin can set default AI model and approved models for all facilitators
- US-6.4.3: Product routes model requests appropriately based on subscription tier
- US-6.4.4: Organization can integrate with preferred AI API provider

**Total User Stories:** 24 with 154 acceptance criteria

### NonFunctional Requirements

**NFR-1: Performance Requirements**
- Mobile app load time <2 seconds (first paint on 4G network)
- Answer submission latency <500ms (acceptable for real-time gameplay)
- Score update latency <1 second (real-time feel for facilitator display)
- Concurrent participants 5000+ per event (support large company-wide events)
- Availability 99.5% uptime (corporate SLA expectation)
- Database query response <100ms (responsive experience)

**NFR-2: Security Requirements**
- HTTPS/TLS encryption for all data in transit (validated via SSL Labs testing)
- Password hashing bcrypt with salt rounds ≥10 (validated via code review)
- Rate limiting 100 req/min per IP (validated via load testing)
- SQL injection prevention via parameterized queries (validated via OWASP ZAP)
- CSRF protection for forms (validated via security testing)
- Input validation on all user inputs (validated via fuzzing and penetration testing)
- Secure session management with httpOnly cookies (validated via security audit)
- Data encryption at rest AES-256 application-level for MVP (validated via compliance review)
- GDPR compliance with data export and deletion (validated via legal review and automated testing)
- SOC 2 audit readiness post-MVP (validated via third-party audit)

**NFR-3: Scalability Requirements**
- Horizontal scaling with stateless app servers (validated via load testing)
- Database connection pooling and read replicas (validated via query performance monitoring)
- Static assets via CDN delivery (validated via geographic latency testing)
- Real-time WebSocket scalability for 5000+ connections (validated via concurrent connection testing)
- Load testing simulating 5000 concurrent users with Locust/JMeter maintaining <500ms p95
- Auto-scaling infrastructure (validated via progressive load testing)

**NFR-4: Accessibility Requirements**
- WCAG 2.1 AA compliance
- Mobile-first responsive design
- Touch targets minimum 48x48px
- Color contrast ratio 4.5:1 for text
- Keyboard navigation support
- Screen reader compatible
- No flashing content >3Hz

**NFR-5: Browser & Device Support**
- Chrome, Safari, Firefox (latest 2 versions, validated on BrowserStack)
- Mobile Safari iOS 12+, Chrome Mobile Android 9+ (validated on real devices and BrowserStack)
- Responsive design 320px-1920px (validated via responsive design testing tools)
- Touch-optimized mobile experience with buttons ≥48x48px (validated via mobile usability testing)

### Additional Requirements

**Architecture Requirements:**
- **Starter Template**: Custom full-stack setup following tiangolo/FastAPI patterns (not single all-in-one starter)
- Multi-tenancy: Row-level isolation via organization_id on all tables, enforced at API layer
- Authentication: JWT + refresh tokens (15min access, 7day refresh) with httpOnly cookies
- Real-time: Hybrid REST + WebSocket architecture with Redis Pub/Sub per session channel
- Database migrations: Alembic for versioned schema changes
- Validation: Four-layer defense (Frontend schemas → Backend Pydantic → ORM → DB constraints)
- Event broadcasting: Redis Pub/Sub channels per session (session:{id}:scores, session:{id}:events)
- API response format: {data: {...}} for success, {error: {code, message}} for failures
- WebSocket events: Versioned payloads with namespace.entity.action naming (session.score.updated)
- Backend structure: Feature-oriented modules (api/endpoints, services, schemas, models, db, core, websocket, integrations, tasks)
- Frontend structure: Feature-based folders (Session, Question, Team, Scoring, Admin, Common components)
- State management: Zustand for UI/session state, TanStack Query for server state
- Testing: pytest (backend 80%+ coverage), Jest/Vitest (frontend), Playwright/Cypress (E2E)

**UX Requirements:**
- Design philosophy: Frictionless experience, psychological safety, clarity over cleverness, mobile-first, accessibility
- Color palette: Primary Blue #0066FF, Success Green #00B34D, Warning Orange #FF9500
- Typography: Inter/Open Sans with specific font scales (H1: 32px, Body: 16px, Question: 18px)
- Spacing scale: xs(4px), sm(8px), md(16px), lg(24px), xl(32px), 2xl(48px)
- Button specifications: 44px height minimum for mobile touch targets
- Animation guidelines: 200-300ms duration, purposeful feedback animations
- Key user flows: Facilitator setup in <2 min (3-step wizard), Participant mobile join and answer, Live session monitoring
- Responsive breakpoints: Mobile 320px-640px, Tablet 640px-1024px, Desktop 1024px-1920px
- Performance targets: FCP <1s, LCP <2s, CLS <0.1, FID <100ms

**QA and Testing Requirements:**
- Testing pyramid: 60% unit tests, 30% integration tests, 10% E2E tests
- Backend testing: pytest with 80%+ code coverage target, FastAPI TestClient for API testing
- Frontend testing: Jest or Vitest with React Testing Library for component and hook testing
- E2E testing: Cypress or Playwright for critical user journeys (3-4 critical paths minimum)
- Integration testing: 100% API endpoint coverage required
- Performance testing: JMeter or Locust simulating 5000 concurrent users with p95 <500ms target
- Security testing: OWASP ZAP automated scanning, manual penetration testing, dependency vulnerability scanning
- Accessibility testing: axe DevTools and WAVE for WCAG 2.1 AA compliance, keyboard navigation, screen reader testing
- Load testing targets: p50 <200ms, p95 <500ms, p99 <1000ms, error rate <0.1% normal load and <1% peak load, throughput >100 req/sec
- CI/CD pipeline: GitHub Actions with 6 stages (lint → unit tests → integration tests → security scan → build → E2E on staging), ~40 minute total pipeline time
- Test data management: pytest fixtures for backend, test factories for reproducible data, no production data in tests, separate test database environments
- Regression testing: Critical features test suite runs before each release, nightly in CI/CD headless mode
- Bug severity classification: P1 critical (1hr response, emergency hotfix), P2 high (24hr, next sprint), P3 medium (3-5 days, next release), P4 low (2 weeks, when available)
- Test environments: Local development (SQLite for backend dev), Staging (PostgreSQL matching production), QA (PostgreSQL with anonymized production-like data)
- Test automation ROI: 20-30% development time saved, 60% bug escape rate reduction, 95%+ release confidence, 90% regression prevention

### FR Coverage Map

- FR-1.1 (Lightning Round Opening Trivia): Epic 3 - Live Trivia Gameplay & Real-Time Scoring
- FR-1.2 (Post-Session Knowledge Check): Epic 4 - Educational Feedback & Knowledge Assessment
- FR-2.1 (Video Conferencing Integration): Epic 3 - Live Trivia Gameplay & Real-Time Scoring
- FR-2.2 (Coffee Break Trivia): Epic 5 - Chat Platform Integration & Persistent Engagement
- FR-3.1 (Streak Tracking): Epic 6 - Advanced Engagement Mechanics
- FR-3.2 (AI Knowledge Gap Analysis): Epic 6 - Advanced Engagement Mechanics
- FR-3.3 (Time-Limited Challenges): Epic 6 - Advanced Engagement Mechanics
- FR-3.4 (Progress Tracking Over Time): Epic 6 - Advanced Engagement Mechanics
- FR-4.1 (Frictionless Onboarding): Epic 2 - Session Creation & Management
- FR-4.2 (Real-Time Educational Feedback): Epic 4 - Educational Feedback & Knowledge Assessment
- FR-5.1 (New Hire Onboarding Module): Epic 9 - New Hire Onboarding Specialization
- FR-6.1 (Peer-Led Session Mode): Epic 7 - Flexible Participation Modes
- FR-6.2 (Async-Before-Sync Workflow): Epic 7 - Flexible Participation Modes
- FR-6.3 (Observer Mode): Epic 7 - Flexible Participation Modes
- FR-6.4 (Enterprise AI Model Selection): Epic 8 - Enterprise Features & AI Customization

**Coverage Status:** 24/24 user stories mapped to epics (100%)

## Epic List

### Epic 1: Platform Foundation & Authentication
Users can register, login, and access the trivia platform with their organization, establishing multi-tenant infrastructure for all subsequent features.
**FRs covered:** Core infrastructure, authentication, user management, organization management, multi-tenancy
**Phase:** 1 (MVP - Month 1)

### Epic 2: Session Creation & Management
Facilitators can create trivia sessions with question banks and team assignments in <2 minutes using an intuitive setup wizard.
**FRs covered:** FR-4.1 (Frictionless Onboarding)
**Phase:** 1 (MVP - Month 1-2)

### Epic 3: Live Trivia Gameplay & Real-Time Scoring
Participants can join sessions on mobile devices and answer questions with real-time team scoring visible to all, supporting hybrid in-person and remote participation.
**FRs covered:** FR-1.1 (Lightning Round Opening Trivia), FR-2.1 (Video Conferencing Integration)
**Phase:** 1 (MVP - Month 2)

### Epic 4: Educational Feedback & Knowledge Assessment
Participants receive immediate educational feedback on answers and facilitators can assess learning outcomes with analytics showing knowledge gaps and training effectiveness.
**FRs covered:** FR-1.2 (Post-Session Knowledge Check), FR-4.2 (Real-Time Educational Feedback)
**Phase:** 1 (MVP - Month 2-3)

### Epic 5: Chat Platform Integration & Persistent Engagement
Teams engage with daily trivia challenges in Slack and Microsoft Teams channels, creating continuous learning culture between formal training events.
**FRs covered:** FR-2.2 (Coffee Break Trivia)
**Phase:** 1 (MVP - Month 2) / Phase 2 (Enhancements - Month 4)

### Epic 6: Advanced Engagement Mechanics
Teams build learning habits through participation streaks, receive personalized topic recommendations based on knowledge gaps, and compete in time-limited flash challenges with progress tracking over time.
**FRs covered:** FR-3.1 (Streak Tracking), FR-3.2 (AI Knowledge Gap Analysis), FR-3.3 (Time-Limited Challenges), FR-3.4 (Progress Tracking)
**Phase:** 2 (Market Fit Validation - Month 4)

### Epic 7: Flexible Participation Modes
All team members can participate comfortably through peer-led sessions (grassroots adoption), solo practice mode (async-before-sync), and observer mode (psychological safety for anxious participants).
**FRs covered:** FR-6.1 (Peer-Led Sessions), FR-6.2 (Async-Before-Sync Workflow), FR-6.3 (Observer Mode)
**Phase:** 2 (Market Fit Validation - Month 4-5)

### Epic 8: Enterprise Features & AI Customization
Enterprise organizations can select from approved AI models for generating trivia content, integrate with preferred AI API providers, and configure organization-wide defaults with tier-based access control.
**FRs covered:** FR-6.4 (Enterprise AI Model Selection)
**Phase:** 2 (Enterprise Readiness - Month 6)

### Epic 9: New Hire Onboarding Specialization
HR teams deploy specialized onboarding learning paths for new hire cohorts, tracking progress and enabling peer bonding through gamified culture and product knowledge trivia.
**FRs covered:** FR-5.1 (New Hire Onboarding Module)
**Phase:** 2 (Expansion Features - Month 4) / Phase 3 (Scale & Expansion - Month 7+)

---

## Epic 1: Platform Foundation & Authentication

Users can register, login, and access the trivia platform with their organization, establishing multi-tenant infrastructure for all subsequent features.

**Phase:** 1 (MVP - Month 1)
**FRs Covered:** Core infrastructure, authentication, user management, organization management, multi-tenancy

### Story 1.1: Project Initialization & Development Environment Setup

As a **developer**,
I want to **initialize the project with FastAPI backend and React frontend following the architectural patterns**,
So that **I have a working development environment ready for feature implementation**.

**Acceptance Criteria:**

**Given** the architecture specifies custom FastAPI + React setup (not single boilerplate)
**When** project is initialized
**Then** backend directory structure exists with core/, api/, models/, schemas/, services/, db/, websocket/, integrations/, tasks/, alembic/ folders
**And** frontend directory structure exists with components/, hooks/, store/, services/, pages/, types/, styles/, lib/ folders
**And** Docker Compose configured for PostgreSQL 13+ and Redis 7+ local development
**And** backend dependencies installed: FastAPI 0.100+, uvicorn, celery, redis, psycopg[binary], pydantic-settings
**And** frontend dependencies installed: React 18+, Vite, Zustand, TanStack Query, Tailwind CSS, axios
**And** development servers run successfully (backend on uvicorn with auto-reload, frontend on Vite with HMR)
**And** basic test infrastructure configured (pytest for backend 80%+ target, Jest/Vitest for frontend)
**And** linting and formatting tools configured (ESLint, Prettier for frontend; Ruff or flake8 for backend)
**And** .gitignore properly configured for Python venv/, Node.js node_modules/, and environment files
**And** README.md includes setup instructions for new developers

### Story 1.2: Organization & User Data Models

As a **developer**,
I want to **create organization and user database models with multi-tenant row-level isolation**,
So that **organizations can securely manage their users and data independently**.

**Acceptance Criteria:**

**Given** multi-tenancy requires row-level isolation via organization_id
**When** database models are created
**Then** organizations table exists with id (UUID PK), name, slug (unique), plan enum('free','premium','enterprise'), created_at
**And** users table exists with id (UUID PK), email (unique, not null), name, password_hash, organization_id (FK to organizations), role enum('facilitator','participant','admin'), created_at, updated_at
**And** Alembic migration created for schema versioning (migration 001_initial_users_orgs.py)
**And** SQLAlchemy ORM models defined in backend/models/organization.py and backend/models/user.py
**And** Pydantic schemas defined in backend/schemas/user.py (UserIn, UserOut, UserUpdate) and backend/schemas/organization.py
**And** all tables include organization_id for multi-tenant filtering (except organizations table itself)
**And** database indexes created: idx_users_email, idx_users_organization_id
**And** unit tests verify model creation, constraints, and relationships
**And** migration applies successfully on clean PostgreSQL database

### Story 1.3: User Registration with Email

As a **facilitator or participant**,
I want to **register for the platform with my email and password**,
So that **I can access the trivia application and join my organization**.

**Acceptance Criteria:**

**Given** user is on registration page
**When** user submits email, password, name, and organization slug
**Then** POST /api/v1/auth/register endpoint validates input (email format, password strength ≥8 chars, organization exists)
**And** password is hashed with bcrypt (salt rounds ≥10) before storage
**And** user record created in database with default role 'participant'
**And** API returns 201 Created with {data: {id, email, name, organization_id, role, created_at}}
**And** duplicate email returns 400 Bad Request with {error: {code: 'EMAIL_ALREADY_EXISTS', message: 'Email already registered'}}
**And** invalid organization slug returns 404 Not Found with {error: {code: 'ORG_NOT_FOUND', message: 'Organization not found'}}
**And** weak password returns 400 Bad Request with {error: {code: 'WEAK_PASSWORD', message: 'Password must be ≥8 characters'}}
**And** unit tests cover successful registration, duplicate email, invalid org, weak password scenarios
**And** integration tests verify end-to-end registration flow
**And** frontend registration form exists with email, password, name, organization fields
**And** frontend shows validation errors inline and handles API responses

### Story 1.4: User Login with JWT Authentication

As a **registered user**,
I want to **login with my email and password to receive authentication tokens**,
So that **I can access protected features securely**.

**Acceptance Criteria:**

**Given** user has registered account
**When** user submits login credentials to POST /api/v1/auth/login
**Then** backend verifies email exists and password matches bcrypt hash
**And** JWT access token generated with 15-minute expiration containing claims: {sub: user_id, org_id: organization_id, roles: [user.role]}
**And** JWT refresh token generated with 7-day expiration
**And** access token returned in response body: {data: {access_token, token_type: 'bearer', expires_in: 900}}
**And** refresh token set in httpOnly secure cookie (prevents XSS)
**And** invalid credentials return 401 Unauthorized with {error: {code: 'INVALID_CREDENTIALS', message: 'Invalid email or password'}}
**And** non-existent email returns 401 Unauthorized (same message to prevent email enumeration)
**And** unit tests verify JWT generation, token claims, expiration times
**And** integration tests verify login flow and token validation
**And** frontend login form stores access token in memory (not localStorage for security)
**And** frontend includes Authorization: Bearer {token} header in subsequent API requests

### Story 1.5: Session Management & Token Refresh

As a **logged-in user**,
I want to **refresh my authentication token before expiration**,
So that **I can stay logged in without re-entering credentials**.

**Acceptance Criteria:**

**Given** user has valid refresh token in httpOnly cookie
**When** access token expires (after 15 minutes)
**Then** frontend automatically calls POST /api/v1/auth/refresh with httpOnly cookie
**And** backend validates refresh token signature and expiration
**And** new access token generated with fresh 15-minute expiration
**And** new access token returned: {data: {access_token, token_type: 'bearer', expires_in: 900}}
**And** refresh token rotated (new 7-day refresh token issued for security)
**And** expired refresh token returns 401 Unauthorized requiring full login
**And** invalid refresh token returns 401 Unauthorized
**And** POST /api/v1/auth/logout endpoint clears refresh token cookie and invalidates tokens
**And** unit tests verify token refresh logic, expiration handling, rotation
**And** integration tests verify automatic refresh on token expiry
**And** frontend handles 401 responses by redirecting to login page
**And** frontend TanStack Query configured to retry failed requests after token refresh

### Story 1.6: Multi-Tenant Access Control

As a **system administrator**,
I want to **enforce row-level data isolation between organizations**,
So that **users can only access data within their organization**.

**Acceptance Criteria:**

**Given** multiple organizations exist in the database
**When** user makes API request to any endpoint
**Then** FastAPI dependency injection (get_current_user) extracts organization_id from JWT claims
**And** all database queries automatically filter by organization_id via dependency injection
**And** backend/api/v1/dependencies.py includes verify_org_access() function
**And** attempting to access another organization's data returns 403 Forbidden with {error: {code: 'ORG_ACCESS_DENIED', message: 'Access denied to this organization'}}
**And** all CRUD operations in backend/db/crud/ include organization_id filtering
**And** SQLAlchemy queries use .filter(model.organization_id == current_user.organization_id)
**And** unit tests verify isolation: user A cannot access user B's data from different org
**And** integration tests verify cross-org access is blocked at API layer
**And** admin role can access org-level data but not cross-org data
**And** database constraints prevent orphan records (all relevant tables have organization_id FK)

### Story 1.7: User Profile Management

As a **registered user**,
I want to **view and update my profile information**,
So that **I can manage my account details and preferences**.

**Acceptance Criteria:**

**Given** user is authenticated
**When** user requests GET /api/v1/auth/me
**Then** API returns current user profile: {data: {id, email, name, organization: {id, name, slug}, role, created_at}}
**And** password_hash is never included in response (security)
**And** user can PUT /api/v1/users/{id} to update name and email
**And** email uniqueness is validated on update (returns 400 if duplicate)
**And** users can only update their own profile (403 if attempting to update another user)
**And** admin role can update other users within same organization
**And** password changes require current password verification for security
**And** password change endpoint POST /api/v1/users/{id}/change-password validates current password before updating
**And** unit tests cover profile retrieval, updates, cross-user access denial
**And** integration tests verify end-to-end profile management
**And** frontend profile page displays user information and allows editing
**And** frontend validates email format and shows inline errors

---

## Epic 2: Session Creation & Management

Facilitators can create trivia sessions with question banks and team assignments in <2 minutes using an intuitive setup wizard.

**Phase:** 1 (MVP - Month 1-2)
**FRs Covered:** FR-4.1 (Frictionless Onboarding - US-4.1.1, US-4.1.2, US-4.1.3)

### Story 2.1: Question Bank Data Models

As a **developer**,
I want to **create question bank and question database models**,
So that **the system can store and manage curated trivia questions**.

**Acceptance Criteria:**

**Given** sessions need question banks for trivia content
**When** question database models are created
**Then** question_banks table exists with id (UUID PK), organization_id (FK), name, description, category enum('onboarding','compliance','product','culture','custom'), is_public (boolean), created_at
**And** questions table exists with id (UUID PK), question_bank_id (FK), question_text (text, not null), question_type enum('multiple_choice'), correct_answer, explanation, difficulty enum('easy','normal','hard'), topic, created_at
**And** answer_options table exists with id (UUID PK), question_id (FK), option_text, is_correct (boolean), display_order (int), created_at
**And** Alembic migration created (002_questions_schema.py)
**And** SQLAlchemy ORM models defined in backend/models/question.py and backend/models/question_bank.py
**And** Pydantic schemas defined in backend/schemas/question.py (QuestionIn, QuestionOut, QuestionBankIn, QuestionBankOut)
**And** database indexes: idx_questions_question_bank_id, idx_questions_topic, idx_answer_options_question_id
**And** foreign key constraints enforce referential integrity
**And** unit tests verify model creation and relationships
**And** seed data script creates sample question banks for development (backend/db/seed.py)

### Story 2.2: Session & Team Data Models

As a **developer**,
I want to **create session and team database models**,
So that **facilitators can create sessions and assign participants to teams**.

**Acceptance Criteria:**

**Given** facilitators need to create trivia sessions with teams
**When** session database models are created
**Then** sessions table exists with id (UUID PK), organization_id (FK), facilitator_id (FK to users), name, status enum('setup','active','completed'), event_type enum('opening','assessment','coffee_break','challenge'), question_bank_id (FK), started_at, ended_at, created_at
**And** teams table exists with id (UUID PK), session_id (FK), name, score (int default 0), created_at
**And** participants table exists with id (UUID PK), team_id (FK), user_id (FK), score (int default 0), streak (int default 0), last_participation_date, created_at
**And** session_results table exists with id (UUID PK), session_id (FK), participant_id (FK), question_id (FK), answer_given, is_correct (boolean), response_time_ms (int), answered_at
**And** Alembic migration created (003_sessions_teams_schema.py)
**And** SQLAlchemy ORM models defined in backend/models/session.py and backend/models/team.py
**And** Pydantic schemas defined in backend/schemas/session.py and backend/schemas/team.py
**And** database indexes: idx_sessions_organization_id, idx_teams_session_id, idx_participants_user_id
**And** cascade deletes configured (deleting session cascades to teams and results)
**And** unit tests verify model relationships and constraints

### Story 2.3: Session Creation API

As a **facilitator**,
I want to **create a new trivia session via API**,
So that **I can set up training events programmatically**.

**Acceptance Criteria:**

**Given** facilitator is authenticated and has facilitator or admin role
**When** facilitator sends POST /api/v1/sessions with {name, event_type, question_bank_id}
**Then** backend validates input via Pydantic schema (SessionCreate)
**And** backend/services/session_service.py creates session with status 'setup', facilitator_id from JWT, organization_id from JWT
**And** backend/db/crud/session_crud.py performs database insert with organization_id filtering
**And** API returns 201 Created with {data: {id, name, status: 'setup', event_type, organization_id, facilitator_id, created_at, share_link}}
**And** share_link auto-generated as short code (6 characters alphanumeric: "ABC123")
**And** GET /api/v1/sessions endpoint lists sessions filtered by organization_id (only user's org)
**And** GET /api/v1/sessions/{id} returns session details if user has org access, else 403 Forbidden
**And** PUT /api/v1/sessions/{id} allows facilitator to update name, question_bank_id (only before session started)
**And** DELETE /api/v1/sessions/{id} allows facilitator to delete session (only in 'setup' status)
**And** attempting to delete active/completed session returns 400 Bad Request
**And** unit tests cover CRUD operations, multi-tenant filtering, role-based access
**And** integration tests verify end-to-end session creation API flow

### Story 2.4: Question Bank Management

As a **facilitator**,
I want to **access pre-built question banks and view available questions**,
So that **I can quickly populate sessions without creating custom content**.

**Acceptance Criteria:**

**Given** question banks exist in the database
**When** facilitator requests GET /api/v1/question_banks
**Then** API returns list of question banks filtered by organization_id OR is_public=true
**And** response format: {data: [{id, name, description, category, question_count, is_public}]}
**And** GET /api/v1/question_banks/{id}/questions returns all questions in that bank with answer options
**And** questions returned include: {id, question_text, difficulty, topic, options: [{option_text, display_order}]} (correct_answer not exposed until answer submission)
**And** facilitator can POST /api/v1/question_banks to create custom bank (name, description, category, organization_id auto-filled)
**And** only admin or facilitator roles can create question banks
**And** participant role receives 403 Forbidden when attempting to create question banks
**And** seed data includes 3-5 pre-built public question banks (Company Culture, Professional Development, Compliance Basics, Product Knowledge)
**And** each seed question bank contains 15-20 questions with proper answer options
**And** unit tests verify question bank CRUD, public vs private filtering, role-based access
**And** integration tests verify end-to-end question bank retrieval

### Story 2.5: Team Management & Participant Assignment

As a **facilitator**,
I want to **create teams and assign participants for a session**,
So that **I can organize collaborative competition**.

**Acceptance Criteria:**

**Given** facilitator has created a session in 'setup' status
**When** facilitator creates teams via POST /api/v1/sessions/{session_id}/teams with {name}
**Then** team record created with session_id, name, score=0
**And** API returns 201 Created with {data: {id, session_id, name, score, created_at}}
**And** GET /api/v1/sessions/{session_id}/teams returns all teams for that session
**And** facilitator can assign participants via POST /api/v1/teams/{team_id}/participants with {user_id}
**And** participant record created linking user_id to team_id
**And** participants can self-assign via POST /api/v1/sessions/{session_id}/join with {team_name} (creates or joins team)
**And** team size validation: maximum 5 participants per team (returns 400 if team full)
**And** participant cannot join multiple teams in same session (returns 400 if already in a team)
**And** participants can leave team via POST /api/v1/teams/{team_id}/leave (only before session starts)
**And** only facilitator or admin can manually assign participants to teams
**And** unit tests cover team CRUD, participant assignment, size limits, duplicate prevention
**And** integration tests verify end-to-end team creation and participant assignment

---

## Epic 3: Live Trivia Gameplay & Real-Time Scoring

Participants can join sessions on mobile devices and answer questions with real-time team scoring visible to all, supporting hybrid in-person and remote participation.

**Phase:** 1 (MVP - Month 2)
**FRs Covered:** FR-1.1 (Lightning Round Opening Trivia), FR-2.1 (Video Conferencing Integration)

*[Detailed stories for Epic 3 will be created when Sprint 1 (Epics 1-2) nears completion - agile approach]*

---

## Epic 4: Educational Feedback & Knowledge Assessment

Participants receive immediate educational feedback on answers and facilitators can assess learning outcomes with analytics showing knowledge gaps and training effectiveness.

**Phase:** 1 (MVP - Month 2-3)
**FRs Covered:** FR-1.2 (Post-Session Knowledge Check), FR-4.2 (Real-Time Educational Feedback)

*[Detailed stories for Epic 4 will be created when Sprint 1 (Epics 1-2) nears completion]*

---

## Epic 5: Chat Platform Integration & Persistent Engagement

Teams engage with daily trivia challenges in Slack and Microsoft Teams channels, creating continuous learning culture between formal training events.

**Phase:** 1 (MVP - Month 2) / Phase 2 (Enhancements - Month 4)
**FRs Covered:** FR-2.2 (Coffee Break Trivia)

*[Detailed stories for Epic 5 will be created when Sprint 1 (Epics 1-2) nears completion]*

---

## Epic 6: Advanced Engagement Mechanics

Teams build learning habits through participation streaks, receive personalized topic recommendations based on knowledge gaps, and compete in time-limited flash challenges with progress tracking over time.

**Phase:** 2 (Market Fit Validation - Month 4)
**FRs Covered:** FR-3.1 (Streak Tracking), FR-3.2 (AI Knowledge Gap Analysis), FR-3.3 (Time-Limited Challenges), FR-3.4 (Progress Tracking)

*[Detailed stories for Epic 6 will be created in future sprint planning]*

---

## Epic 7: Flexible Participation Modes

All team members can participate comfortably through peer-led sessions (grassroots adoption), solo practice mode (async-before-sync), and observer mode (psychological safety for anxious participants).

**Phase:** 2 (Market Fit Validation - Month 4-5)
**FRs Covered:** FR-6.1 (Peer-Led Sessions), FR-6.2 (Async-Before-Sync Workflow), FR-6.3 (Observer Mode)

*[Detailed stories for Epic 7 will be created in future sprint planning]*

---

## Epic 8: Enterprise Features & AI Customization

Enterprise organizations can select from approved AI models for generating trivia content, integrate with preferred AI API providers, and configure organization-wide defaults with tier-based access control.

**Phase:** 2 (Enterprise Readiness - Month 6)
**FRs Covered:** FR-6.4 (Enterprise AI Model Selection)

*[Detailed stories for Epic 8 will be created in future sprint planning]*

---

## Epic 9: New Hire Onboarding Specialization

HR teams deploy specialized onboarding learning paths for new hire cohorts, tracking progress and enabling peer bonding through gamified culture and product knowledge trivia.

**Phase:** 2 (Expansion Features - Month 4) / Phase 3 (Scale & Expansion - Month 7+)
**FRs Covered:** FR-5.1 (New Hire Onboarding Module)

*[Detailed stories for Epic 9 will be created in future sprint planning]*