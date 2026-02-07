# Contributing to Trivia App

Thank you for your interest in contributing to **trivia-app**! This is an open source project aimed at helping organizations create engaging learning experiences through gamified trivia. We welcome contributions from developers of all skill levels.

> 📍 **Finding Files**: See [FILE_LOCATIONS.md](FILE_LOCATIONS.md) for a complete guide to navigating the repository.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Areas for Contribution](#areas-for-contribution)
- [Getting Help](#getting-help)

## 🤝 Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. By participating in this project, you agree to:

- **Be Respectful**: Treat everyone with respect and consideration
- **Be Constructive**: Provide helpful feedback and support others
- **Be Collaborative**: Work together toward common goals
- **Be Inclusive**: Welcome diverse perspectives and experiences
- **Be Professional**: Maintain a professional and courteous tone

Unacceptable behavior includes harassment, discrimination, trolling, or any other conduct that creates an intimidating or unwelcoming environment.

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have:

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git
- A GitHub account
- OpenSSL (for JWT secret generation)

### Initial Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/trivia-app.git
   cd trivia-app
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/trivia-app.git
   ```
4. **Set up Python virtual environment**:
   ```bash
   cd backend
   # IMPORTANT: Use 'venv' as the directory name (not '.venv')
   # This project standardizes on 'venv/' for consistency across all environments
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # or: venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```
5. **Follow the remaining setup instructions** in the [README.md](README.md)

## 🔨 How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **Bug Reports**: Help us identify and fix issues
- **Feature Requests**: Suggest new features or enhancements
- **Code Contributions**: Implement features or fix bugs
- **Documentation**: Improve guides, API docs, and examples
- **Testing**: Write tests to improve coverage
- **Design**: UX/UI improvements and accessibility enhancements
- **Reviews**: Review pull requests and provide feedback

### Reporting Bugs

When reporting a bug, please include:

1. **Clear title and description**
2. **Steps to reproduce** the issue
3. **Expected vs. actual behavior**
4. **Environment details** (OS, Python version, Node version, etc.)
5. **Screenshots or logs** if applicable
6. **Possible solution** if you have ideas

### Suggesting Enhancements

When suggesting an enhancement:

1. **Check existing issues** to avoid duplicates
2. **Describe the problem** you're trying to solve
3. **Explain your proposed solution**
4. **Consider alternative approaches**
5. **Note any implementation challenges**

## 🔄 Development Workflow

### 1. Create a Feature Branch

Always create a new branch for your work:

```bash
# Update your main branch
git checkout main
git pull upstream main

# Create a feature branch
git checkout -b feature/your-feature-name
# or for bug fixes:
git checkout -b fix/bug-description
```

**Branch Naming Conventions**:
- `feature/` - New features (e.g., `feature/chat-integration`)
- `fix/` - Bug fixes (e.g., `fix/login-validation`)
- `docs/` - Documentation updates (e.g., `docs/api-endpoints`)
- `test/` - Test additions (e.g., `test/auth-endpoints`)
- `refactor/` - Code refactoring (e.g., `refactor/user-service`)

### 2. Make Your Changes

- Write clean, readable code
- Follow existing code structure and conventions
- Add or update tests as needed
- Update documentation if your changes affect it
- Keep commits focused and atomic

### 3. Commit Your Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "Add user authentication feature

- Implement JWT token generation
- Add password hashing with bcrypt
- Create login and registration endpoints
- Add unit tests for auth service

Resolves #123"
```

**Commit Message Format**:
- First line: Brief summary (50 characters or less)
- Blank line
- Detailed description with bullet points
- Reference related issues (e.g., "Resolves #123" or "Relates to #456")

### 4. Keep Your Branch Updated

Regularly sync with the upstream repository:

```bash
git fetch upstream
git rebase upstream/main
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## 📐 Coding Standards

### Backend (Python/FastAPI)

- **Style Guide**: Follow PEP 8
- **Type Hints**: Use type hints for all functions
- **Docstrings**: Write docstrings for modules, classes, and functions
- **Error Handling**: Use proper exception handling
- **Async/Await**: Use async functions where appropriate
- **Imports**: Organize imports (standard library, third-party, local)

**Example**:
```python
from typing import Optional
from fastapi import HTTPException
from pydantic import EmailStr

async def get_user_by_email(
    email: EmailStr,
    organization_id: str
) -> Optional[User]:
    """
    Retrieve a user by email within an organization.
    
    Args:
        email: User's email address
        organization_id: Organization UUID
        
    Returns:
        User object if found, None otherwise
        
    Raises:
        HTTPException: If database query fails
    """
    # Implementation
```

**Code Quality Tools**:
```bash
# Format code
black .

# Lint code
ruff check .

# Type checking
mypy backend/
```

### Frontend (React/TypeScript)

- **Style Guide**: Use Prettier and ESLint configurations
- **TypeScript**: Strict typing, avoid `any` types
- **Components**: Functional components with hooks
- **File Organization**: One component per file
- **CSS**: Use Tailwind CSS utility classes
- **Naming**: PascalCase for components, camelCase for functions

**Example**:
```typescript
interface LoginFormProps {
  onSuccess: (token: string) => void;
  onError: (error: Error) => void;
}

export const LoginForm: React.FC<LoginFormProps> = ({ 
  onSuccess, 
  onError 
}) => {
  // Implementation
};
```

**Code Quality Tools**:
```bash
# Lint
npm run lint

# Format
npm run format

# Type check
npm run type-check
```

### Database

- **Migrations**: Always use Alembic for schema changes
- **Naming**: Use descriptive migration names
- **Indexes**: Add indexes for frequently queried columns
- **Constraints**: Use database constraints for data integrity
- **Multi-tenancy**: Include `organization_id` in all tenant tables

### Working with Database Migrations

**Creating a New Migration**:
```bash
cd backend

# Auto-generate migration from model changes
alembic revision --autogenerate -m "Add user profile fields"

# Or create empty migration for data changes
alembic revision -m "Seed initial organizations"
```

**Important Migration Guidelines**:
1. **Always review auto-generated migrations** before committing
2. **Test migrations both up and down**:
   ```bash
   # Apply migration
   alembic upgrade head
   
   # Test rollback
   alembic downgrade -1
   
   # Re-apply
   alembic upgrade head
   ```
3. **Never modify existing migrations** that have been merged to main
4. **Include both upgrade and downgrade** operations
5. **Add indexes and constraints** in the same migration as the table

**Migration Best Practices**:
```python
# Good: Descriptive operation with proper naming
def upgrade():
    op.create_table(
        'sessions',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('organization_id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )
    # Add index immediately
    op.create_index('ix_sessions_organization_id', 'sessions', ['organization_id'])
    # Add foreign key constraint
    op.create_foreign_key(
        'fk_sessions_organization', 'sessions', 'organizations',
        ['organization_id'], ['id'], ondelete='CASCADE'
    )

def downgrade():
    op.drop_table('sessions')
```

**Checking Migration Status**:
```bash
# View current migration
alembic current

# View migration history
alembic history

# View pending migrations
alembic upgrade head --sql  # Shows SQL without applying
```

## 🧪 Testing Requirements

### Backend Testing

**Required**:
- Unit tests for all new functions and classes
- Integration tests for API endpoints
- Test coverage target: **80%+ overall**

**Structure**:
```
backend/tests/
├── models/          # Model tests
├── crud/            # CRUD operation tests
├── api/             # API endpoint tests
├── services/        # Business logic tests
├── integration/     # Integration tests (tenant isolation, WebSocket, etc.)
├── core/            # Core functionality tests (multi-tenancy, security)
└── conftest.py      # Pytest fixtures
```

**Running Tests**:
```bash
# From project root (recommended)
pytest backend/tests --cov=backend --cov-report=html

# Or from backend directory (requires PYTHONPATH)
cd backend
PYTHONPATH=.. pytest

# Run with coverage from backend directory
PYTHONPATH=.. pytest --cov=backend --cov-report=html

# Run specific test file
PYTHONPATH=.. pytest tests/api/test_auth.py

# Run specific test
PYTHONPATH=.. pytest tests/api/test_auth.py::test_user_registration

# Run WebSocket integration tests
PYTHONPATH=.. pytest tests/integration/test_websocket.py -v

# Run all integration tests
PYTHONPATH=.. pytest tests/integration/ -v
```

**Example API Test**:
```python
def test_user_registration_success(test_client, test_organization):
    """Test successful user registration."""
    response = test_client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "secure_password123",
            "name": "New User",
            "organization_slug": test_organization.slug
        }
    )
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["email"] == "newuser@example.com"
    assert "password" not in data
```

**Example WebSocket Test**:
```python
def test_websocket_connection_with_valid_token(client, sample_user):
    """Test WebSocket accepts connection with valid JWT token."""
    token = create_access_token(
        data={
            "sub": str(sample_user.id),
            "org_id": str(sample_user.organization_id),
            "roles": [sample_user.role.value]
        }
    )
    
    session_id = "test-session-1"
    
    with client.websocket_connect(f"/ws/{session_id}?token={token}") as websocket:
        # Receive welcome message
        data = websocket.receive_json()
        
        assert data["type"] == "connection"
        assert data["session_id"] == session_id
        assert data["user_id"] == str(sample_user.id)
```

**Test Categories**:
- **Unit Tests**: Test individual functions and classes in isolation
- **Integration Tests**: Test interactions between components (API + DB, WebSocket + Auth)
- **Multi-Tenancy Tests**: Verify organization isolation and security
- **WebSocket Tests**: Test real-time communication, broadcasting, and session management

For WebSocket testing details, see [WebSocket Infrastructure Documentation](../docs/websocket-infrastructure.md#testing).

### Frontend Testing

**Required**:
- Component tests for UI components
- Hook tests for custom hooks
- Integration tests for critical user flows

**Running Tests**:
```bash
cd frontend

# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run in watch mode
npm run test:watch
```

## 🔄 CI/CD and GitHub Actions

### Understanding Our CI/CD Workflows

The project uses several GitHub Actions workflows for automated testing and code quality:

**1. CI Pipeline** (`.github/workflows/ci.yml`)
- **Runs on**: All PRs and pushes to main
- **Purpose**: Fast feedback on code quality and test results
- **What it does**:
  - Runs backend tests with pytest (enforces 80%+ coverage)
  - Runs frontend tests and linting
  - Uploads coverage to Codacy and GitHub (when secrets available)
  - **Note**: Coverage upload is optional - works without secrets for external contributors

**2. Security Scans** (`.github/workflows/security-scheduled.yml`)
- **Runs on**: Weekly schedule (Saturday) and pushes to main
- **Purpose**: Deep security analysis
- **What it does**:
  - Runs Codacy security analysis
  - Runs CodeQL analysis for Python and JavaScript/TypeScript
  - Uploads security results to GitHub Security tab
  - **Note**: Codacy security analysis is optional and is skipped if the `CODACY_PROJECT_TOKEN` secret is not available; CodeQL analysis still runs regardless of this secret

**3. Legacy Workflows** (scheduled only):
- **Codacy** (`.github/workflows/codacy.yml`): Weekly security scans (Thursday)
- **CodeQL** (`.github/workflows/codeql.yml`): Weekly security scans (Saturday)

**4. Other Workflows**:
- **Greetings**: Welcomes new contributors
- **Summary**: AI-powered issue summarization

### For External Contributors

**You don't need to set up any secrets!** 

When you submit a PR:
- All tests will run automatically
- You'll see results in the PR checks
- Some workflows may show warnings about missing secrets (like `CODACY_PROJECT_TOKEN`)
- **This is normal** - maintainers will handle coverage uploads and security scanning
- Your PR will still be reviewed and can be merged

### For Maintainers: GitHub Secrets Setup

If you're a maintainer setting up a fork or need to configure CI/CD:

**GitHub Secrets Setup** (Repository Settings → Secrets and variables → Actions):

#### 1. CODACY_PROJECT_TOKEN (Optional for PR CI, recommended for main branch)

**Purpose**: Uploads test coverage and security scan results to Codacy

**How to Obtain**:
1. Sign up at [codacy.com](https://www.codacy.com/) with your GitHub account
2. Add the `trivia-app` repository to Codacy
3. Navigate to: Project → Settings → Integrations → Project API Token
4. Copy the Project API Token
5. In GitHub: Repository Settings → Secrets and variables → Actions → New repository secret
   - **Name**: `CODACY_PROJECT_TOKEN`
   - **Value**: [paste token from Codacy]

**What Happens Without This Secret**:
- ✅ All tests still run on PRs
- ✅ CI checks will pass/fail normally
- ❌ Coverage reports won't be uploaded to Codacy
- ❌ Codacy security scans will be skipped
- **External contributors don't need this** - workflows gracefully skip optional steps

**Used By**:
- `.github/workflows/ci.yml` - Coverage upload (optional)
- `.github/workflows/security-scheduled.yml` - Security scans (optional)
- `.github/workflows/codacy.yml` - Legacy scheduled scans (optional)

#### Optional Secrets (For Future Features)

- **`DEPENDABOT_TOKEN`**: For automated dependency updates (not currently used)
- **`SLACK_WEBHOOK`**: For deployment notifications (not currently used)

### Workflow Debugging

**If CI/CD checks fail on your PR**:

1. **Click on "Details"** next to the failed check
2. **Review the logs** to identify the issue
3. **Common failures**:
   - Test failures: Fix the failing tests locally first
   - Linting errors: Run `ruff check .` and `black .` locally
   - Import errors: Ensure all dependencies are in requirements.txt
   - Coverage below 80%: Add more tests

**Running CI checks locally before pushing**:
```bash
# Backend tests (same as CI runs)
cd backend
PYTHONPATH=.. pytest --cov=backend --cov-report=term-missing --cov-fail-under=80

# Backend linting
cd backend
ruff check .
black --check .

# Backend type checking
mypy backend/

# Frontend tests (if implemented)
cd frontend
npm test

# Frontend linting
cd frontend
npm run lint
```

### Running CI Locally (No Secrets Required)

**You can run the full CI pipeline locally without any GitHub secrets**. This approximates the backend CI job that runs on PRs:

#### Backend Tests
```bash
# Set DATABASE_URL to point at your local PostgreSQL instance (CI uses PostgreSQL)
export DATABASE_URL="postgresql://test_user:test_pass@localhost:5432/test_db"

# Apply Alembic migrations before running tests (CI does this automatically)
cd backend
alembic upgrade head

# Run tests with coverage (matches CI exactly)
PYTHONPATH=.. pytest --cov=backend --cov-report=term-missing --cov-fail-under=80

# The coverage threshold must be 80% or higher for CI to pass
```

#### Frontend Tests
```bash
# Install dependencies
cd frontend
npm ci  # or npm install if no package-lock.json

# Run linter
npm run lint

# Run tests
npm test

# Build check
npm run build
```

#### Security Scanning (Optional)
```bash
# Install Codacy CLI (optional - for local security scans)
curl -L https://github.com/codacy/codacy-analysis-cli/releases/download/7.10.7/codacy-analysis-cli-assembly.jar -o codacy-cli.jar

# Run analysis (no token needed for local scan)
java -jar codacy-cli.jar analyze --directory . --format json --output results.json
```

**Note**: The security scans are optional and primarily run on a schedule. You don't need to run them locally unless you're specifically working on security improvements.

### Known CI/CD Issues

⚠️ **Test Database Configuration**: CI and production both use PostgreSQL (via `DATABASE_URL` in `.github/workflows/ci.yml`). If you run tests locally with SQLite or another database, be aware of potential behavior differences and ensure migrations and tests are validated against PostgreSQL before merging. See [action items](../_bmad-output/implementation-artifacts/action-items-2026-02-02.md) for details.

⚠️ **Frontend Tests**: Frontend test suite is still being developed. CI runs tests but they are currently optional (continue-on-error).

## 📝 Pull Request Process

### Before Submitting

1. ✅ **All tests pass** locally
2. ✅ **Code is properly formatted** (black, prettier)
3. ✅ **No linting errors** (ruff, eslint)
4. ✅ **Documentation is updated** if needed
5. ✅ **Commits are well-organized** and descriptive
6. ✅ **Branch is up-to-date** with main

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Related Issues
Closes #123
Relates to #456

## Changes Made
- Added user authentication endpoints
- Implemented JWT token generation
- Added unit tests for auth service

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests pass locally
- [ ] Manual testing completed

## Screenshots (if applicable)
[Add screenshots for UI changes]

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review of code completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added that prove fix/feature works
- [ ] New and existing tests pass
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs automatically
2. **Code Review**: At least one maintainer reviews your PR
3. **Feedback**: Address review comments and requested changes
4. **Approval**: PR is approved after successful review
5. **Merge**: Maintainer merges your PR into main

### After Your PR is Merged

1. Delete your feature branch
2. Update your local repository
3. Celebrate your contribution! 🎉

## 🎯 Areas for Contribution

### High Priority

- **Testing**: Implement unit and integration tests (current gap)
- **Frontend Components**: Build registration and login forms
- **Seed Data**: Create development data script
- **Documentation**: API documentation and examples

### Feature Development

Review the [Epic Breakdown](_bmad-output/planning-artifacts/epics.md) for upcoming features:

- **Epic 2**: Session Creation & Management
- **Epic 3**: Live Trivia Gameplay & Real-Time Scoring
- **Epic 4**: Educational Feedback & Knowledge Assessment
- **Epic 5**: Chat Platform Integration

### Ongoing Needs

- 🐛 **Bug Fixes**: Check [Issues](../../issues) for open bugs
- ♿ **Accessibility**: WCAG 2.1 AA compliance improvements
- 🌐 **i18n**: Internationalization support
- 📊 **Performance**: Optimization and scalability
- 🎨 **UX/UI**: Design improvements

## 🆘 Getting Help

### Resources

- **📍 File Locations**: [FILE_LOCATIONS.md](FILE_LOCATIONS.md) - Find any file in the repository
- **Documentation**: Check the `docs/` directory
- **Architecture**: Review `_bmad-output/implementation-artifacts/architecture.md`
- **CI/CD Guide**: See `docs/CI_CD.md` for workflow documentation
- **Validation Reports**: See `docs/validation/` for quality standards
- **PRD**: Review `_bmad-output/implementation-artifacts/TRIVIA_APP_PRD.md`

### Questions?

- **GitHub Issues**: Open an issue with the `question` label
- **Discussions**: Use GitHub Discussions for general questions
- **Code Review**: Ask questions in PR comments

### Stuck?

- Review similar code in the codebase
- Check existing tests for examples
- Read validation reports for architectural guidance
- Don't hesitate to ask for help in your PR

## 📄 License

By contributing to trivia-app, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

**Thank you for contributing to trivia-app!** 🙏

Your contributions help create better learning experiences for teams everywhere.

**Built with ❤️ by the open source community**
