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

