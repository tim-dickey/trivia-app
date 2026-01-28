"""
Unit tests for User CRUD operations with multi-tenant filtering
Tests create, read, update operations and multi-tenancy isolation
"""
import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid

from backend.db.crud import user_crud
from backend.schemas.user import UserCreate, UserUpdate
from backend.models.user import User, UserRole
from backend.models.organization import Organization, PlanType
from backend.core.security import verify_password


class TestUserCRUD:
    """Test suite for User CRUD operations"""
    
    def test_create_user_with_valid_organization(self, db: Session, sample_organization: Organization):
        """Test creating a user with valid organization"""
        # Arrange
        user_data = UserCreate(
            email="newuser@test.com",
            name="New User",
            password="SecurePassword123!",
            organization_slug=sample_organization.slug
        )
        
        # Act
        user = user_crud.create_user(db, user_data, sample_organization.id)
        
        # Assert
        assert user.id is not None
        assert user.email == "newuser@test.com"
        assert user.name == "New User"
        assert user.organization_id == sample_organization.id
        assert user.role == UserRole.PARTICIPANT  # Default role
        assert user.password_hash != "SecurePassword123!"  # Password is hashed
        assert verify_password("SecurePassword123!", user.password_hash)  # Hash is valid
    
    def test_create_user_password_is_hashed(self, db: Session, sample_organization: Organization):
        """Test that password is hashed during user creation"""
        # Arrange
        plain_password = "PlainTextPassword123!"
        user_data = UserCreate(
            email="test@test.com",
            name="Test User",
            password=plain_password,
            organization_slug=sample_organization.slug
        )
        
        # Act
        user = user_crud.create_user(db, user_data, sample_organization.id)
        
        # Assert
        assert user.password_hash != plain_password
        assert user.password_hash.startswith("$2b$")  # Bcrypt format
        assert verify_password(plain_password, user.password_hash)
    
    def test_create_user_defaults_to_participant_role(self, db: Session, sample_organization: Organization):
        """Test that newly created user has PARTICIPANT role by default"""
        # Arrange
        user_data = UserCreate(
            email="participant@test.com",
            name="Participant User",
            password="Password123!",
            organization_slug=sample_organization.slug
        )
        
        # Act
        user = user_crud.create_user(db, user_data, sample_organization.id)
        
        # Assert
        assert user.role == UserRole.PARTICIPANT
    
    def test_get_user_by_email(self, db: Session, sample_user: User):
        """Test retrieving user by email"""
        # Arrange & Act
        user = user_crud.get_user_by_email(db, sample_user.email)
        
        # Assert
        assert user is not None
        assert user.id == sample_user.id
        assert user.email == sample_user.email
    
    def test_get_user_by_email_not_found(self, db: Session):
        """Test retrieving non-existent user by email returns None"""
        # Arrange & Act
        user = user_crud.get_user_by_email(db, "nonexistent@test.com")
        
        # Assert
        assert user is None
    
    def test_get_user_by_id_with_organization_filter(self, db: Session, sample_user: User):
        """Test retrieving user by ID with organization filtering"""
        # Arrange & Act
        user = user_crud.get_user_by_id(db, sample_user.id, sample_user.organization_id)
        
        # Assert
        assert user is not None
        assert user.id == sample_user.id
        assert user.email == sample_user.email
    
    def test_get_user_by_id_wrong_organization_returns_none(self, db: Session, sample_user: User):
        """Test multi-tenant isolation: Cannot access user from different organization"""
        # Arrange
        wrong_org_id = uuid.uuid4()
        
        # Act
        user = user_crud.get_user_by_id(db, sample_user.id, wrong_org_id)
        
        # Assert
        assert user is None  # Should not return user from different organization
    
    def test_get_users_filters_by_organization(self, db: Session, sample_organization: Organization, premium_organization: Organization):
        """Test multi-tenant filtering: Users only see their org's users"""
        # Arrange
        # Create users in sample_organization
        user1_data = UserCreate(
            email="user1@test.com",
            name="User 1",
            password="Password123!",
            organization_slug=sample_organization.slug
        )
        user2_data = UserCreate(
            email="user2@test.com",
            name="User 2",
            password="Password123!",
            organization_slug=sample_organization.slug
        )
        user_crud.create_user(db, user1_data, sample_organization.id)
        user_crud.create_user(db, user2_data, sample_organization.id)
        
        # Create user in premium_organization
        user3_data = UserCreate(
            email="user3@premium.com",
            name="User 3",
            password="Password123!",
            organization_slug=premium_organization.slug
        )
        user_crud.create_user(db, user3_data, premium_organization.id)
        
        # Act
        sample_org_users = user_crud.get_users(db, sample_organization.id)
        premium_org_users = user_crud.get_users(db, premium_organization.id)
        
        # Assert
        assert len(sample_org_users) == 2
        assert all(u.organization_id == sample_organization.id for u in sample_org_users)
        
        assert len(premium_org_users) == 1
        assert all(u.organization_id == premium_organization.id for u in premium_org_users)
    
    def test_get_users_with_pagination(self, db: Session, sample_organization: Organization):
        """Test listing users with pagination"""
        # Arrange
        for i in range(5):
            user_data = UserCreate(
                email=f"user{i}@test.com",
                name=f"User {i}",
                password="Password123!",
                organization_slug=sample_organization.slug
            )
            user_crud.create_user(db, user_data, sample_organization.id)
        
        # Act
        result = user_crud.get_users(db, sample_organization.id, skip=2, limit=2)
        
        # Assert
        assert len(result) == 2
    
    def test_update_user_profile(self, db: Session, sample_user: User):
        """Test updating user profile"""
        # Arrange
        update_data = UserUpdate(
            email="updated@test.com",
            name="Updated Name"
        )
        
        # Act
        updated_user = user_crud.update_user(
            db, 
            sample_user.id, 
            sample_user.organization_id, 
            update_data
        )
        
        # Assert
        assert updated_user is not None
        assert updated_user.email == "updated@test.com"
        assert updated_user.name == "Updated Name"
    
    def test_update_user_partial_update(self, db: Session, sample_user: User):
        """Test partial update (only some fields)"""
        # Arrange
        original_email = sample_user.email
        update_data = UserUpdate(name="New Name Only")
        
        # Act
        updated_user = user_crud.update_user(
            db, 
            sample_user.id, 
            sample_user.organization_id, 
            update_data
        )
        
        # Assert
        assert updated_user is not None
        assert updated_user.name == "New Name Only"
        assert updated_user.email == original_email  # Email unchanged
    
    def test_update_user_wrong_organization_returns_none(self, db: Session, sample_user: User):
        """Test multi-tenant isolation: Cannot update user from different organization"""
        # Arrange
        wrong_org_id = uuid.uuid4()
        update_data = UserUpdate(name="Hacker Name")
        
        # Act
        result = user_crud.update_user(db, sample_user.id, wrong_org_id, update_data)
        
        # Assert
        assert result is None
    
    def test_update_password(self, db: Session, sample_user: User):
        """Test updating user password"""
        # Arrange
        new_password = "NewSecurePassword123!"
        old_hash = sample_user.password_hash
        
        # Act
        updated_user = user_crud.update_password(
            db,
            sample_user.id,
            sample_user.organization_id,
            new_password
        )
        
        # Refresh to get latest data from database
        db.refresh(updated_user)
        
        # Assert
        assert updated_user is not None
        assert updated_user.password_hash != old_hash  # Hash changed
        assert verify_password(new_password, updated_user.password_hash)  # New password works
        assert not verify_password("Password123!", updated_user.password_hash)  # Old password doesn't work
    
    def test_update_password_wrong_organization_returns_none(self, db: Session, sample_user: User):
        """Test multi-tenant isolation: Cannot change password for user from different organization"""
        # Arrange
        wrong_org_id = uuid.uuid4()
        
        # Act
        result = user_crud.update_password(db, sample_user.id, wrong_org_id, "NewPassword123!")
        
        # Assert
        assert result is None
    
    def test_prevent_cross_organization_access(self, db: Session, sample_user: User, other_org_user: User):
        """Test that users cannot access data from other organizations"""
        # Arrange & Act
        # Try to get other_org_user using sample_user's organization_id
        result = user_crud.get_user_by_id(
            db, 
            other_org_user.id, 
            sample_user.organization_id
        )
        
        # Assert
        assert result is None  # Should not return user from different organization
    
    def test_create_user_with_duplicate_email_fails(self, db: Session, sample_organization: Organization, sample_user: User):
        """Test that creating user with duplicate email fails"""
        # Arrange
        user_data = UserCreate(
            email=sample_user.email,  # Duplicate email
            name="Another User",
            password="Password123!",
            organization_slug=sample_organization.slug
        )
        
        # Act & Assert
        with pytest.raises(IntegrityError):
            user_crud.create_user(db, user_data, sample_organization.id)
