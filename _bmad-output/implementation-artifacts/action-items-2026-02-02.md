# Action Items from Code Review - February 2, 2026

## Overview

This document contains prioritized action items derived from the comprehensive code review of PR #20. Items are organized by priority and estimated effort to help with sprint planning.

---

## 🔴 CRITICAL PRIORITY (Must Complete Before Feature Work)

### 1. Consolidate CI/CD Workflows

**Issue**: Duplicate test runs on every PR (Codacy + CodeQL both run tests)

**Impact**: 
- Wastes CI/CD minutes
- Slows down PR feedback cycle
- Confuses contributors about which workflow to check

**Action**:
```yaml
# Proposed: Create single consolidated workflow
.github/workflows/ci.yml:
  - Checkout + Setup
  - Backend tests (once)
  - Frontend tests
  - Upload results to Codacy AND CodeQL
  
.github/workflows/security-scheduled.yml:
  - Run only on schedule + main branch merges
  - Deep security scans (Bandit, CodeQL, dependency audit)
```

**Acceptance Criteria**:
- [ ] Single workflow runs tests on PRs
- [ ] No duplicate test executions
- [ ] Coverage reports uploaded to both Codacy and GitHub
- [ ] Security scans run on schedule only

**Estimated Effort**: 3 hours  
**Priority**: P0 - Blocks efficient development

---

### 2. Implement Organization Scoping Middleware

**Issue**: Multi-tenant data isolation not enforced at application layer

**Risk**: 
- Developers might forget to filter by `organization_id`
- Potential data leakage between tenants
- Security vulnerability

**Action**:
```python
# Create: backend/core/multi_tenancy.py

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

async def get_current_organization(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Organization:
    """Extract organization from JWT and validate access"""
    # Decode JWT, extract org_id, verify access
    pass

# Create: backend/db/crud/base.py

class MultiTenantCRUD:
    """Base CRUD with automatic organization scoping"""
    
    def get_multi_for_org(self, db: Session, org_id: int, skip: int = 0, limit: int = 100):
        return db.query(self.model).filter(
            self.model.organization_id == org_id
        ).offset(skip).limit(limit).all()
```

**Acceptance Criteria**:
- [ ] Middleware extracts organization from JWT
- [ ] Base CRUD class auto-filters by organization_id
- [ ] Integration tests validate tenant isolation
- [ ] Documentation updated with usage examples

**Estimated Effort**: 1 day  
**Priority**: P0 - Security critical

---

### 3. Implement WebSocket Infrastructure

**Issue**: Core architecture requires real-time features, but no WebSocket setup exists

**Blocks**:
- Session management
- Live scoring
- Real-time participant updates
- Chat features

**Action**:
```python
# Create: backend/websocket/manager.py

from fastapi import WebSocket
from typing import Dict, List

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)
    
    async def broadcast_to_session(self, session_id: str, message: dict):
        if session_id in self.active_connections:
            for connection in self.active_connections[session_id]:
                await connection.send_json(message)

# Update: backend/main.py

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(websocket, session_id)
    # Handle messages
```

**Frontend Action**:
```typescript
// Create: frontend/src/services/websocket.ts

export class WebSocketService {
  private ws: WebSocket | null = null;
  
  connect(sessionId: string) {
    this.ws = new WebSocket(`ws://localhost:8000/ws/${sessionId}`);
    this.ws.onmessage = (event) => {
      // Handle incoming messages
    };
  }
}
```

**Acceptance Criteria**:
- [ ] WebSocket endpoint implemented in backend
- [ ] Connection manager handles multiple sessions
- [ ] Authentication integrated with WebSocket connections
- [ ] Frontend WebSocket service created
- [ ] Basic message broadcast working
- [ ] Integration tests for WebSocket functionality

**Estimated Effort**: 2 days  
**Priority**: P0 - Blocks MVP features

---

### 4. Fix Test Database Configuration

**Issue**: CI uses SQLite while production uses PostgreSQL (different SQL dialects)

**Risk**:
- Tests pass locally but fail in production
- PostgreSQL-specific features won't be tested
- Migration compatibility issues

**Action**:
```yaml
# Update: .github/workflows/codacy.yml

