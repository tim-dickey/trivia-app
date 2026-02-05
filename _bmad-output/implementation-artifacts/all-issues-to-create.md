# All 15 Code Review Issues - Ready to Create

This document contains all 15 issues from the code review in a format ready for creation.

**Instructions**:
1. Each issue is separated by `---ISSUE-SEPARATOR---`
2. Copy each section and create as a new GitHub issue
3. Or use the provided scripts to create automatically

---

## ISSUE 1 of 15

**Title**: [P0] Consolidate CI/CD Workflows to Eliminate Duplicate Test Runs

**Labels**: priority:critical, ci/cd, tech-debt

**Body**:

## Problem

Currently, both Codacy and CodeQL workflows run tests on every PR, causing:
- Duplicate test execution (wastes CI/CD minutes)
- Slower PR feedback cycles
- Confusion about which workflow to check

## Impact

- **Efficiency**: CI runs take 2x longer than necessary
- **Cost**: Wastes GitHub Actions minutes
- **Developer Experience**: Slower feedback on PRs

## Proposed Solution

Create a consolidated CI workflow structure:

```yaml
# .github/workflows/ci.yml - Runs on all PRs
- Checkout + Setup
- Backend tests (once)
- Frontend tests  
- Upload results to both Codacy AND CodeQL

# .github/workflows/security-scheduled.yml - Runs on schedule only
- Deep security scans (Bandit, CodeQL, dependency audit)
- Runs weekly + on main branch merges
```

## Acceptance Criteria

- [ ] Single workflow runs tests on PRs
- [ ] No duplicate test executions
- [ ] Coverage reports uploaded to both Codacy and GitHub
- [ ] Security scans run on schedule only
- [ ] PR feedback time reduced by ~50%

## Implementation Details

See: `_bmad-output/implementation-artifacts/action-items-2026-02-02.md` Section 1

**Estimated Effort**: 3 hours  
**Priority**: P0 - Blocks efficient development  
**Source**: Code Review 2026-02-02

---ISSUE-SEPARATOR---

## ISSUE 2 of 15

**Title**: [P0] Implement Organization Scoping Middleware for Multi-Tenancy

**Labels**: priority:critical, security, multi-tenancy, backend

**Body**:

## Problem

Multi-tenant data isolation is not enforced at the application layer. Currently:
- No middleware to automatically filter by `organization_id`
- Developers must manually add filters to every query
- Risk of data leakage between tenants

## Security Risk

**HIGH**: Without automatic scoping, a developer could accidentally:
- Return data from wrong organization
- Allow cross-tenant data access
- Create compliance violations (GDPR, SOC 2)

## Proposed Solution

Implement organization scoping at two levels:

1. **Middleware**: Extract organization from JWT and set in request context
2. **Base CRUD Class**: Automatically filter all queries by organization_id

```python
# backend/core/multi_tenancy.py
async def get_current_organization(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Organization:
    """Extract organization from JWT and validate access"""

# backend/db/crud/base.py  
class MultiTenantCRUD:
    """Base CRUD with automatic organization scoping"""
    def get_multi_for_org(self, db: Session, org_id: int, ...):
        # Auto-filter by organization_id
```

## Acceptance Criteria

- [ ] Middleware extracts organization from JWT
- [ ] Base CRUD class auto-filters by organization_id
- [ ] All existing CRUD operations use base class
- [ ] Integration tests validate tenant isolation
- [ ] Documentation updated with usage examples
- [ ] No queries bypass organization filter

## Implementation Details

See: `_bmad-output/implementation-artifacts/action-items-2026-02-02.md` Section 2

**Estimated Effort**: 1 day (8 hours)  
**Priority**: P0 - Security Critical  
**Source**: Code Review 2026-02-02

---ISSUE-SEPARATOR---

## ISSUE 3 of 15

**Title**: [P0] Implement WebSocket Infrastructure for Real-Time Features

**Labels**: priority:critical, websocket, real-time, backend, frontend

**Body**:

## Problem

Architecture requires real-time features (live scoring, session updates, chat), but no WebSocket infrastructure exists. This blocks:

