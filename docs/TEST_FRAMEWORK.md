# Test Framework Documentation

## Overview

This document describes the test framework configuration for the trivia-app backend, including the PostgreSQL/SQLite dual database setup and test infrastructure.

## Testing Dependencies

The source of truth for backend test dependencies is `backend/requirements.txt`. Use the project `venv` (not `.venv`) and install dependencies before running tests.

Key testing-related packages (current requirements):
- `pytest==9.0.2`
- `pytest-asyncio>=0.25.0`
- `pytest-cov==6.0.0`

Note: Keep `pytest` and `pytest-asyncio` compatible when updating versions.

## Recent Updates (2026-02-07)

- Standardized on `venv` for Python environments
- Updated backend requirements (testing/dev pins and ranges) in `backend/requirements.txt`

## Test Database Configuration

### Dual Database Support

The test framework supports both PostgreSQL (for CI) and SQLite (for local development):

- **CI Environment**: Uses PostgreSQL 13 via Docker service
- **Local Development**: Uses SQLite for fast, dependency-free testing

### Configuration File

Location: `backend/tests/conftest.py`

```python
# Test database URL - Uses environment variable if set (CI), 
# otherwise falls back to SQLite for local dev
TEST_DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./test_trivia.db")

# Create test engine with appropriate configuration
engine_kwargs = {}
if "sqlite" in TEST_DATABASE_URL:
    engine_kwargs["connect_args"] = {"check_same_thread": False}

test_engine = create_engine(TEST_DATABASE_URL, **engine_kwargs)
```

### Environment Variables

- `DATABASE_URL`: Database connection string
  - **CI**: Set to `postgresql://test_user:test_pass@localhost:5432/test_db`
  - **Local**: Defaults to `sqlite:///./test_trivia.db` if not set

## Test Structure

### Test Organization

```
backend/tests/
├── api/                  # API endpoint tests
│   └── test_auth.py      # Authentication endpoints
├── core/                 # Core functionality tests
│   ├── test_multi_tenancy.py      # Multi-tenant features
│   └── test_database_config.py    # Database configuration validation
├── crud/                 # CRUD operation tests
│   ├── test_base.py
│   ├── test_organization_crud.py
│   └── test_user_crud.py
├── integration/          # Integration tests
│   └── test_tenant_isolation.py
├── models/              # Model tests
│   ├── test_organization.py
│   └── test_user.py
└── conftest.py          # Shared fixtures and configuration
```

### Test Fixtures

Common fixtures available to all tests (defined in `conftest.py`):

- `db`: Database session with transaction rollback
- `client`: FastAPI test client
- `sample_organization`: Pre-created organization (FREE plan)
- `premium_organization`: Pre-created organization (PREMIUM plan)
- `enterprise_organization`: Pre-created organization (ENTERPRISE plan)
- `sample_user`: Pre-created user (PARTICIPANT role)
- `facilitator_user`: Pre-created user (FACILITATOR role)
- `admin_user`: Pre-created user (ADMIN role)
- `other_org_user`: User from different organization (for multi-tenancy tests)
- `auth_token`: JWT token for sample_user
- `admin_auth_token`: JWT token for admin_user
- `auth_headers`: Authorization headers for sample_user
- `admin_auth_headers`: Authorization headers for admin_user

## Database Configuration Tests

### Test Categories

Location: `backend/tests/core/test_database_config.py`

#### 1. TestDatabaseConfiguration

Validates core database functionality:

- ✅ Environment variable configuration
- ✅ Basic query execution
- ✅ Transaction support and rollback
- ✅ Test isolation between runs
- ✅ UUID primary key handling
- ✅ Foreign key relationships
- ✅ Enum type support
- ✅ Unique constraint enforcement
- ✅ Timestamp columns
- ✅ Field updates and nullable fields

#### 2. TestPostgreSQLSpecificFeatures

Tests PostgreSQL-specific features (skipped when using SQLite):

- ✅ PostgreSQL connection validation
- ✅ Full-text search capability (placeholder)
- ✅ JSON operator support (placeholder)

#### 3. TestSQLiteSpecificFeatures

Tests SQLite-specific features (skipped when using PostgreSQL):

- ✅ SQLite connection validation
- ✅ Performance characteristics

#### 4. TestDatabaseMigrations

Validates database schema and migrations:

- ✅ Table existence (organizations, users)
- ✅ Alembic version tracking (when applicable)
- ✅ Organizations table schema
- ✅ Users table schema
- ✅ Foreign key constraints

## Running Tests

### Local Development (SQLite)

```bash
# Navigate to backend directory
cd backend

# Ensure the venv is active and dependencies are installed
# pip install -r requirements.txt

# Run all tests
pytest

# Run specific test file
pytest tests/core/test_database_config.py

# Run with coverage
pytest --cov=backend --cov-report=html

# Run verbose
pytest -v
```

### With PostgreSQL (Local)

```bash
# Start PostgreSQL
docker compose up -d postgres

# Wait for PostgreSQL to be ready
docker compose ps

# Set environment variable and run tests
export DATABASE_URL="postgresql://trivia_user:trivia_pass@localhost:5432/trivia_db"
export PYTHONPATH=$(pwd)/..
pytest tests/core/test_database_config.py -v
```

### CI Environment

Tests automatically run with PostgreSQL in CI workflows:

```yaml
# .github/workflows/ci.yml
services:
  postgres:
    image: postgres:13
    env:
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_pass
      POSTGRES_DB: test_db
    ports:
      - 5432:5432
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5

steps:
  - name: Run migrations
    env:
      DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db
    run: cd backend && alembic upgrade head

  - name: Run tests with coverage
    env:
      DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db
      PYTHONPATH: .
    run: pytest backend/tests --cov=backend --cov-report=xml
```

## Test Isolation

### Database Session Management

Each test receives a fresh database session via the `db` fixture:

1. **Setup**: Tables are created before each test
2. **Execution**: Test runs with its own session
3. **Teardown**: Transaction is rolled back, tables are dropped

This ensures complete isolation between tests.

### Transaction Rollback

The `db` fixture uses transaction rollback to ensure:
- No data persists between tests
- Tests can modify database without affecting others
- Fast test execution (no need to recreate database)

## Best Practices

### Writing Database Tests

1. **Use fixtures**: Leverage existing fixtures for common test data
2. **Test isolation**: Don't rely on data from previous tests
3. **Clean assertions**: Test one thing per test method
4. **Database-agnostic**: Avoid database-specific SQL unless necessary

### Example Test

```python
def test_user_creation(db, sample_organization):
    """Test creating a new user"""
    user = User(
        email="newuser@test.com",
        name="New User",
        password_hash="hashed_password",
        organization_id=sample_organization.id,
        role=UserRole.PARTICIPANT
    )
    db.add(user)
    db.flush()
    
    # Verify user was created
    found_user = db.query(User).filter_by(email="newuser@test.com").first()
    assert found_user is not None
    assert found_user.name == "New User"
```

## Database Compatibility

### Supported Features (Both Databases)

- ✅ UUID primary keys
- ✅ Foreign key relationships
- ✅ Enum types
- ✅ Unique constraints
- ✅ Timestamps
- ✅ Transaction isolation
- ✅ Basic indexes

### PostgreSQL-Only Features

- Full-text search (ts_vector)
- Array types
- JSONB operators
- Advanced indexing (GiST, GIN)

### SQLite Limitations

- Limited ALTER TABLE support
- No array types
- Different JSON handling
- Case-sensitive string comparison by default

## Troubleshooting

### Tests Pass Locally but Fail in CI

**Problem**: SQLite and PostgreSQL dialect differences

**Solution**: Run tests with PostgreSQL locally:
```bash
docker compose up -d postgres
export DATABASE_URL="postgresql://trivia_user:trivia_pass@localhost:5432/trivia_db"
pytest
```

### Database Connection Errors

**Problem**: Cannot connect to PostgreSQL

**Solution**: Check PostgreSQL is running:
```bash
docker compose ps postgres
docker compose logs postgres
```

### Migration Errors

**Problem**: Alembic version mismatch

**Solution**: Run migrations:
```bash
cd backend
alembic upgrade head
```

### Test Isolation Issues

**Problem**: Tests failing due to leftover data

**Solution**: The `db` fixture handles cleanup automatically. If issues persist:
1. Check that tests use the `db` fixture
2. Verify no direct database connections are made
3. Ensure tests don't commit transactions

## Warning Remediation Notes

Recent local test runs surfaced deprecation warnings. Track these for cleanup during refactors:

- Starlette `python-multipart` import deprecation
- SQLAlchemy `declarative_base()` deprecation (2.0)
- Pydantic class-based config deprecation (V2)
- httpx `app` shortcut deprecation
- `datetime.utcnow()` deprecation warnings (core + tests)

## Coverage Requirements

- **Minimum coverage**: 80% (enforced in CI)
- **Coverage reports**: Generated in `htmlcov/` directory
- **View coverage**: Open `htmlcov/index.html` in browser

## CI/CD Integration

### Workflow Files

1. **ci.yml**: Main CI pipeline
   - Runs on all PRs and pushes to main
   - Uses PostgreSQL service
   - Enforces 80% coverage threshold

2. **codacy.yml**: Scheduled security scans
   - Runs weekly and on manual trigger
   - Uses PostgreSQL service
   - Uploads coverage to Codacy

### Database Service Configuration

Both workflows use identical PostgreSQL configuration:
- Image: `postgres:13`
- Health checks: `pg_isready` every 10s
- Credentials: test_user/test_pass
- Database: test_db

## Future Improvements

### Planned Enhancements

1. **Performance Testing**: Add benchmarks for database operations
2. **Migration Testing**: Automated migration up/down testing
3. **Data Generators**: Factory pattern for test data generation
4. **Parallel Testing**: Enable pytest-xdist for faster execution
5. **Test Fixtures**: Expand fixture library for common scenarios

### Feature-Specific Tests

As new features are added, add corresponding tests:

- **Full-text search**: Test PostgreSQL ts_vector when implemented
- **Array columns**: Test PostgreSQL array types when implemented
- **JSONB columns**: Test PostgreSQL JSONB when implemented
- **Soft deletes**: Test deletion behavior when implemented

## Related Documentation

- [CI/CD Documentation](CI_CD.md)
- [Multi-Tenancy Documentation](MULTI_TENANCY.md)
- [Contributing Guide](../CONTRIBUTING.md)

## Changelog

### 2026-02-03: PostgreSQL in CI

- Added PostgreSQL 13 service to CI workflows
- Updated conftest.py for dual database support
- Created test_database_config.py test suite
- All 108+ tests passing with both SQLite and PostgreSQL
- Documentation: This file created

---

*Last Updated: 2026-02-03*
*Maintainer: Development Team*