services:
  postgres:
    image: postgres:13
    env:
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_pass
      POSTGRES_DB: test_db
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5

jobs:
  codacy-security-scan:
    env:
      DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db
```

**Acceptance Criteria**:
- [ ] PostgreSQL service added to CI workflows
- [ ] All tests use PostgreSQL in CI
- [ ] Migrations run before tests
- [ ] Test database properly cleaned between test runs

**Estimated Effort**: 2 hours  
**Priority**: P0 - Test reliability

---

### 5. Document Required Secrets and CI Setup

**Issue**: External contributors cannot run full CI pipeline

**Impact**:
- Blocks external contributions
- Workflows fail silently for forks
- Poor contributor experience

**Action**:

**Update CONTRIBUTING.md**:
```markdown
## CI/CD Setup

### Required GitHub Secrets

For full CI/CD functionality, configure these secrets:

1. **CODACY_PROJECT_TOKEN** (Optional for external contributors)
   - Go to Settings → Secrets → Actions
   - Add secret: `CODACY_PROJECT_TOKEN`
   - Value: Get from https://app.codacy.com/

### Running CI Locally

```bash
# Backend tests
cd backend
pytest --cov=backend --cov-report=term

# Frontend tests  
cd frontend
npm test

# Security scan (optional)
docker run --rm -v $(pwd):/src codacy/codacy-analysis-cli analyze
```

### Workflow Behavior

- **Main CI**: Runs on all PRs, tests only
- **Security Scans**: Runs on main branch + weekly schedule
- **Codacy Upload**: Skipped if secret not available (forks)
```

**Update Workflows**:
```yaml
# Make Codacy optional
- name: Upload SARIF results file
  if: ${{ secrets.CODACY_PROJECT_TOKEN != '' }}
  uses: github/codeql-action/upload-sarif@v3
```

**Acceptance Criteria**:
- [ ] All required secrets documented
- [ ] Local testing instructions provided
- [ ] Workflows gracefully skip steps if secrets missing
- [ ] README.md links to CONTRIBUTING.md CI section

**Estimated Effort**: 1 hour  
**Priority**: P0 - Blocks contributions

---

## 🟡 HIGH PRIORITY (Should Complete This Sprint)

### 6. Update Outdated Dependencies

**Issue**: Multiple packages have security updates and performance improvements available

**Packages to Update**:
```bash
# Backend
fastapi: 0.109.0 → 0.115.0+
pydantic: 2.12.5 → 2.13.x (security fixes)
pytest: 7.4.4 → 8.x (better performance)

# Frontend  
react: ^18.2.0 → ^18.3.1
vite: ^5.0.8 → ^5.4.x (security patches)
typescript: ^5.2.2 → ^5.7.x
tailwindcss: ^3.3.6 → ^3.4.x
```

**Action**:
1. Create dependency update branch
2. Update each ecosystem separately (backend, then frontend)
3. Run full test suite after each update
4. Document any breaking changes
5. Update documentation if APIs changed

**Acceptance Criteria**:
- [ ] All major dependencies updated to latest stable
- [ ] Tests pass on both backend and frontend
- [ ] No new deprecation warnings
- [ ] CHANGELOG updated with dependency changes

**Estimated Effort**: 4 hours (+ testing)  
**Priority**: P1 - Security & performance

---

### 7. Add Frontend CI Workflow

**Issue**: No automated validation of frontend code quality

**Current State**:
- Backend: ✅ Tested automatically
- Frontend: ❌ No CI validation

**Action**:
```yaml
# Create: .github/workflows/frontend-ci.yml

name: Frontend CI

