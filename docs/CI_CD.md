# CI/CD Pipeline Documentation

> **Last Updated**: February 2, 2026  
> **Status**: Consolidated workflows - Single CI for PRs, scheduled security scans

## Overview

The trivia-app project uses GitHub Actions for continuous integration, code quality analysis, and security scanning. The workflows have been optimized to eliminate duplicate test runs and improve PR feedback time.

## Active Workflows

### 1. CI Pipeline (Primary)

**File**: `.github/workflows/ci.yml`

**Triggers**:
- Pull requests to `main` branch
- Pushes to `main` branch

**Purpose**: Fast feedback on code changes - runs tests once and uploads coverage

**What It Does**:

**Backend Tests Job**:
1. Checks out repository code
2. Sets up Python 3.11 environment with pip caching
3. Installs backend dependencies
4. Runs pytest test suite with coverage (enforces 80% threshold)
5. Uploads coverage to Codacy (if secret is available)
6. Uploads coverage to GitHub/Codecov

**Frontend Tests Job**:
1. Checks out repository code
2. Sets up Node.js 20 environment
3. Installs frontend dependencies
4. Runs ESLint linter (non-blocking)
5. Runs Vitest test suite (non-blocking)
6. Attempts to build frontend to surface build errors (non-blocking; failures do not currently fail CI)

**Requirements**:
- **Secret**: `CODACY_PROJECT_TOKEN` (optional - workflow continues without it)
- **Python Version**: 3.11
- **Node Version**: 20
- **Coverage Threshold**: 80% enforced with `--cov-fail-under=80`

**Key Features**:
- ✅ No duplicate test runs
- ✅ Graceful degradation when secrets are missing (works for external contributors)
- ✅ Enforces 80% coverage threshold
- ✅ Fast feedback (typically completes in 3-5 minutes)

---

### 2. Security Scans (Scheduled)

**File**: `.github/workflows/security-scheduled.yml`

**Triggers**:
- Pushes to `main` branch (after merge)
- Weekly schedule: Saturday at 11:21 AM UTC
- Manual trigger via workflow_dispatch

**Purpose**: Deep security analysis without slowing down PR feedback

**What It Does**:

**Codacy Security Job**:
1. Runs Codacy Analysis CLI (Bandit for Python)
2. Generates SARIF security report
3. Uploads results to GitHub Security tab

**CodeQL Security Job** (matrix strategy):
1. Analyzes Python code for vulnerabilities
2. Analyzes JavaScript/TypeScript code for vulnerabilities
3. Uses security-extended query pack
4. Uploads results to GitHub Security tab

**Languages Analyzed**: Python, JavaScript/TypeScript

**Key Features**:
- ✅ Comprehensive security scanning
- ✅ Doesn't slow down PRs
- ✅ Runs automatically after merge to main
- ✅ Weekly scheduled deep scans

---

### 3. Codacy Workflow (Legacy)

**File**: `.github/workflows/codacy.yml`

**Status**: Scheduled only (no longer runs on PRs)

**Triggers**:
- Weekly schedule: Thursday at 5:33 PM UTC
- Manual trigger via workflow_dispatch

**Purpose**: Legacy support for Codacy-specific features

**Note**: This workflow is maintained for backward compatibility. Most functionality has been moved to ci.yml and security-scheduled.yml.

---

### 4. CodeQL Workflow (Legacy)

**File**: `.github/workflows/codeql.yml`

**Status**: Scheduled only (no longer runs on PRs)

**Triggers**:
- Weekly schedule: Saturday at 11:21 AM UTC
- Manual trigger via workflow_dispatch

**Purpose**: Legacy CodeQL workflow

**Current Configuration**:
- **Languages**: Python, JavaScript/TypeScript, GitHub Actions
- **Build Mode**: None (interpreted languages)
- **Queries**: security-extended

**Note**: This workflow is maintained for backward compatibility. CodeQL analysis is now part of security-scheduled.yml.

---

### 5. Greetings Workflow

**File**: `.github/workflows/greetings.yml`

**Triggers**:
- New issues created
- New pull requests opened

**Purpose**: Welcome first-time contributors with friendly messages

**What It Does**:
- Detects first-time issue creators and commenters
- Posts welcome message on first issue
- Posts thank you message on first PR

**Configuration**:
- Uses `actions/first-interaction@v1`
- Customizable welcome messages

---

### 6. Summary Workflow

