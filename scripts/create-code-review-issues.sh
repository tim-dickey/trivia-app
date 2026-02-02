#!/bin/bash
# Script to create GitHub issues for code review findings
# Generated: 2026-02-02
# Source: Code Review of PR #20

set -e

REPO="tim-dickey/trivia-app"

echo "Creating GitHub issues for code review findings..."
echo "Repository: $REPO"
echo ""

# Check if gh is authenticated
if ! gh auth status &>/dev/null; then
    echo "ERROR: GitHub CLI is not authenticated."
    echo "This script requires GitHub authentication."
    echo ""
    echo "Please run: gh auth login"
    echo ""
    echo "Exiting script due to missing GitHub authentication."
    exit 1
fi

# Array to store created issue numbers
declare -a ISSUE_NUMBERS=()
SUCCESS_COUNT=0

# Function to create an issue
create_issue() {
    local title="$1"
    local body="$2"
    local labels="$3"
    
    echo "Creating: $title"
    
    issue_url=$(gh issue create \
        --repo "$REPO" \
        --title "$title" \
        --body "$body" \
        --label "$labels" \
        2>&1)
    
    if [ $? -eq 0 ]; then
        echo "✓ Created: $issue_url"
        issue_num=$(echo "$issue_url" | grep -oP '/issues/\K[0-9]+' || echo "unknown")
        ISSUE_NUMBERS+=("$issue_num|$title")
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
        echo ""
        sleep 1
    else
        echo "✗ Failed: $title"
        echo ""
    fi
}

echo "Creating P0 (Critical) Issues..."
echo "================================"
echo ""

# P0-1: Consolidate CI/CD Workflows
create_issue "[P0] Consolidate CI/CD Workflows to Eliminate Duplicate Test Runs" \
"## Problem

Currently, both Codacy and CodeQL workflows run tests on every PR, causing:
- Duplicate test execution (wastes CI/CD minutes)
- Slower PR feedback cycles
- Confusion about which workflow to check

## Impact

- **Efficiency**: CI runs take 2x longer than necessary
- **Cost**: Wastes GitHub Actions minutes
- **Developer Experience**: Slower feedback on PRs

## Proposed Solution

Create a consolidated CI workflow structure.

## Acceptance Criteria

- [ ] Single workflow runs tests on PRs
- [ ] No duplicate test executions
- [ ] Coverage reports uploaded to both Codacy and GitHub
- [ ] Security scans run on schedule only

**Estimated Effort**: 3 hours
**Priority**: P0 - Blocks efficient development
**Source**: Code Review 2026-02-02

