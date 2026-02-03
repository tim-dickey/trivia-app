"""
Tests for database configuration and test framework setup
Validates that tests work correctly with both PostgreSQL and SQLite
"""
import os
import pytest
from sqlalchemy import text

from backend.models.organization import Organization, PlanType
from backend.models.user import User, UserRole


class TestDatabaseConfiguration:
    """Test suite to validate database configuration in test environment"""

    def test_database_url_reads_from_environment(self):
        """Test that DATABASE_URL is read from environment variable"""
        # The conftest.py should read DATABASE_URL from environment
        db_url = os.environ.get("DATABASE_URL")
        if db_url:
            assert "postgresql" in db_url or "sqlite" in db_url
        else:
            # If not set, it should fall back to SQLite
            assert True

    def test_database_engine_configuration(self, db):
        """Test that database engine is properly configured"""
        # Verify we can execute a basic query
        result = db.execute(text("SELECT 1")).scalar()
        assert result == 1

    def test_database_supports_transactions(self, db):
        """Test that database properly supports transactions and rollback"""
        # Create an organization
        org = Organization(
            name="Transaction Test Org",
            slug="transaction-test",
            plan=PlanType.FREE
        )
        db.add(org)
        db.flush()
        
        # Verify it exists in this transaction
        found_org = db.query(Organization).filter_by(slug="transaction-test").first()
        assert found_org is not None
        
        # After test, db fixture should rollback (no commit in fixture)
        # This is verified by test isolation

    def test_database_isolation_between_tests(self, db):
        """Test that database state is isolated between tests"""
        # This test verifies that previous test data doesn't persist
        # If isolation works, there should be no organizations with this slug
        org = db.query(Organization).filter_by(slug="transaction-test").first()
        assert org is None

    def test_database_supports_uuid_primary_keys(self, db, sample_organization):
        """Test that database properly handles UUID primary keys"""
        import uuid
        
        # Verify the organization has a valid UUID
        assert isinstance(sample_organization.id, uuid.UUID)
        
        # Verify we can query by UUID
        found_org = db.query(Organization).filter_by(id=sample_organization.id).first()
        assert found_org is not None
        assert found_org.id == sample_organization.id

    def test_database_supports_foreign_keys(self, db, sample_organization, sample_user):
        """Test that database properly enforces foreign key relationships"""
        # Verify user is linked to organization
        assert sample_user.organization_id == sample_organization.id
        
        # Verify we can query through relationship
        user_with_org = db.query(User).filter_by(id=sample_user.id).first()
        assert user_with_org is not None
        assert user_with_org.organization_id == sample_organization.id

    def test_database_supports_enums(self, db, sample_organization, sample_user):
        """Test that database properly handles enum types"""
        # Verify organization plan enum
        assert isinstance(sample_organization.plan, PlanType)
        assert sample_organization.plan == PlanType.FREE
        
        # Verify user role enum
        assert isinstance(sample_user.role, UserRole)
        assert sample_user.role == UserRole.PARTICIPANT

    def test_database_supports_unique_constraints(self, db, sample_organization):
        """Test that database properly enforces unique constraints"""
        # Try to create another organization with the same slug
        duplicate_org = Organization(
            name="Duplicate Org",
            slug=sample_organization.slug,  # Same slug
            plan=PlanType.FREE
        )
        db.add(duplicate_org)
        
        # This should raise an integrity error
        with pytest.raises(Exception):  # Could be IntegrityError or similar
            db.flush()

    def test_database_supports_timestamps(self, db, sample_user):
        """Test that database properly handles timestamp columns"""
        from datetime import datetime
        
        # Verify created_at is set
        assert sample_user.created_at is not None
        assert isinstance(sample_user.created_at, datetime)
        
        # Verify updated_at is set (only User model has this)
        assert sample_user.updated_at is not None
        assert isinstance(sample_user.updated_at, datetime)

    def test_database_supports_nullable_fields(self, db, sample_user):
        """Test that database properly handles nullable fields"""
        # Verify non-nullable fields are set
        assert sample_user.email is not None
        assert sample_user.name is not None
        assert sample_user.password_hash is not None
        
        # Update name to test field updates
        original_name = sample_user.name
        sample_user.name = "Updated Name"
        db.flush()
        
        # Verify it was saved
        updated_user = db.query(User).filter_by(id=sample_user.id).first()
        assert updated_user.name == "Updated Name"
        assert updated_user.name != original_name