**File**: `.github/workflows/summary.yml`

**Triggers**:
- New issues created

**Purpose**: AI-powered issue summarization for quick triage

**What It Does**:
- Analyzes issue content
- Generates structured summary
- Helps maintainers quickly understand issues

**Note**: Experimental feature for improving issue management

---

### 7. Dependency Review (Disabled)

**File**: `.github/workflows/dependency-review.yml.disabled`

**Status**: Currently disabled (filename ends with `.disabled`)

**Purpose**: Scan dependencies for known security vulnerabilities

**Why Disabled**: 
- Planned for future implementation
- Requires dependency scanning configuration
- May be replaced with Dependabot

**To Enable**:
```bash
mv .github/workflows/dependency-review.yml.disabled \
   .github/workflows/dependency-review.yml
```

---

## Workflow Execution Matrix

| Workflow | PRs | Push to Main | Schedule | External Contributors |
|----------|-----|--------------|----------|---------------------|
| **CI Pipeline** | ✅ | ✅ | N/A | ✅ Full (with graceful degradation) |
| **Security Scans** | ❌ | ✅ | Weekly (Sat) | ✅ Full |
| Codacy (Legacy) | ❌ | ❌ | Weekly (Thu) | Partial (no token) |
| CodeQL (Legacy) | ❌ | ❌ | Weekly (Sat) | ✅ Full |
| Greetings | ✅ | N/A | N/A | ✅ Full |
| Summary | On issue creation | N/A | N/A | ✅ Full |
| Dependency Review | ❌ Disabled | ❌ Disabled | ❌ Disabled | ❌ Disabled |

**Key Changes**:
- ✅ **No more duplicate test runs** - Tests run once per PR in CI Pipeline
- ✅ **Faster PR feedback** - CI typically completes in 3-5 minutes
- ✅ **Security scans don't slow PRs** - Run on schedule and after merge
- ✅ **Works for external contributors** - No secrets required for basic CI

---

## Consolidated Workflow Benefits

### Before Consolidation
- ❌ Tests ran twice on every PR (Codacy + CodeQL)
- ❌ PR feedback took 8-10 minutes
- ❌ Wasted CI/CD minutes
- ❌ Confusion about which workflow to check

### After Consolidation
- ✅ Tests run once on every PR
- ✅ PR feedback in 3-5 minutes (~50% faster)
- ✅ Efficient use of CI/CD minutes
- ✅ Clear workflow responsibilities
- ✅ Security scans don't slow down development

---

## Issues Resolved

### ✅ Fixed: Duplicate Test Runs

**Previous Issue**: Both Codacy and CodeQL workflows ran tests on every PR

**Solution Implemented**:
- Created unified `ci.yml` that runs tests once
- Moved security scans to scheduled `security-scheduled.yml`
- Updated legacy workflows to run on schedule only

**Impact**:
- 50% reduction in PR feedback time
- No wasted CI/CD minutes
- Clear separation of concerns

---

### ✅ Fixed: CodeQL Limited Language Coverage

**Previous Issue**: CodeQL only analyzed GitHub Actions files

**Solution Implemented**:
- Updated CodeQL configuration to analyze Python
- Updated CodeQL configuration to analyze JavaScript/TypeScript
- Added security-extended query pack

**Impact**:
- Comprehensive security coverage
- Catches vulnerabilities in application code
- Better security posture

---

### ✅ Fixed: Frontend Not Tested in CI

**Previous Issue**: No automated frontend testing

**Solution Implemented**:
- Added frontend job to CI pipeline
- Runs ESLint, tests, and build checks
- Parallel execution with backend tests

**Impact**:
- Frontend changes validated automatically
- Catches frontend issues before merge
- Consistent code quality across stack

---

## Known Issues and Action Items

### 🟡 High Priority

#### 1. Test Database Inconsistency ✅ RESOLVED

**Previous Problem**: CI used SQLite, production uses PostgreSQL

**Resolution**: Implemented PostgreSQL service in CI workflows (completed 2026-02-03)

**Implementation**:
- Added PostgreSQL 13 service to `ci.yml` and `codacy.yml` workflows
- Migrations run automatically before tests
- Tests now use PostgreSQL in CI, SQLite remains available for local development
- All 108 tests verified passing with PostgreSQL

**Benefits**:
- Eliminates SQL dialect differences between CI and production
- PostgreSQL-specific features now properly tested
- Migration compatibility verified in CI