- Session management
- Live scoring updates
- Real-time participant tracking
- Chat features
- **All MVP core features**

## Impact

**BLOCKS MVP**: Cannot implement any real-time features without this foundation.

## Proposed Solution

Implement WebSocket infrastructure on both backend and frontend:

**Backend** (`backend/websocket/manager.py`):
```python
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        # Connection management
    
    async def broadcast_to_session(self, session_id: str, message: dict):
        # Broadcast to all connections in session
```

**Frontend** (`frontend/src/services/websocket.ts`):
```typescript
export class WebSocketService {
  private ws: WebSocket | null = null;
  
  connect(sessionId: string) {
    this.ws = new WebSocket(`ws://localhost:8000/ws/${sessionId}`);
    // Message handling
  }
}
```

## Acceptance Criteria

- [ ] WebSocket endpoint implemented in FastAPI
- [ ] Connection manager handles multiple sessions
- [ ] Authentication integrated with WebSocket
- [ ] Frontend WebSocket service created
- [ ] Basic message broadcast working
- [ ] Integration tests for WebSocket functionality
- [ ] Documentation with usage examples

## Implementation Details

See: `_bmad-output/implementation-artifacts/action-items-2026-02-02.md` Section 3

**Estimated Effort**: 2 days (16 hours)  
**Priority**: P0 - Blocks MVP  
**Source**: Code Review 2026-02-02

---ISSUE-SEPARATOR---

## ISSUE 4 of 15

**Title**: [P0] Fix Test Database Configuration (PostgreSQL in CI)

**Labels**: priority:critical, testing, ci/cd, backend

**Body**:

## Problem

CI workflows use SQLite for tests while production uses PostgreSQL:

```yaml
# .github/workflows/codacy.yml
DATABASE_URL: sqlite:///./test_trivia.db  # ⚠️ Different from production
```

## Risk

SQLite and PostgreSQL have different SQL dialects and features:
- **PostgreSQL**: Full-text search, array types, JSON operators, specific ALTER TABLE syntax
- **SQLite**: Limited ALTER TABLE, no array types, different JSON handling

**Impact**: Tests may pass in CI but fail in production (or vice versa).

## Proposed Solution

Use PostgreSQL for CI tests via Docker service:

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

jobs:
  test:
    env:
      DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db
    steps:
      - name: Run migrations
        run: cd backend && alembic upgrade head
      - name: Run tests
        run: cd backend && pytest
```

## Acceptance Criteria

- [ ] PostgreSQL service added to CI workflows
- [ ] All tests use PostgreSQL in CI
- [ ] Migrations run before tests
- [ ] Test database properly cleaned between runs
- [ ] No SQLite-specific code in tests

## Implementation Details

See: `_bmad-output/implementation-artifacts/action-items-2026-02-02.md` Section 4

**Estimated Effort**: 2 hours  
**Priority**: P0 - Test Reliability  
**Source**: Code Review 2026-02-02

---ISSUE-SEPARATOR---

## ISSUE 5 of 15

**Title**: [P0] Document Required GitHub Secrets for CI/CD

**Labels**: priority:critical, documentation, ci/cd, contributor-experience

**Body**:

## Problem

Workflows require `CODACY_PROJECT_TOKEN` but there's no documentation on:
- What secrets are needed
- How to obtain them
- How to configure them
- What happens if they're missing

**Impact**: External contributors cannot run full CI pipeline, workflows fail for forks.

## Proposed Solution

1. **Document all required secrets** in `CONTRIBUTING.md`:

```markdown
## CI/CD Setup

### Required GitHub Secrets

For full CI/CD functionality, configure these secrets:

1. **CODACY_PROJECT_TOKEN** (Optional for external contributors)
   - Navigate to: Settings → Secrets → Actions
   - Add secret: `CODACY_PROJECT_TOKEN`
   - Value: Obtain from https://app.codacy.com/

### Running CI Locally

```bash
# Backend tests (no secrets needed)
cd backend && pytest --cov=backend

# Frontend tests
cd frontend && npm test
```
```

2. **Make Codacy optional** in workflows:

```yaml
- name: Upload to Codacy
  if: ${{ secrets.CODACY_PROJECT_TOKEN != '' }}
  uses: codacy/codacy-coverage-reporter-action@v1
```

## Acceptance Criteria

- [ ] All required secrets documented in CONTRIBUTING.md
- [ ] Instructions for obtaining secrets provided
- [ ] Local testing instructions (no secrets needed)
- [ ] Workflows skip optional steps if secrets missing
- [ ] README links to CONTRIBUTING.md CI section
- [ ] External contributors can run CI locally

## Implementation Details

See: `_bmad-output/implementation-artifacts/action-items-2026-02-02.md` Section 5

**Estimated Effort**: 1 hour  
**Priority**: P0 - Blocks Contributions  
**Source**: Code Review 2026-02-02

---ISSUE-SEPARATOR---

## ISSUE 6 of 15

**Title**: [P1] Update Outdated Dependencies with Security Patches

**Labels**: priority:high, security, dependencies, backend, frontend

**Body**:

## Problem

Multiple packages have security updates and performance improvements available:

**Backend**:
- `fastapi`: 0.109.0 → 0.115.0+ (security & performance)
- `pydantic`: 2.12.5 → 2.13.x (security fixes - CVEs)
- `pytest`: 7.4.4 → 8.x (better performance)
- `python-jose`: 3.4.0 has known vulnerabilities

**Frontend**:
- `react`: ^18.2.0 → ^18.3.1
- `vite`: ^5.0.8 → ^5.4.x (security patches)
- `typescript`: ^5.2.2 → ^5.7.x (performance)
- `tailwindcss`: ^3.3.6 → ^3.4.x

## Security Impact

- Pydantic 2.12.5 has known security vulnerabilities
- `python-jose` has CVEs - consider migrating to `PyJWT`
- Vite has security patches in 5.4.x

## Proposed Solution

1. Update backend dependencies in `requirements.txt`
2. Update frontend dependencies in `package.json`
3. Run full test suite after each ecosystem update
4. Document any breaking changes
5. Consider migrating from `python-jose` to `PyJWT`

## Acceptance Criteria

- [ ] All major dependencies updated to latest stable
- [ ] Backend tests pass
- [ ] Frontend tests pass
- [ ] No new deprecation warnings
- [ ] CHANGELOG updated with dependency changes
- [ ] Security scan shows no critical vulnerabilities

## Implementation Details

See: `_bmad-output/implementation-artifacts/action-items-2026-02-02.md` Section 6

**Estimated Effort**: 4 hours (+ testing)  
**Priority**: P1 - Security & Performance  
**Source**: Code Review 2026-02-02

---ISSUE-SEPARATOR---

## ISSUE 7 of 15

**Title**: [P1] Add Frontend CI Workflow for Quality Validation

**Labels**: priority:high, ci/cd, frontend, testing

**Body**:

## Problem

No automated validation of frontend code quality:
- Backend: ✅ Tested in Codacy workflow
- Frontend: ❌ No CI validation

**Risk**: Frontend bugs, type errors, and lint issues won't be caught until deployment.

## Proposed Solution

Create `.github/workflows/frontend-ci.yml` with comprehensive checks:
- Linting (ESLint)
- Type checking (TypeScript)
- Build verification
- Unit tests with coverage
- Coverage upload to Codecov

## Acceptance Criteria

- [ ] Workflow runs on frontend changes
- [ ] All checks pass (lint, type-check, build, test)
- [ ] Coverage reports uploaded
- [ ] Workflow badge added to README
- [ ] Runs within 5 minutes

## Implementation Details

See: `_bmad-output/implementation-artifacts/action-items-2026-02-02.md` Section 7

**Estimated Effort**: 2 hours  
**Priority**: P1 - Quality Assurance  
**Source**: Code Review 2026-02-02

---ISSUE-SEPARATOR---

## ISSUE 8 of 15

**Title**: [P1] Expand CodeQL Security Analysis to Python and TypeScript

**Labels**: priority:high, security, ci/cd, codeql

**Body**:

## Problem

CodeQL workflow only analyzes GitHub Actions, not application code.

**Security Gap**: Python and TypeScript code vulnerabilities won't be detected.