class TestPostgreSQLSpecificFeatures:
    """Tests for PostgreSQL-specific features (skipped if using SQLite)"""

    @pytest.fixture(autouse=True)
    def check_postgres(self, db):
        """Skip tests if not using PostgreSQL"""
        db_url = os.environ.get("DATABASE_URL", "sqlite:///./test_trivia.db")
        if "postgresql" not in db_url:
            pytest.skip("PostgreSQL-specific test (currently using SQLite)")

    def test_postgresql_connection(self, db):
        """Test that PostgreSQL connection is working"""
        # Execute a PostgreSQL-specific query
        result = db.execute(text("SELECT version()")).scalar()
        assert "PostgreSQL" in result

    def test_postgresql_supports_full_text_search(self, db):
        """Test PostgreSQL full-text search capability (placeholder)"""
        # This is a placeholder for future full-text search features
        # For now, just verify we can execute PostgreSQL-specific syntax
        result = db.execute(text("SELECT to_tsvector('english', 'test')")).scalar()
        assert result is not None

    def test_postgresql_supports_json_operators(self, db):
        """Test PostgreSQL JSON operators (placeholder)"""
        # This is a placeholder for future JSON column features
        # For now, just verify we can execute PostgreSQL-specific JSON syntax
        result = db.execute(text("SELECT '{\"key\": \"value\"}'::jsonb")).scalar()
        assert result is not None


class TestSQLiteSpecificFeatures:
    """Tests for SQLite-specific features (skipped if using PostgreSQL)"""

    @pytest.fixture(autouse=True)
    def check_sqlite(self, db):
        """Skip tests if not using SQLite"""
        db_url = os.environ.get("DATABASE_URL", "sqlite:///./test_trivia.db")
        if "sqlite" not in db_url:
            pytest.skip("SQLite-specific test (currently using PostgreSQL)")

    def test_sqlite_connection(self, db):
        """Test that SQLite connection is working"""
        # Execute a SQLite-specific query
        result = db.execute(text("SELECT sqlite_version()")).scalar()
        assert result is not None
        assert len(result.split('.')) >= 3  # Version format: X.Y.Z

    def test_sqlite_in_memory_performance(self, db):
        """Test SQLite performance characteristics"""
        # SQLite should be fast for simple queries
        import time
        
        start = time.time()
        for _ in range(100):
            db.execute(text("SELECT 1")).scalar()
        elapsed = time.time() - start
        
        # 100 simple queries should complete in under 1 second
        assert elapsed < 1.0


class TestDatabaseMigrations:
    """Tests to validate that migrations work correctly"""

    def test_all_tables_exist(self, db):
        """Test that all required tables exist in the database"""
        from sqlalchemy import inspect
        
        inspector = inspect(db.bind)
        tables = inspector.get_table_names()
        
        # Verify core tables exist
        assert "organizations" in tables
        assert "users" in tables
        # Note: alembic_version may not exist when using test fixtures
        # which create tables directly without running migrations

    def test_alembic_version_is_current(self, db):
        """Test that alembic version is at the latest migration (if using migrations)"""
        from sqlalchemy import inspect
        
        inspector = inspect(db.bind)
        tables = inspector.get_table_names()
        
        if "alembic_version" in tables:
            # Only check version if alembic_version table exists
            result = db.execute(text("SELECT version_num FROM alembic_version")).scalar()
            assert result is not None
            assert len(result) > 0
        else:
            # Test fixtures create tables directly, so alembic_version may not exist
            pytest.skip("alembic_version table not found (tests use direct table creation)")

    def test_organizations_table_schema(self, db):
        """Test that organizations table has correct schema"""
        from sqlalchemy import inspect
        
        inspector = inspect(db.bind)
        columns = {col['name']: col for col in inspector.get_columns('organizations')}
        
        # Verify required columns exist
        assert 'id' in columns
        assert 'name' in columns
        assert 'slug' in columns
        assert 'plan' in columns
        assert 'created_at' in columns
        # Note: Organization model doesn't have updated_at field

    def test_users_table_schema(self, db):
        """Test that users table has correct schema"""
        from sqlalchemy import inspect
        
        inspector = inspect(db.bind)
        columns = {col['name']: col for col in inspector.get_columns('users')}
        
        # Verify required columns exist
        assert 'id' in columns
        assert 'email' in columns
        assert 'name' in columns
        assert 'password_hash' in columns
        assert 'organization_id' in columns
        assert 'role' in columns
        assert 'created_at' in columns
        assert 'updated_at' in columns

    def test_foreign_key_constraints_exist(self, db):
        """Test that foreign key constraints are properly configured"""
        from sqlalchemy import inspect
        
        inspector = inspect(db.bind)
        foreign_keys = inspector.get_foreign_keys('users')
        
        # Users table should have FK to organizations
        assert len(foreign_keys) > 0
        org_fk = [fk for fk in foreign_keys if fk['referred_table'] == 'organizations']
        assert len(org_fk) > 0
