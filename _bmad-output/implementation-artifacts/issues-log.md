# Issues Log - Trivia App

**Version**: 1.0  
**Created**: 2026-02-02  
**Last Updated**: 2026-02-02  
**Repository**: tim-dickey/trivia-app

---

## Overview

This document provides a consolidated, trackable log of all identified issues from various sources. It serves as a single source of truth for issue tracking and GitHub issue creation.

### Summary Statistics

| Metric | Value |
|--------|-------|
| **Total Issues** | 20 |
| **Critical (P0)** | 5 |
| **High Priority (P1)** | 5 |
| **Medium Priority (P2)** | 10 |
| **Total Effort** | 47.25 hours (5.9 days) |
| **GitHub Issues Created** | 0 |

### By Source

| Source | Count |
|--------|-------|
| Code Review 2026-02-02 (PR #20) | 15 |
| PRD Validation Report 2026-01-24 | 5 |

### By Category

| Category | Count |
|----------|-------|
| Documentation | 7 |
| Requirements | 5 |
| Security | 4 |
| CI/CD | 3 |
| Testing | 2 |
| Dependencies | 2 |
| Real-time | 1 |
| Docker | 1 |
| Code Quality | 1 |
| Automation | 1 |

---

## 🔴 P0 - Critical Priority Issues (5 issues, 2.6 days)

### LOG-001: [P0] Consolidate CI/CD Workflows to Eliminate Duplicate Test Runs
- **Source**: code-review-2026-02-02 (P0-1)
- **Category**: ci/cd
- **Effort**: 3 hours
- **Status**: Open
- **GitHub Issue**: Not created
- **Labels**: priority:critical, ci/cd, tech-debt

**Description**: Currently, both Codacy and CodeQL workflows run tests on every PR, causing duplicate test execution, slower PR feedback cycles, and confusion about which workflow to check.

**Acceptance Criteria**:
- [ ] Single workflow runs tests on PRs
- [ ] No duplicate test executions
- [ ] Coverage reports uploaded to both Codacy and GitHub
- [ ] Security scans run on schedule only
- [ ] PR feedback time reduced by ~50%

---

### LOG-002: [P0] Implement Organization Scoping Middleware for Multi-Tenancy
- **Source**: code-review-2026-02-02 (P0-2)
- **Category**: security
- **Effort**: 8 hours
- **Status**: Open
- **GitHub Issue**: Not created
- **Labels**: priority:critical, security, multi-tenancy, backend

**Description**: Multi-tenant data isolation is not enforced at the application layer. No middleware to automatically filter by organization_id, requiring developers to manually add filters to every query, creating risk of data leakage between tenants.

**Blocks**: feature-development, data-security

**Acceptance Criteria**:
- [ ] Middleware extracts organization from JWT
- [ ] Base CRUD class auto-filters by organization_id
- [ ] All existing CRUD operations use base class
- [ ] Integration tests validate tenant isolation
- [ ] Documentation updated with usage examples
- [ ] No queries bypass organization filter

---

### LOG-003: [P0] Implement WebSocket Infrastructure for Real-Time Features
- **Source**: code-review-2026-02-02 (P0-3)
- **Category**: real-time
- **Effort**: 16 hours
- **Status**: Open
- **GitHub Issue**: Not created
- **Labels**: priority:critical, websocket, real-time, backend, frontend

**Description**: Architecture requires real-time features (live scoring, session updates, chat), but no WebSocket infrastructure exists. This blocks all MVP core features including session management, live scoring updates, and real-time participant tracking.

**Blocks**: mvp-features, session-management, live-scoring

**Acceptance Criteria**:
- [ ] WebSocket endpoint implemented in FastAPI
- [ ] Connection manager handles multiple sessions
- [ ] Authentication integrated with WebSocket
- [ ] Frontend WebSocket service created
- [ ] Basic message broadcast working
- [ ] Integration tests for WebSocket functionality
- [ ] Documentation with usage examples

---

### LOG-004: [P0] Fix Test Database Configuration (PostgreSQL in CI)
- **Source**: code-review-2026-02-02 (P0-4)
- **Category**: testing
- **Effort**: 2 hours
- **Status**: Open
- **GitHub Issue**: Not created
- **Labels**: priority:critical, testing, ci/cd, backend

**Description**: CI workflows use SQLite for tests while production uses PostgreSQL. This creates risk that tests may pass in CI but fail in production due to different SQL dialects and features (full-text search, array types, JSON operators, ALTER TABLE syntax).

**Blocks**: test-reliability

**Acceptance Criteria**:
- [ ] PostgreSQL service added to CI workflows
- [ ] All tests use PostgreSQL in CI
- [ ] Migrations run before tests
- [ ] Test database properly cleaned between runs
- [ ] No SQLite-specific code in tests

---

### LOG-005: [P0] Document Required GitHub Secrets for CI/CD
- **Source**: code-review-2026-02-02 (P0-5)
- **Category**: documentation
- **Effort**: 1 hour
- **Status**: Open
- **GitHub Issue**: Not created
- **Labels**: priority:critical, documentation, ci/cd, contributor-experience

**Description**: Workflows require CODACY_PROJECT_TOKEN but there's no documentation on what secrets are needed, how to obtain them, how to configure them, or what happens if they're missing. This prevents external contributors from running the full CI pipeline.

**Blocks**: external-contributions

**Acceptance Criteria**:
- [ ] All required secrets documented in CONTRIBUTING.md
- [ ] Instructions for obtaining secrets provided
- [ ] Local testing instructions (no secrets needed)
- [ ] Workflows skip optional steps if secrets missing
- [ ] README links to CONTRIBUTING.md CI section
- [ ] External contributors can run CI locally

---

## 🟡 P1 - High Priority Issues (5 issues, 2 days)

### LOG-006: [P1] Update Outdated Dependencies with Security Patches
- **Source**: code-review-2026-02-02 (P1-1)
- **Category**: dependencies
- **Effort**: 4 hours
- **Status**: Open
- **GitHub Issue**: Not created
- **Labels**: priority:high, security, dependencies, backend, frontend

**Description**: Multiple packages have security updates available: fastapi 0.109.0 → 0.115.0+, pydantic 2.12.5 → 2.13.x (CVEs), python-jose has known vulnerabilities, vite has security patches in 5.4.x, and other updates for performance improvements.

**Acceptance Criteria**:
- [ ] All major dependencies updated to latest stable
- [ ] Backend tests pass
- [ ] Frontend tests pass
- [ ] No new deprecation warnings
- [ ] CHANGELOG updated with dependency changes
- [ ] Security scan shows no critical vulnerabilities

---

### LOG-007: [P1] Add Frontend CI Workflow for Quality Validation
- **Source**: code-review-2026-02-02 (P1-2)
- **Category**: ci/cd
- **Effort**: 2 hours
- **Status**: Open
- **GitHub Issue**: Not created
- **Labels**: priority:high, ci/cd, frontend, testing

**Description**: No automated validation of frontend code quality. Backend is tested in Codacy workflow but frontend has no CI validation, allowing bugs, type errors, and lint issues to reach deployment.

**Acceptance Criteria**:
- [ ] Workflow runs on frontend changes
- [ ] All checks pass (lint, type-check, build, test)
- [ ] Coverage reports uploaded
- [ ] Workflow badge added to README
- [ ] Runs within 5 minutes

---

### LOG-008: [P1] Expand CodeQL Security Analysis to Python and TypeScript
- **Source**: code-review-2026-02-02 (P1-3)
- **Category**: security
- **Effort**: 1 hour
- **Status**: Open
- **GitHub Issue**: Not created
- **Labels**: priority:high, security, ci/cd, codeql

**Description**: CodeQL workflow only analyzes GitHub Actions, not application code. Python and TypeScript code vulnerabilities won't be detected (SQL injection, XSS, authentication bypasses, insecure cryptography, path traversal).

**Acceptance Criteria**:
- [ ] Python analysis enabled
- [ ] JavaScript/TypeScript analysis enabled
- [ ] First scan completes successfully
- [ ] Security issues (if any) documented
- [ ] False positives marked and justified
- [ ] Results appear in Security tab

---

### LOG-009: [P1] Add Application Services to Docker Compose
- **Source**: code-review-2026-02-02 (P1-4)
- **Category**: docker
- **Effort**: 3 hours
- **Status**: Open
- **GitHub Issue**: Not created
- **Labels**: priority:high, docker, developer-experience, infrastructure

**Description**: docker-compose.yml only defines infrastructure (PostgreSQL, Redis), not application services. Developers must manually run backend and frontend in separate terminals, remembering 4+ commands for startup.

**Acceptance Criteria**:
- [ ] Single 'docker-compose up' starts everything
- [ ] Hot reload works for backend and frontend
- [ ] Database migrations run automatically
- [ ] README updated with Docker instructions
- [ ] Development environment starts in <2 minutes

---

### LOG-010: [P1] Add Security Headers Middleware
- **Source**: code-review-2026-02-02 (P1-5)
- **Category**: security
- **Effort**: 2 hours
- **Status**: Open
- **GitHub Issue**: Not created
- **Labels**: priority:high, security, backend, middleware

**Description**: Missing common security headers: HSTS, CSP, X-Frame-Options, X-Content-Type-Options, X-XSS-Protection. Application is vulnerable to common attacks including clickjacking, XSS, and MIME sniffing.

**Acceptance Criteria**:
- [ ] All security headers present in responses
- [ ] CSP policy doesn't break functionality
- [ ] Tests verify headers are set correctly
- [ ] Documentation explains each header
- [ ] Security scan shows improved rating

---

## 🟢 P2 - Medium Priority Issues (10 issues, 3.75 hours)

### LOG-011: [P2] Add Quick Start Section to README
- **Source**: code-review-2026-02-02 (P2-1)
- **Category**: documentation
- **Effort**: 0.25 hours (15 minutes)
- **Status**: Open
- **GitHub Issue**: Not created
- **Labels**: priority:medium, documentation, developer-experience

**Description**: README is comprehensive but lacks quick start at the top. Users must read extensive documentation before running the application.

**Acceptance Criteria**:
- [ ] Quick start section added at top of README
- [ ] Single-command option documented
- [ ] Manual setup documented
- [ ] All commands tested and work
- [ ] Time-to-first-run < 5 minutes for new contributors

---

### LOG-012: [P2] Create Architecture Diagram
- **Source**: code-review-2026-02-02 (P2-2)
- **Category**: documentation
- **Effort**: 1 hour
- **Status**: Open
- **GitHub Issue**: Not created
- **Labels**: priority:medium, documentation, architecture

**Description**: Architecture document is text-heavy with no visual representation. Diagrams improve understanding of system components, data flow, external integrations, and multi-tenant isolation.

**Acceptance Criteria**:
- [ ] High-level architecture diagram created
- [ ] Embedded in architecture.md
- [ ] Shows all major components
- [ ] Data flow clearly illustrated
- [ ] Multi-tenancy boundaries shown

---

### LOG-013: [P2] Add Pre-commit Hooks for Code Quality
- **Source**: code-review-2026-02-02 (P2-3)
- **Category**: code-quality
- **Effort**: 1 hour
- **Status**: Open
- **GitHub Issue**: Not created
- **Labels**: priority:medium, code-quality, developer-experience

**Description**: Code quality checks only run in CI, not locally. Developers push code that fails CI checks, wasting time and CI minutes.

**Acceptance Criteria**:
- [ ] Pre-commit hooks configured
- [ ] Installation instructions in CONTRIBUTING.md
- [ ] Hooks run before commits
- [ ] CI checks match pre-commit checks
- [ ] Hooks can be bypassed with --no-verify if needed

---

### LOG-014: [P2] Configure Dependabot for Automated Dependency Updates
- **Source**: code-review-2026-02-02 (P2-4)
- **Category**: automation
- **Effort**: 0.5 hours (30 minutes)
- **Status**: Open
- **GitHub Issue**: Not created
- **Labels**: priority:medium, dependencies, automation

**Description**: No automated dependency update notifications. Security patches and updates are missed, requiring manual monitoring.

**Acceptance Criteria**:
- [ ] Dependabot configured for all ecosystems
- [ ] Weekly PRs created automatically
- [ ] Proper labels and reviewers assigned
- [ ] Documentation explains workflow
- [ ] Auto-merge configured for patch updates (optional)

---

### LOG-015: [P2] Add Troubleshooting Guide to Documentation
- **Source**: code-review-2026-02-02 (P2-5)
- **Category**: documentation
- **Effort**: 1 hour
- **Status**: Open
- **GitHub Issue**: Not created
- **Labels**: priority:medium, documentation, developer-experience

**Description**: No documentation for common development issues. Developers waste time solving known problems like database connection issues, port conflicts, migration errors, and test failures.

**Acceptance Criteria**:
- [ ] Troubleshooting guide created
- [ ] Covers 10+ common issues
- [ ] Solutions tested and verified
- [ ] Linked from README
- [ ] Easy to find and search

---

### LOG-016: [P2] Replace Subjective Adjectives in Functional Requirements
- **Source**: prd-validation-2026-01-24 (VAL-FR-01)
- **Category**: requirements
- **Effort**: 0.5 hours (30 minutes)
- **Status**: Open
- **GitHub Issue**: Not created
- **Labels**: priority:medium, documentation, requirements, prd

**Description**: PRD validation found 8 subjective adjectives in acceptance criteria that should be replaced with measurable criteria: 'quickly' (should specify time), 'clearly' (should specify readability), 'relevant and interesting' (subjective), 'clear and simple' (subjective), 'confusing' (subjective).

**Acceptance Criteria**:
- [ ] All 8 subjective adjectives replaced with quantitative criteria
- [ ] Line 167: 'quickly form teams' → specify time target (e.g., <30 seconds)
- [ ] Line 170: 'display clearly' → specify readability criteria
- [ ] Line 181: 'clearly clickable' → specify touch target size/contrast
- [ ] Line 304: 'relevant and interesting' → specify measurable engagement criteria
- [ ] Line 461: 'clear and simple' → specify measurable complexity metrics
- [ ] Line 466: 'No confusing options' → specify usability criteria
- [ ] PRD updated and validated

---

### LOG-017: [P2] Add Measurement Methods to NFR Security Requirements
- **Source**: prd-validation-2026-01-24 (VAL-NFR-01)
- **Category**: requirements
- **Effort**: 0.25 hours (15 minutes)
- **Status**: Open
- **GitHub Issue**: Not created
- **Labels**: priority:medium, documentation, requirements, security, prd

**Description**: Security requirements (lines 699-709) list techniques but some lack measurement methods. Need to specify how each security requirement will be validated and tested.

**Acceptance Criteria**:
- [ ] Each security requirement includes measurement method
- [ ] Validation approach documented for JWT authentication
- [ ] Testing methodology specified for password hashing
- [ ] Verification criteria for organization-level isolation
- [ ] PRD updated with measurement methods

---

### LOG-018: [P2] Add Detailed Measurement to Scalability Requirements
- **Source**: prd-validation-2026-01-24 (VAL-NFR-02)
- **Category**: requirements
- **Effort**: 0.25 hours (15 minutes)
- **Status**: Open
- **GitHub Issue**: Not created
- **Labels**: priority:medium, documentation, requirements, scalability, prd

**Description**: Scalability requirements (lines 711-717) could specify more detailed measurement approaches for validating system can handle 5000+ concurrent users and scale across multiple organizations.

**Acceptance Criteria**:
- [ ] Load testing methodology specified
- [ ] Performance benchmarks defined for concurrent users
- [ ] Multi-tenant scaling metrics documented
- [ ] Measurement tools identified (e.g., JMeter, k6)
- [ ] PRD updated with detailed measurement approaches

---

### LOG-019: [P2] Add Testing Methodology for Browser Support Requirements
- **Source**: prd-validation-2026-01-24 (VAL-NFR-03)
- **Category**: requirements
- **Effort**: 0.25 hours (15 minutes)
- **Status**: Open
- **GitHub Issue**: Not created
- **Labels**: priority:medium, documentation, requirements, testing, prd

**Description**: Browser support requirements (lines 729-737) could benefit from testing methodology specification for validating cross-browser compatibility and mobile responsiveness.

**Acceptance Criteria**:
- [ ] Cross-browser testing methodology documented
- [ ] Browser matrix specified (versions to test)
- [ ] Testing tools identified (BrowserStack, Playwright)
- [ ] Mobile testing approach defined
- [ ] PRD updated with testing methodology

---

### LOG-020: [P2] Add Dedicated Product Scope Section to PRD
- **Source**: prd-validation-2026-01-24 (VAL-SCOPE-01)
- **Category**: requirements
- **Effort**: 0.25 hours (15 minutes)
- **Status**: Open
- **GitHub Issue**: Not created
- **Labels**: priority:medium, documentation, requirements, prd

**Description**: PRD validation found missing dedicated Product Scope section (one of 6 BMAD core sections). While scope information exists throughout the document (Release Plan, Backlog, MVP markers), consolidating into a dedicated section would improve clarity.

**Acceptance Criteria**:
- [ ] Dedicated Product Scope section added to PRD
- [ ] MVP scope clearly defined
- [ ] Out-of-scope items explicitly listed
- [ ] Future iterations roadmap consolidated
- [ ] Section placed appropriately in PRD structure
- [ ] Validation score improves to 100% BMAD compliance

---

## Usage Instructions

### Creating GitHub Issues

**Option 1: Use Automation Script (Recommended)**
```bash
# Authenticate with GitHub CLI
gh auth login

# Run the consolidated log script to create all 20 issues
python3 scripts/create-issues-from-log.py
```

This script:
- Creates all 20 issues from the consolidated log
- Updates `github_issue_number`, `status`, and `date_opened` fields automatically
- Skips already-created issues (idempotent)
- Updates summary statistics

**Option 2: Manual Creation**
1. Visit https://github.com/tim-dickey/trivia-app/issues/new
2. Copy title, labels, and description from each issue above
3. Create issue and manually update `github_issue_number` field in issues-log.json

### Tracking Issues

After creating GitHub issues (automatically updated by the script or manually):
1. Set `github_issue_number` to the created issue number
2. Update `status` from "open" to "in_progress" or "closed"
3. Set `date_opened` and `assignee` as appropriate
4. Update summary statistics at bottom of JSON file

### Reporting

Generate reports using the JSON data:
- Issues by priority
- Issues by category
- Issues by source
- Effort estimates
- Progress tracking

---

## Maintenance

This log should be updated when:
- New issues are identified from any source
- Issues are created in GitHub
- Issue status changes (in_progress, closed)
- Issues are assigned to team members
- New sources of issues are discovered

**Last Updated**: 2026-02-02  
**Next Review**: After GitHub issue creation