## Proposed Solution

Expand CodeQL analysis to cover all languages:

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

## Security Benefits

CodeQL will detect:
- SQL injection vulnerabilities
- XSS vulnerabilities
- Authentication bypasses
- Insecure cryptography
- Path traversal issues
- And 200+ other vulnerability types

## Acceptance Criteria

- [ ] Python analysis enabled
- [ ] JavaScript/TypeScript analysis enabled
- [ ] First scan completes successfully
- [ ] Security issues (if any) documented
- [ ] False positives marked and justified
- [ ] Results appear in Security tab

## Implementation Details

See: `_bmad-output/implementation-artifacts/action-items-2026-02-02.md` Section 8

**Estimated Effort**: 1 hour  
**Priority**: P1 - Security Scanning  
**Source**: Code Review 2026-02-02

---ISSUE-SEPARATOR---

## ISSUE 9 of 15

**Title**: [P1] Add Application Services to Docker Compose

**Labels**: priority:high, docker, developer-experience, infrastructure

**Body**:

## Problem

`docker-compose.yml` only defines infrastructure (PostgreSQL, Redis), not application services. Developers must:
- Manually run backend in one terminal
- Manually run frontend in another terminal
- Remember 4+ commands to start development environment

**Poor Developer Experience**: No unified development startup.

## Proposed Solution

Add backend and frontend services to `docker-compose.yml` with:
- Hot reload for both services
- Automatic dependency management
- Health checks
- Proper volume mounting

## Acceptance Criteria

- [ ] Single `docker-compose up` starts everything
- [ ] Hot reload works for backend and frontend
- [ ] Database migrations run automatically
- [ ] README updated with Docker instructions
- [ ] Development environment starts in <2 minutes

## Implementation Details

See: `_bmad-output/implementation-artifacts/action-items-2026-02-02.md` Section 9

**Estimated Effort**: 3 hours  
**Priority**: P1 - Developer Experience  
**Source**: Code Review 2026-02-02

---ISSUE-SEPARATOR---

## ISSUE 10 of 15

**Title**: [P1] Add Security Headers Middleware

**Labels**: priority:high, security, backend, middleware

**Body**:

## Problem

Missing common security headers:
- No HSTS (HTTP Strict Transport Security)
- No CSP (Content Security Policy)
- No X-Frame-Options (clickjacking protection)
- No X-Content-Type-Options
- No X-XSS-Protection

**Security Risk**: Application vulnerable to common attacks.

## Security Best Practices

- **HSTS**: Force HTTPS connections
- **CSP**: Prevent XSS attacks by restricting resource loading
- **X-Frame-Options**: Prevent clickjacking
- **X-Content-Type-Options**: Prevent MIME sniffing attacks

## Proposed Solution

Create security headers middleware in `backend/core/security_middleware.py` and integrate with FastAPI application.

## Acceptance Criteria

- [ ] All security headers present in responses
- [ ] CSP policy doesn't break functionality
- [ ] Tests verify headers are set correctly
- [ ] Documentation explains each header
- [ ] Security scan shows improved rating

## Implementation Details

See: `_bmad-output/implementation-artifacts/action-items-2026-02-02.md` Section 10

**Estimated Effort**: 2 hours  
**Priority**: P1 - Security Hardening  
**Source**: Code Review 2026-02-02

---ISSUE-SEPARATOR---

## ISSUE 11 of 15

**Title**: [P2] Add Quick Start Section to README

**Labels**: priority:medium, documentation, developer-experience

**Body**:

## Problem

README is comprehensive but lacks quick start at the top. Users must read extensive documentation before running the application.

## Proposed Solution

Add quick start section at top of README.md with:
- One-command Docker startup
- Manual setup steps
- Access URLs for frontend, backend, and API docs

## Acceptance Criteria

- [ ] Quick start section added at top of README
- [ ] Single-command option documented
- [ ] Manual setup documented
- [ ] All commands tested and work
- [ ] Time-to-first-run < 5 minutes for new contributors

## Implementation Details

See: `_bmad-output/implementation-artifacts/action-items-2026-02-02.md` Section 11