on:
  pull_request:
    paths:
      - 'frontend/**'
      - '.github/workflows/frontend-ci.yml'
  push:
    branches: [main]
    paths:
      - 'frontend/**'

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json
      
      - name: Install dependencies
        run: cd frontend && npm ci
      
      - name: Lint
        run: cd frontend && npm run lint
      
      - name: Type check
        run: cd frontend && npm run type-check
      
      - name: Build
        run: cd frontend && npm run build
      
      - name: Test
        run: cd frontend && npm test -- --coverage
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          directory: ./frontend/coverage
```

**Acceptance Criteria**:
- [ ] Workflow runs on frontend changes
- [ ] All checks (lint, type-check, build, test) pass
- [ ] Coverage reports uploaded
- [ ] Workflow badge added to README

**Estimated Effort**: 2 hours  
**Priority**: P1 - Quality assurance

---

### 8. Expand CodeQL Security Analysis

**Issue**: CodeQL only analyzes GitHub Actions, not application code

**Security Gap**:
- Python code not scanned for vulnerabilities
- TypeScript/JavaScript not analyzed
- SQL injection, XSS, and other issues may be missed

**Action**:
```yaml
# Update: .github/workflows/codeql.yml

strategy:
  matrix:
    include:
    - language: python
      build-mode: none
    - language: javascript-typescript
      build-mode: none  
    - language: actions
      build-mode: none
```

**Acceptance Criteria**:
- [ ] Python analysis enabled
- [ ] JavaScript/TypeScript analysis enabled
- [ ] First scan completes successfully
- [ ] Security issues (if any) documented
- [ ] False positives marked as such

**Estimated Effort**: 1 hour  
**Priority**: P1 - Security scanning

---

### 9. Add Docker Compose Development Services

**Issue**: docker-compose.yml only has infrastructure, not application services

**Developer Pain Point**:
- Must manually run 4 commands in different terminals
- Inconsistent development environments
- New contributors struggle with setup

**Action**:
```yaml
# Update: docker-compose.yml

services:
  postgres:
    # ... existing config ...
  
  redis:
    # ... existing config ...
  
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    command: uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://trivia_user:trivia_pass@postgres:5432/trivia_db
      REDIS_URL: redis://redis:6379/0
      DEBUG: "true"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
  
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    command: npm run dev -- --host 0.0.0.0
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "5173:5173"
    environment:
      VITE_API_URL: http://localhost:8000
```

**Create Dockerfiles**:
```dockerfile
# backend/Dockerfile.dev
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "backend.main:app", "--reload", "--host", "0.0.0.0"]

# frontend/Dockerfile.dev
FROM node:20-alpine
WORKDIR /app
COPY package*.json .
RUN npm ci
COPY . .
CMD ["npm", "run", "dev"]
```

**Acceptance Criteria**:
- [ ] Single `docker-compose up` starts everything
- [ ] Hot reload works for backend and frontend
- [ ] Database migrations run automatically
- [ ] README updated with Docker instructions

**Estimated Effort**: 3 hours  
**Priority**: P1 - Developer experience

---

### 10. Add Security Headers Middleware

**Issue**: Missing common security headers (HSTS, CSP, X-Frame-Options)

**Security Best Practices**:
- HSTS: Force HTTPS
- CSP: Prevent XSS attacks
- X-Frame-Options: Prevent clickjacking

**Action**:
```python
# Create: backend/core/security_middleware.py

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # HSTS - Force HTTPS for 1 year
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # CSP - Restrict resource loading
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' ws: wss:;"
        )
        
        # Clickjacking protection
        response.headers["X-Frame-Options"] = "DENY"
        
        # MIME type sniffing protection
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # XSS protection (legacy browsers)
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        return response