---

### 🟢 Medium Priority

#### 2. Coverage Threshold Enforcement

**Status**: ✅ Now enforced in CI Pipeline

**Solution Implemented**:
```yaml
# In .github/workflows/ci.yml
pytest --cov=backend --cov-report=xml --cov-report=term-missing --cov-fail-under=80
```

**Impact**: CI now fails if coverage drops below 80%

---

#### 3. Dependency Updates

**Problem**: Manual dependency updates required

**Solution**: Enable Dependabot
```yaml
# Create .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/backend"
    schedule:
      interval: "weekly"
  
  - package-ecosystem: "npm"
    directory: "/frontend"
    schedule:
      interval: "weekly"
```

---

## For External Contributors

### What You Need to Know

When you submit a PR:
1. ✅ Tests will run automatically (you'll see results in ~2-3 minutes)
2. ✅ CodeQL security scanning will run
3. ⚠️ Codacy workflow may show warnings about missing `CODACY_PROJECT_TOKEN`
   - **This is normal** - maintainers handle coverage uploads
   - Your PR can still be merged if tests pass
4. ✅ You'll get a friendly greeting message on your first contribution!

### If Your PR Fails CI Checks

1. **Click "Details"** next to the failed check
2. **Read the logs** to find the specific error
3. **Common failures**:
   - **Test failures**: Run `pytest backend/tests` locally
   - **Linting errors**: Run `ruff check .` and `black .`
   - **Import errors**: Check `requirements.txt` is complete
   - **Coverage issues**: Add tests for new code

### Running CI Checks Locally

**Before pushing**:
```bash
# Backend tests (exactly like CI)
cd backend
PYTHONPATH=.. pytest --cov=backend --cov-report=term-missing

# Code formatting
black .

# Linting
ruff check .

# Type checking
mypy backend/
```

**Frontend** (when CI is added):
```bash
cd frontend
npm test -- --coverage
npm run lint
npm run type-check
```

---

## For Maintainers

### Required GitHub Secrets

Set these in: **Repository Settings** → **Secrets and variables** → **Actions**

1. **`CODACY_PROJECT_TOKEN`** (Required)
   - Purpose: Upload test coverage and security scan results
   - Get from: [Codacy Project Settings](https://app.codacy.com/)
   - Path: Project → Settings → Integrations → Project API Token

2. **`DEPENDABOT_TOKEN`** (Optional, for future)
   - Purpose: Automated dependency updates
   - Get from: GitHub Personal Access Tokens

### Setting Up Codacy

1. Sign up at [codacy.com](https://www.codacy.com/) with GitHub account
2. Add the `tim-dickey/trivia-app` repository
3. Go to: Project Settings → Integrations
4. Copy the **Project API Token**
5. Add to GitHub repository secrets as `CODACY_PROJECT_TOKEN`

### Monitoring Workflows

**View workflow runs**:
- GitHub repository → Actions tab
- Filter by workflow name or branch
- Check logs for failures

**Security alerts**:
- GitHub repository → Security tab
- CodeQL results appear here
- Review and dismiss/fix as needed

---

## Workflow Optimization Roadmap

### Phase 1: Immediate Fixes (1-2 days)
- [ ] Consolidate duplicate test runs
- [ ] Add frontend CI pipeline
- [ ] Fix CodeQL language configuration
- [ ] Enforce 80% coverage threshold

### Phase 2: Quality Improvements (1 week)
- [x] Add PostgreSQL service to CI ✅ (Completed 2026-02-03)
- [ ] Enable Dependabot
- [ ] Add pre-commit hooks
- [ ] Set up branch protection rules

### Phase 3: Advanced Features (2-4 weeks)
- [ ] Add deployment workflows (staging/production)
- [ ] Implement E2E tests in CI
- [ ] Add performance testing
- [ ] Set up Docker image builds

---

## Resources

- **GitHub Actions Documentation**: https://docs.github.com/en/actions
- **Codacy Documentation**: https://docs.codacy.com/
- **CodeQL Documentation**: https://codeql.github.com/docs/
- **pytest-cov Documentation**: https://pytest-cov.readthedocs.io/

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-02-02 | Initial CI/CD documentation | Documentation update |
| 2026-02-01 | Added Codacy and CodeQL workflows | PR #21 |

---

**Questions or issues with CI/CD?** Open an issue with the `ci/cd` label.
