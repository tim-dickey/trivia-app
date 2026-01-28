"""
Pytest fixtures and configuration for trivia-app backend tests
Provides test database, client, and sample data fixtures
"""
import pytest
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
import uuid

from backend.core.database import Base, get_db
from backend.main import app
from backend.models.organization import Organization, PlanType
from backend.models.user import User, UserRole
from backend.core.security import hash_password, create_access_token

# Test database URL - Use file-based SQLite for better test stability
TEST_DATABASE_URL = "sqlite:///./test_trivia.db"
# Alternatively for PostgreSQL: "postgresql://trivia_user:trivia_pass@localhost:5432/trivia_test"

# Create test engine
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in TEST_DATABASE_URL else {},
    poolclass=None if "sqlite" in TEST_DATABASE_URL else None
)

# Create test session factory
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function", autouse=False)
def db() -> Generator[Session, None, None]:
    """
    Create a fresh database session for each test
    Rolls back all changes after test completes
    """
    # Import all models to ensure they're registered with Base
    from backend.models.organization import Organization  # noqa: F401
    from backend.models.user import User  # noqa: F401
    
    # Create all tables before each test
    Base.metadata.drop_all(bind=test_engine)  # Ensure clean state
    Base.metadata.create_all(bind=test_engine)
    
    # Create session
    session = TestSessionLocal()
    
    try:
        yield session
    except Exception:
        session.rollback()  # Rollback on exception
        raise
    finally:
        # Always rollback to ensure clean state (handles intentional constraint violations in tests)
        session.rollback()
        session.close()
        # Drop all tables after test to ensure isolation
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """
    Create FastAPI test client with overridden database dependency
    Uses the same db session as other fixtures for consistency
    """
    # Ensure all models are imported and registered
    from backend.models.organization import Organization  # noqa: F401
    from backend.models.user import User  # noqa: F401
    
    def override_get_db():
        try:
            yield db
        finally:
            pass  # Don't close the session here, managed by db fixture
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def sample_organization(db: Session) -> Organization:
    """Create a sample organization with FREE plan"""
    org = Organization(
        id=uuid.uuid4(),
        name="Test Organization",
        slug="test-org",
        plan=PlanType.FREE
    )
    db.add(org)
    db.commit()
    db.refresh(org)
    return org


@pytest.fixture
def premium_organization(db: Session) -> Organization:
    """Create a sample organization with PREMIUM plan"""
    org = Organization(
        id=uuid.uuid4(),
        name="Premium Organization",
        slug="premium-org",
        plan=PlanType.PREMIUM
    )
    db.add(org)
    db.commit()
    db.refresh(org)
    return org


@pytest.fixture
def enterprise_organization(db: Session) -> Organization:
    """Create a sample organization with ENTERPRISE plan"""
    org = Organization(
        id=uuid.uuid4(),
        name="Enterprise Organization",
        slug="enterprise-org",
        plan=PlanType.ENTERPRISE
    )
    db.add(org)
    db.commit()
    db.refresh(org)
    return org


@pytest.fixture
def sample_user(db: Session, sample_organization: Organization) -> User:
    """Create a sample user (participant role)"""
    user = User(
        id=uuid.uuid4(),
        email="user@test.com",
        name="Test User",
        password_hash=hash_password("Password123!"),
        organization_id=sample_organization.id,
        role=UserRole.PARTICIPANT
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def facilitator_user(db: Session, sample_organization: Organization) -> User:
    """Create a facilitator user"""
    user = User(
        id=uuid.uuid4(),
        email="facilitator@test.com",
        name="Facilitator User",
        password_hash=hash_password("Password123!"),
        organization_id=sample_organization.id,
        role=UserRole.FACILITATOR
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def admin_user(db: Session, sample_organization: Organization) -> User:
    """Create an admin user"""
    user = User(
        id=uuid.uuid4(),
        email="admin@test.com",
        name="Admin User",
        password_hash=hash_password("Password123!"),
        organization_id=sample_organization.id,
        role=UserRole.ADMIN
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def other_org_user(db: Session, premium_organization: Organization) -> User:
    """Create a user from a different organization for multi-tenancy tests"""
    user = User(
        id=uuid.uuid4(),
        email="otheruser@test.com",
        name="Other Org User",
        password_hash=hash_password("Password123!"),
        organization_id=premium_organization.id,
        role=UserRole.PARTICIPANT
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_token(sample_user: User) -> str:
    """Generate a valid JWT token for sample_user"""
    token = create_access_token(
        data={
            "sub": str(sample_user.id),
            "org_id": str(sample_user.organization_id),
            "roles": [sample_user.role.value]
        }
    )
    return token


@pytest.fixture
def admin_auth_token(admin_user: User) -> str:
    """Generate a valid JWT token for admin_user"""
    token = create_access_token(
        data={
            "sub": str(admin_user.id),
            "org_id": str(admin_user.organization_id),
            "roles": [admin_user.role.value]
        }
    )
    return token


@pytest.fixture
def auth_headers(auth_token: str) -> dict:
    """Generate authorization headers with Bearer token"""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def admin_auth_headers(admin_auth_token: str) -> dict:
    """Generate authorization headers with admin Bearer token"""
    return {"Authorization": f"Bearer {admin_auth_token}"}