**Estimated Effort**: 15 minutes  
**Priority**: P2 - Documentation  
**Source**: Code Review 2026-02-02

---ISSUE-SEPARATOR---

## ISSUE 12 of 15

**Title**: [P2] Create Architecture Diagram

**Labels**: priority:medium, documentation, architecture

**Body**:

## Problem

Architecture document is text-heavy with no visual representation. Diagrams improve understanding.

## Proposed Solution

Create Mermaid or Excalidraw diagram showing:
- System components (Frontend, Backend, Database, Redis, Celery)
- Data flow for key operations
- External integrations (Slack, Teams, AI)
- Multi-tenant isolation

## Acceptance Criteria

- [ ] High-level architecture diagram created
- [ ] Embedded in architecture.md
- [ ] Shows all major components
- [ ] Data flow clearly illustrated
- [ ] Multi-tenancy boundaries shown

## Implementation Details

See: `_bmad-output/implementation-artifacts/action-items-2026-02-02.md` Section 12

**Estimated Effort**: 1 hour  
**Priority**: P2 - Documentation  
**Source**: Code Review 2026-02-02

---ISSUE-SEPARATOR---

## ISSUE 13 of 15

**Title**: [P2] Add Pre-commit Hooks for Code Quality

**Labels**: priority:medium, code-quality, developer-experience

**Body**:

## Problem

Code quality checks only run in CI, not locally. Developers push code that fails CI checks.

## Proposed Solution

Install pre-commit hooks with:
- Black (Python formatting)
- Ruff (Python linting)
- ESLint (JavaScript/TypeScript)
- Trailing whitespace checks
- YAML/JSON validation
- Secret detection

## Acceptance Criteria

- [ ] Pre-commit hooks configured
- [ ] Installation instructions in CONTRIBUTING.md
- [ ] Hooks run before commits
- [ ] CI checks match pre-commit checks
- [ ] Hooks can be bypassed with --no-verify if needed

## Implementation Details

See: `_bmad-output/implementation-artifacts/action-items-2026-02-02.md` Section 13

**Estimated Effort**: 1 hour  
**Priority**: P2 - Developer Experience  
**Source**: Code Review 2026-02-02

---ISSUE-SEPARATOR---

## ISSUE 14 of 15

**Title**: [P2] Configure Dependabot for Automated Dependency Updates

**Labels**: priority:medium, dependencies, automation

**Body**:

## Problem

No automated dependency update notifications. Security patches and updates are missed.

## Proposed Solution

Create `.github/dependabot.yml` with:
- Python (pip) updates for backend
- npm updates for frontend
- GitHub Actions updates
- Weekly schedule
- Automatic PR creation with proper labels

## Acceptance Criteria

- [ ] Dependabot configured for all ecosystems
- [ ] Weekly PRs created automatically
- [ ] Proper labels and reviewers assigned
- [ ] Documentation explains workflow
- [ ] Auto-merge configured for patch updates (optional)

## Implementation Details

See: `_bmad-output/implementation-artifacts/action-items-2026-02-02.md` Section 14

**Estimated Effort**: 30 minutes  
**Priority**: P2 - Automation  
**Source**: Code Review 2026-02-02

---ISSUE-SEPARATOR---

## ISSUE 15 of 15

**Title**: [P2] Add Troubleshooting Guide to Documentation

**Labels**: priority:medium, documentation, developer-experience

**Body**:

## Problem

No documentation for common development issues. Developers waste time solving known problems.

## Proposed Solution

Create troubleshooting section covering:
- Database connection issues
- Frontend/backend connection problems
- Migration errors
- Port conflicts
- Test failures
- Common setup problems

## Acceptance Criteria

- [ ] Troubleshooting guide created
- [ ] Covers 10+ common issues
- [ ] Solutions tested and verified
- [ ] Linked from README
- [ ] Easy to find and search

## Implementation Details

See: `_bmad-output/implementation-artifacts/action-items-2026-02-02.md` Section 15

**Estimated Effort**: 1 hour  
**Priority**: P2 - Documentation  
**Source**: Code Review 2026-02-02

---ISSUE-SEPARATOR---

