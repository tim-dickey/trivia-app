"""
Unit tests for Organization model
Tests model creation, constraints, relationships, and cascade behavior
"""
import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid

from backend.models.organization import Organization, PlanType
from backend.models.user import User, UserRole
from backend.core.security import hash_password


class TestOrganizationModel:
    """Test suite for Organization model"""
    
    def test_create_organization_with_valid_data(self, db: Session):
        """Test creating an organization with valid data"""
        # Arrange & Act
        org = Organization(
            id=uuid.uuid4(),
            name="Test Organization",
            slug="test-org",
            plan=PlanType.FREE
        )
        db.add(org)
        db.commit()
        db.refresh(org)
        
        # Assert
        assert org.id is not None
        assert org.name == "Test Organization"
        assert org.slug == "test-org"
        assert org.plan == PlanType.FREE
        assert org.created_at is not None
    
    def test_create_organization_defaults_to_free_plan(self, db: Session):
        """Test that organization defaults to FREE plan if not specified"""
        # Arrange & Act
        org = Organization(
            id=uuid.uuid4(),
            name="Test Organization",
            slug="test-org"
        )
        db.add(org)
        db.commit()
        db.refresh(org)
        
        # Assert
        assert org.plan == PlanType.FREE
    
    def test_organization_slug_must_be_unique(self, db: Session):
        """Test that organization slug must be unique"""
        # Arrange
        org1 = Organization(
            id=uuid.uuid4(),
            name="Organization 1",
            slug="test-org",
            plan=PlanType.FREE
        )
        db.add(org1)
        db.commit()
        
        org2 = Organization(
            id=uuid.uuid4(),
            name="Organization 2",
            slug="test-org",  # Duplicate slug
            plan=PlanType.PREMIUM
        )
        db.add(org2)
        
        # Act & Assert
        with pytest.raises(IntegrityError):
            db.commit()
    
    def test_organization_plan_enum_validation(self, db: Session):
        """Test that only valid plan types are accepted"""
        # Arrange
        valid_plans = [PlanType.FREE, PlanType.PREMIUM, PlanType.ENTERPRISE]
        
        # Act & Assert
        for plan in valid_plans:
            org = Organization(
                id=uuid.uuid4(),
                name=f"Org {plan.value}",
                slug=f"org-{plan.value}",
                plan=plan
            )
            db.add(org)
            db.commit()
            assert org.plan == plan
            db.rollback()  # Clean up for next iteration
    
    def test_organization_has_users_relationship(self, db: Session):
        """Test that organization has relationship with users"""
        # Arrange
        org = Organization(
            id=uuid.uuid4(),
            name="Test Organization",
            slug="test-org",
            plan=PlanType.FREE
        )
        db.add(org)
        db.commit()
        db.refresh(org)
        
        # Act - Create users for the organization
        user1 = User(
            id=uuid.uuid4(),
            email="user1@test.com",
            name="User 1",
            password_hash=hash_password("password123"),
            organization_id=org.id,
            role=UserRole.PARTICIPANT
        )
        user2 = User(
            id=uuid.uuid4(),
            email="user2@test.com",
            name="User 2",
            password_hash=hash_password("password123"),
            organization_id=org.id,
            role=UserRole.FACILITATOR
        )
        db.add(user1)
        db.add(user2)
        db.commit()
        db.refresh(org)
        
        # Assert
        assert len(org.users) == 2
        assert user1 in org.users
        assert user2 in org.users
    
    def test_organization_cascade_delete_removes_users(self, db: Session):
        """Test that deleting an organization cascades to delete its users"""
        # Arrange
        org = Organization(
            id=uuid.uuid4(),
            name="Test Organization",
            slug="test-org",
            plan=PlanType.FREE
        )
        db.add(org)
        db.commit()
        
        user = User(
            id=uuid.uuid4(),
            email="user@test.com",
            name="Test User",
            password_hash=hash_password("password123"),
            organization_id=org.id,
            role=UserRole.PARTICIPANT
        )
        db.add(user)
        db.commit()
        
        user_id = user.id
        
        # Act - Delete organization
        db.delete(org)
        db.commit()
        
        # Assert - User should be deleted due to cascade
        deleted_user = db.query(User).filter(User.id == user_id).first()
        assert deleted_user is None
    
    def test_organization_name_cannot_be_null(self, db: Session):
        """Test that organization name is required"""
        # Arrange
        org = Organization(
            id=uuid.uuid4(),
            name=None,  # Invalid
            slug="test-org",
            plan=PlanType.FREE
        )
        db.add(org)
        
        # Act & Assert
        with pytest.raises(IntegrityError):
            db.commit()
    
    def test_organization_slug_cannot_be_null(self, db: Session):
        """Test that organization slug is required"""
        # Arrange
        org = Organization(
            id=uuid.uuid4(),
            name="Test Organization",
            slug=None,  # Invalid
            plan=PlanType.FREE
        )
        db.add(org)
        
        # Act & Assert
        with pytest.raises(IntegrityError):
            db.commit()
    
    def test_organization_repr(self, db: Session):
        """Test organization __repr__ method"""
        # Arrange & Act
        org = Organization(
            id=uuid.uuid4(),
            name="Test Organization",
            slug="test-org",
            plan=PlanType.PREMIUM
        )
        db.add(org)
        db.commit()
        db.refresh(org)
        
        # Assert
        repr_str = repr(org)
        assert "Organization" in repr_str
        assert "test-org" in repr_str
        assert "premium" in repr_str.lower()
        assert str(org.id) in repr_str