See: \`_bmad-output/implementation-artifacts/action-items-2026-02-02.md\` Section 1" \
"priority:critical,ci/cd,tech-debt"

# P0-2: Organization Scoping Middleware  
create_issue "[P0] Implement Organization Scoping Middleware for Multi-Tenancy" \
"## Problem

Multi-tenant data isolation not enforced at application layer.

## Security Risk

**HIGH**: Risk of data leakage between tenants.

## Proposed Solution

Implement organization scoping middleware and base CRUD class.

## Acceptance Criteria

- [ ] Middleware extracts organization from JWT
- [ ] Base CRUD class auto-filters by organization_id
- [ ] Integration tests validate tenant isolation

**Estimated Effort**: 1 day
**Priority**: P0 - Security Critical
**Source**: Code Review 2026-02-02

See: \`_bmad-output/implementation-artifacts/action-items-2026-02-02.md\` Section 2" \
"priority:critical,security,multi-tenancy,backend"

# P0-3: WebSocket Infrastructure
create_issue "[P0] Implement WebSocket Infrastructure for Real-Time Features" \
"## Problem

Architecture requires real-time features but no WebSocket infrastructure exists.

## Impact

**BLOCKS MVP**: Cannot implement real-time features without this foundation.

## Proposed Solution

Implement WebSocket infrastructure on backend and frontend.

## Acceptance Criteria

- [ ] WebSocket endpoint implemented in FastAPI
- [ ] Connection manager handles multiple sessions
- [ ] Frontend WebSocket service created
- [ ] Basic message broadcast working

**Estimated Effort**: 2 days
**Priority**: P0 - Blocks MVP
**Source**: Code Review 2026-02-02

See: \`_bmad-output/implementation-artifacts/action-items-2026-02-02.md\` Section 3" \
"priority:critical,websocket,real-time,backend,frontend"

# P0-4: Test Database Configuration
create_issue "[P0] Fix Test Database Configuration (PostgreSQL in CI)" \
"## Problem

CI uses SQLite while production uses PostgreSQL.

## Risk

Tests may pass in CI but fail in production.

## Proposed Solution

Use PostgreSQL for CI tests via Docker service.

## Acceptance Criteria

- [ ] PostgreSQL service added to CI workflows
- [ ] All tests use PostgreSQL in CI
- [ ] Migrations run before tests

**Estimated Effort**: 2 hours
**Priority**: P0 - Test Reliability
**Source**: Code Review 2026-02-02

See: \`_bmad-output/implementation-artifacts/action-items-2026-02-02.md\` Section 4" \
"priority:critical,testing,ci/cd,backend"

# P0-5: GitHub Secrets Documentation
create_issue "[P0] Document Required GitHub Secrets for CI/CD" \
"## Problem

Workflows require secrets but no documentation exists.

## Impact

External contributors cannot run full CI pipeline.

## Proposed Solution

Document all required secrets and make Codacy optional.

## Acceptance Criteria

- [ ] All required secrets documented
- [ ] Workflows skip optional steps if secrets missing
- [ ] External contributors can run CI locally

**Estimated Effort**: 1 hour
**Priority**: P0 - Blocks Contributions
**Source**: Code Review 2026-02-02

See: \`_bmad-output/implementation-artifacts/action-items-2026-02-02.md\` Section 5" \
"priority:critical,documentation,ci/cd,contributor-experience"

echo ""
echo "Creating P1 (High) Issues..."
echo "============================"
echo ""

# P1-6: Update Dependencies
create_issue "[P1] Update Outdated Dependencies with Security Patches" \
"## Problem

Multiple packages have security updates and performance improvements available.

## Packages to Update

Backend: fastapi, pydantic, pytest
Frontend: react, vite, typescript, tailwindcss

## Acceptance Criteria

- [ ] All major dependencies updated to latest stable
- [ ] Tests pass on both backend and frontend
- [ ] No new deprecation warnings

**Estimated Effort**: 4 hours
**Priority**: P1 - Security & Performance
**Source**: Code Review 2026-02-02

See: \`_bmad-output/implementation-artifacts/action-items-2026-02-02.md\` Section 6" \
"priority:high,security,dependencies,backend,frontend"

# P1-7: Frontend CI
create_issue "[P1] Add Frontend CI Workflow for Quality Validation" \
"## Problem

No automated validation of frontend code quality.

## Proposed Solution

Create .github/workflows/frontend-ci.yml with lint, type-check, build, and test steps.

## Acceptance Criteria

- [ ] Workflow runs on frontend changes
- [ ] All checks pass
- [ ] Coverage reports uploaded

**Estimated Effort**: 2 hours
**Priority**: P1 - Quality Assurance
**Source**: Code Review 2026-02-02

See: \`_bmad-output/implementation-artifacts/action-items-2026-02-02.md\` Section 7" \
"priority:high,ci/cd,frontend,testing"

# P1-8: CodeQL Expansion
create_issue "[P1] Expand CodeQL Security Analysis to Python and TypeScript" \
"## Problem

CodeQL only analyzes GitHub Actions, not application code.

## Security Gap

Python and TypeScript vulnerabilities won't be detected.

## Acceptance Criteria

- [ ] Python analysis enabled
- [ ] JavaScript/TypeScript analysis enabled
- [ ] First scan completes successfully

**Estimated Effort**: 1 hour
**Priority**: P1 - Security Scanning
**Source**: Code Review 2026-02-02

See: \`_bmad-output/implementation-artifacts/action-items-2026-02-02.md\` Section 8" \
"priority:high,security,ci/cd,codeql"

# P1-9: Docker Compose Services
create_issue "[P1] Add Application Services to Docker Compose" \
"## Problem

docker-compose.yml only has infrastructure, not application services.

## Developer Pain Point

Must manually run multiple commands in different terminals.

## Acceptance Criteria

- [ ] Single docker-compose up starts everything
- [ ] Hot reload works for backend and frontend
- [ ] Database migrations run automatically

**Estimated Effort**: 3 hours
**Priority**: P1 - Developer Experience
**Source**: Code Review 2026-02-02

See: \`_bmad-output/implementation-artifacts/action-items-2026-02-02.md\` Section 9" \
"priority:high,docker,developer-experience,infrastructure"

# P1-10: Security Headers
create_issue "[P1] Add Security Headers Middleware" \
"## Problem

Missing common security headers (HSTS, CSP, X-Frame-Options).

## Security Risk

Application vulnerable to common attacks.

## Acceptance Criteria

- [ ] All security headers present in responses
- [ ] CSP policy doesn't break functionality
- [ ] Tests verify headers are set correctly

**Estimated Effort**: 2 hours
**Priority**: P1 - Security Hardening
**Source**: Code Review 2026-02-02

See: \`_bmad-output/implementation-artifacts/action-items-2026-02-02.md\` Section 10" \
"priority:high,security,backend,middleware"

echo ""
echo "Creating P2 (Medium) Issues..."
echo "=============================="
echo ""

# P2-11: Quick Start README
create_issue "[P2] Add Quick Start Section to README" \
"## Problem

README lacks quick start at the top.

## Acceptance Criteria

- [ ] Quick start section added at top of README
- [ ] Single-command option documented
- [ ] Manual setup documented

**Estimated Effort**: 15 minutes
**Priority**: P2 - Documentation
**Source**: Code Review 2026-02-02

See: \`_bmad-output/implementation-artifacts/action-items-2026-02-02.md\` Section 11" \
"priority:medium,documentation,developer-experience"

# P2-12: Architecture Diagram
create_issue "[P2] Create Architecture Diagram" \
"## Problem

Architecture document is text-heavy with no visual representation.

## Acceptance Criteria

- [ ] High-level architecture diagram created
- [ ] Embedded in architecture.md
- [ ] Shows all major components

**Estimated Effort**: 1 hour
**Priority**: P2 - Documentation
**Source**: Code Review 2026-02-02

See: \`_bmad-output/implementation-artifacts/action-items-2026-02-02.md\` Section 12" \
"priority:medium,documentation,architecture"

# P2-13: Pre-commit Hooks
create_issue "[P2] Add Pre-commit Hooks for Code Quality" \
"## Problem

Code quality checks only run in CI, not locally.

## Acceptance Criteria

- [ ] Pre-commit hooks configured
- [ ] Installation instructions in CONTRIBUTING.md
- [ ] Hooks run before commits

**Estimated Effort**: 1 hour
**Priority**: P2 - Developer Experience
**Source**: Code Review 2026-02-02

See: \`_bmad-output/implementation-artifacts/action-items-2026-02-02.md\` Section 13" \
"priority:medium,code-quality,developer-experience"

# P2-14: Dependabot
create_issue "[P2] Configure Dependabot for Automated Dependency Updates" \
"## Problem

No automated dependency update notifications.

## Acceptance Criteria

- [ ] Dependabot configured for all ecosystems
- [ ] Weekly PRs created automatically
- [ ] Proper labels assigned

**Estimated Effort**: 30 minutes
**Priority**: P2 - Automation
**Source**: Code Review 2026-02-02

See: \`_bmad-output/implementation-artifacts/action-items-2026-02-02.md\` Section 14" \
"priority:medium,dependencies,automation"

# P2-15: Troubleshooting Guide
create_issue "[P2] Add Troubleshooting Guide to Documentation" \
"## Problem

No documentation for common development issues.

## Acceptance Criteria

- [ ] Troubleshooting guide created
- [ ] Covers 10+ common issues
- [ ] Solutions tested and verified

**Estimated Effort**: 1 hour
**Priority**: P2 - Documentation
**Source**: Code Review 2026-02-02

See: \`_bmad-output/implementation-artifacts/action-items-2026-02-02.md\` Section 15" \
"priority:medium,documentation,developer-experience"

echo ""
echo "Issue creation requests submitted."
echo "Total issues attempted: 15"
echo "Successful creations: $SUCCESS_COUNT"
