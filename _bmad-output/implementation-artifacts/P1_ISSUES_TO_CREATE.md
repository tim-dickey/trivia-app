# P1 Issues to Create

Copy and paste each section below to create issues manually at:
https://github.com/tim-dickey/trivia-app/issues/new

---

## Issue 1 of 5

**Title:**
```
[P1] Update Outdated Dependencies with Security Patches
```

**Labels:** priority:high, security, dependencies, backend, frontend

**Body:**
```markdown
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
```

---

## Issue 2 of 5

**Title:**
```
[P1] Add Frontend CI Workflow for Quality Validation
```

**Labels:** priority:high, ci/cd, frontend, testing

**Body:**
```markdown
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
```

---

## Issue 3 of 5

**Title:**
```
[P1] Expand CodeQL Security Analysis to Python and TypeScript
```

**Labels:** priority:high, security, ci/cd, codeql

**Body:**
```markdown
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
```

---

## Issue 4 of 5

**Title:**
```
[P1] Add Application Services to Docker Compose
```

**Labels:** priority:high, docker, developer-experience, infrastructure

**Body:**
```markdown
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
```

---

## Issue 5 of 5

**Title:**
```
[P1] Add Security Headers Middleware
```

**Labels:** priority:high, security, backend, middleware

**Body:**
```markdown
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
```

---