# Update: backend/main.py
app.add_middleware(SecurityHeadersMiddleware)
```

**Acceptance Criteria**:
- [ ] All security headers present in responses
- [ ] CSP policy doesn't break functionality
- [ ] Tests verify headers are set correctly
- [ ] Documentation explains each header

**Estimated Effort**: 2 hours  
**Priority**: P1 - Security hardening

---

## 🟢 MEDIUM PRIORITY (Nice to Have This Sprint)

### 11. Add Quick Start to README

**Issue**: README is comprehensive but lacks quick start section

**Action**:
Add to top of README.md:
```markdown
## ⚡ Quick Start

```bash
# One-command startup (requires Docker)
docker-compose up

# Access the application:
# - Frontend: http://localhost:5173
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

**Manual Setup** (without Docker):

```bash
# 1. Start infrastructure
docker-compose up -d postgres redis

# 2. Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
python main.py

# 3. Frontend setup (new terminal)
cd frontend
npm install
npm run dev
```
```

**Estimated Effort**: 15 minutes  
**Priority**: P2 - Documentation

---

### 12. Create Architecture Diagram

**Issue**: Architecture doc is text-heavy, no visual representation

**Action**:
Create Excalidraw or Mermaid diagram showing:
- System components (Frontend, Backend, Database, Redis, Celery)
- Data flow for key operations (authentication, session creation, real-time scoring)
- External integrations (Slack, Teams, AI models)
- Multi-tenant data isolation

**Example Mermaid**:
```mermaid
graph TB
    FE[React Frontend] -->|WebSocket| BE[FastAPI Backend]
    FE -->|REST API| BE
    BE -->|SQLAlchemy| DB[(PostgreSQL)]
    BE -->|Pub/Sub| REDIS[(Redis)]
    CELERY[Celery Workers] -->|Tasks| REDIS
    BE -->|Queue Tasks| REDIS
    BE -->|Slack API| SLACK[Slack Integration]
    BE -->|Teams API| TEAMS[MS Teams Integration]
    BE -->|AI Models| AI[OpenAI/Anthropic/Azure]
```

**Acceptance Criteria**:
- [ ] High-level architecture diagram created
- [ ] Embedded in architecture.md
- [ ] Shows all major components
- [ ] Data flow clearly illustrated

**Estimated Effort**: 1 hour  
**Priority**: P2 - Documentation

---

### 13. Add Pre-commit Hooks

**Issue**: Code quality checks only run in CI, not locally

**Action**:
```bash
# Install pre-commit
pip install pre-commit

# Create: .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.3.0
    hooks:
      - id: black
        language_version: python3.11
        files: ^backend/
  
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        files: ^backend/
  
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.55.0
    hooks:
      - id: eslint
        files: ^frontend/
        additional_dependencies:
          - eslint@8.55.0
          - '@typescript-eslint/eslint-plugin@6.14.0'
  
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: detect-private-key
      - id: check-merge-conflict

# Install hooks
pre-commit install
```

**Acceptance Criteria**:
- [ ] Pre-commit hooks configured
- [ ] Installation instructions in CONTRIBUTING.md
- [ ] Hooks run before commits
- [ ] CI checks match pre-commit checks

**Estimated Effort**: 1 hour  
**Priority**: P2 - Developer experience

---

### 14. Create Dependabot Configuration

**Issue**: No automated dependency update notifications

**Action**:
```yaml
# Create: .github/dependabot.yml

version: 2
updates:
  # Backend Python dependencies
  - package-ecosystem: "pip"
    directory: "/backend"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 5
    reviewers:
      - "tim-dickey"
    labels:
      - "dependencies"
      - "backend"
    commit-message:
      prefix: "chore"
      include: "scope"
  
  # Frontend npm dependencies
  - package-ecosystem: "npm"
    directory: "/frontend"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 5
    reviewers:
      - "tim-dickey"
    labels:
      - "dependencies"
      - "frontend"
    commit-message:
      prefix: "chore"
      include: "scope"
  
  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 5
    reviewers:
      - "tim-dickey"
    labels:
      - "dependencies"
      - "ci"
    commit-message:
      prefix: "chore"
```

