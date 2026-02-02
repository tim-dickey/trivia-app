# CI/CD Pipeline Documentation

> **Last Updated**: February 2, 2026  
> **Status**: Active workflows with known optimization opportunities

## Overview

The trivia-app project uses GitHub Actions for continuous integration, code quality analysis, and security scanning. This document describes all active workflows, their purposes, and known issues.

## Active Workflows

### 1. Codacy Workflow

**File**: `.github/workflows/codacy.yml`

**Triggers**:
- Pull requests to `main` branch
- Pushes to `main` branch
- Weekly schedule: Thursday at 5:33 PM UTC

**Purpose**: Code quality analysis, security scanning, and test coverage tracking

**What It Does**:
1. Checks out repository code
2. Sets up Python 3.11 environment
3. Installs backend dependencies with pip caching for faster runs
4. Runs pytest test suite with coverage
5. Generates coverage reports in XML format
6. Uploads coverage results to Codacy
7. Runs Codacy CLI security analysis (Bandit for Python)

**Requirements**:
- **Secret**: `CODACY_PROJECT_TOKEN` (repository secret)
- **Python Version**: 3.11
- **Coverage Threshold**: Configured locally to 80% (not enforced in workflow)

**Known Issues**:
- ⚠️ Runs full test suite on every PR (duplicate with CodeQL)
- ⚠️ Does not fail on coverage below 80% threshold
- ⚠️ Coverage upload may fail if CODACY_PROJECT_TOKEN is missing (external contributors)

**Exit Status**:
- Returns exit code 0 even if tests fail (due to `|| echo` pattern)
- Check logs manually to verify test results

---

### 2. CodeQL Workflow

**File**: `.github/workflows/codeql.yml`

**Triggers**:
- Pull requests to `main` branch
- Pushes to `main` branch  
- Weekly schedule: Saturday at 11:21 AM UTC

**Purpose**: Security vulnerability detection using GitHub's CodeQL analysis engine

**What It Does**:
1. Checks out repository code
2. Initializes CodeQL for specified languages
3. Performs CodeQL analysis
4. Uploads results to GitHub Security tab

**Current Configuration**:
- **Languages**: `actions` (GitHub Actions workflows only)
- **Auto-build**: Enabled for compiled languages
- **Queries**: `security-extended` (comprehensive security checks)

**Known Issues**:
- ⚠️ Currently only analyzes GitHub Actions files
- ⚠️ Python and TypeScript/JavaScript analysis not configured
- ⚠️ Runs tests redundantly with Codacy workflow

**Recommended Changes**:
```yaml
# Add to languages array:
languages: ['actions', 'python', 'javascript']
```

---

### 3. Greetings Workflow

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

### 4. Summary Workflow

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

### 5. Dependency Review (Disabled)

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
| Codacy | ✅ | ✅ | Weekly (Thu) | Partial (no token) |
| CodeQL | ✅ | ✅ | Weekly (Sat) | ✅ Full |
| Greetings | ✅ | N/A | N/A | ✅ Full |
| Summary | On issue creation | N/A | N/A | ✅ Full |
| Dependency Review | ❌ Disabled | ❌ Disabled | ❌ Disabled | ❌ Disabled |

---

## Known Issues and Action Items

### 🔴 Critical Priority

#### 1. Duplicate Test Runs

**Problem**: Both Codacy and CodeQL workflows run tests on every PR

**Impact**:
- Wastes CI/CD minutes
- Slows down PR feedback cycle
- Confuses contributors about which workflow to check

**Recommended Solution**:
```yaml
# Create single consolidated workflow: .github/workflows/ci.yml
name: CI Pipeline
on:
  pull_request:
    branches: [ main ]
  push:
    branches: [ main ]

jobs:
  test-and-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Run tests with coverage
        run: |
          cd backend
          pytest --cov=backend --cov-report=xml --cov-report=term
      
      - name: Upload to Codacy
        run: |
          bash <(curl -Ls https://coverage.codacy.com/get.sh) report \
            -r backend/coverage.xml
        env:
          CODACY_PROJECT_TOKEN: ${{ secrets.CODACY_PROJECT_TOKEN }}
      
      - name: Upload to Codecov (optional)
        uses: codecov/codecov-action@v3
        with:
          files: backend/coverage.xml

# Then run CodeQL and Codacy on schedule only
```

#### 2. No Frontend CI Pipeline

**Problem**: Frontend tests not run in CI

**Impact**: Frontend changes can break without detection

**Recommended Solution**:
Add to consolidated CI workflow:
```yaml
- name: Set up Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '18'
    
- name: Install frontend dependencies
  run: |
    cd frontend
    npm ci
    
- name: Run frontend tests
  run: |
    cd frontend
    npm test -- --coverage
    
- name: Run frontend linting
  run: |
    cd frontend
    npm run lint
```

---

### 🟡 High Priority

#### 3. CodeQL Limited Language Coverage

**Problem**: CodeQL only analyzes GitHub Actions files

**Fix**:
```yaml
# In .github/workflows/codeql.yml
strategy:
  matrix:
    language: ['python', 'javascript', 'actions']
```

#### 4. Test Database Inconsistency

**Problem**: CI uses SQLite, production uses PostgreSQL

**Risk**: Database-specific bugs not caught in CI

**Options**:
1. **Use PostgreSQL in CI** (recommended):
   ```yaml
   services:
     postgres:
       image: postgres:13
       env:
         POSTGRES_PASSWORD: test_password
       options: >-
         --health-cmd pg_isready
         --health-interval 10s
         --health-timeout 5s
         --health-retries 5
   ```

2. **Document differences** and add integration tests with PostgreSQL

---

### 🟢 Medium Priority

#### 5. Coverage Threshold Not Enforced

**Problem**: Workflow doesn't fail if coverage drops below 80%

**Fix**:
```yaml
- name: Check coverage threshold
  run: |
    cd backend
    pytest --cov=backend --cov-report=term --cov-fail-under=80
```

#### 6. Dependency Updates

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
- [ ] Add PostgreSQL service to CI
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
