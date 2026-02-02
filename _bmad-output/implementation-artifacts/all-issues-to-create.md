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