**Acceptance Criteria**:
- [ ] Dependabot configured for all ecosystems
- [ ] Weekly PRs created automatically
- [ ] Proper labels and reviewers assigned
- [ ] Documentation explains Dependabot workflow

**Estimated Effort**: 30 minutes  
**Priority**: P2 - Automation

---

### 15. Add Troubleshooting Guide

**Issue**: No documentation for common issues

**Action**:
```markdown
# Add to README.md or create TROUBLESHOOTING.md

## Troubleshooting

### Database Connection Issues

**Error**: `Connection refused - could not connect to server`

**Solution**:
```bash
# Check if PostgreSQL is running
docker-compose ps

# Restart database
docker-compose restart postgres

# Check logs
docker-compose logs postgres
```

### Frontend Can't Connect to Backend

**Error**: `Network Error` or `CORS policy`

**Solution**:
1. Verify backend is running: http://localhost:8000/health
2. Check CORS_ORIGINS in backend/.env
3. Ensure frontend uses correct API URL

### Migration Errors

**Error**: `Target database is not up to date`

**Solution**:
```bash
cd backend
alembic upgrade head
```

### Port Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Find process using port
lsof -i :8000  # Backend
lsof -i :5173  # Frontend

# Kill process
kill -9 <PID>
```

### Tests Failing Locally

**Solution**:
```bash
# Ensure test database is clean
cd backend
pytest --create-db

# Run with verbose output
pytest -vv
```
```

**Estimated Effort**: 1 hour  
**Priority**: P2 - Documentation

---

## 📊 Summary Metrics

### Effort Breakdown

**Critical Priority (P0)**: 3.5 days
- CI consolidation: 3 hours
- Organization scoping: 1 day
- WebSocket infrastructure: 2 days
- Test DB fix: 2 hours
- Documentation: 1 hour

**High Priority (P1)**: 2 days
- Dependency updates: 4 hours
- Frontend CI: 2 hours
- CodeQL expansion: 1 hour
- Docker Compose: 3 hours
- Security headers: 2 hours

**Medium Priority (P2)**: 1 day
- Documentation improvements: 2.5 hours
- Pre-commit hooks: 1 hour
- Dependabot: 30 minutes

**Total Estimated Effort**: 6.5 days

### Recommended Sprint Plan

**Sprint 1 (Foundation)**: Complete all P0 items
- Days 1-2: Organization scoping + WebSocket infrastructure
- Day 3: CI consolidation + Test DB fix + Documentation
- Goal: Establish architectural foundation

**Sprint 2 (Quality)**: Complete all P1 items
- Days 1-2: Dependency updates + Docker Compose + Frontend CI
- Day 3: CodeQL expansion + Security headers
- Goal: Improve quality and developer experience

**Sprint 3 (Polish)**: Complete P2 items as time allows
- Ongoing: Documentation improvements
- Setup: Pre-commit hooks + Dependabot
- Goal: Long-term maintainability

---

## 🎯 Success Criteria

After completing all P0 and P1 items:

✅ **Development Velocity**:
- Single command starts entire development environment
- CI feedback within 5 minutes for PRs
- No duplicate or redundant workflows

✅ **Code Quality**:
- All code passes linting before commit
- 80% test coverage enforced in CI
- Security scans catch vulnerabilities early

✅ **Architecture Foundation**:
- Multi-tenancy enforced at application layer
- WebSocket infrastructure ready for features
- Real-time communication patterns established

✅ **Security Posture**:
- All major dependencies up to date
- Security headers properly configured
- Automated dependency scanning active

✅ **Developer Experience**:
- Clear documentation for setup and troubleshooting
- Pre-commit hooks catch issues early
- External contributors can run full CI locally

---

*Generated from Code Review dated 2026-02-02*
*Architect: Winston*
