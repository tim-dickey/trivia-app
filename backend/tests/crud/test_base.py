"""
Tests for base multi-tenant CRUD class
Validates automatic organization scoping and data isolation
"""
import pytest
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session
from uuid import uuid4
import uuid

from backend.db.crud.base import MultiTenantCRUD
from backend.core.database import Base
from backend.models.organization import Organization


# Test model for CRUD operations
class TestSession(Base):
    """Test model with organization_id for multi-tenant CRUD testing"""
    __tablename__ = "test_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    organization_id = Column(UUID(as_uuid=True), nullable=False, index=True)


# Test model without organization_id (should fail validation)
class InvalidModel(Base):
    """Test model without organization_id"""
    __tablename__ = "invalid_model"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)


class TestMultiTenantCRUDInitialization:
    """Test suite for MultiTenantCRUD initialization"""
    
    def test_initialization_with_valid_model_succeeds(self):
        """Test that initialization succeeds with a model that has organization_id"""
        # Act & Assert - Should not raise
        crud = MultiTenantCRUD(TestSession)
        assert crud.model == TestSession
    
    def test_initialization_without_organization_id_raises_error(self):
        """Test that initialization fails if model lacks organization_id column"""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            MultiTenantCRUD(InvalidModel)
        
        assert "must have 'organization_id' column" in str(exc_info.value)


class TestMultiTenantCRUDOperations:
    """Test suite for MultiTenantCRUD operations"""
    
    @pytest.fixture
    def test_crud(self):
        """Create CRUD instance for test model"""
        return MultiTenantCRUD(TestSession)
    
    @pytest.fixture
    def setup_db(self, db: Session):
        """Setup test tables"""
        Base.metadata.create_all(bind=db.get_bind())
        yield db
        # Cleanup handled by conftest.py
    
    def test_create_assigns_organization_id(
        self,
        setup_db: Session,
        test_crud: MultiTenantCRUD,
        sample_organization: Organization
    ):
        """Test that create automatically assigns organization_id"""
        # Arrange
        data = {"name": "Test Session"}
        
        # Act
        obj = test_crud.create(setup_db, data, sample_organization.id)
        
        # Assert
        assert obj.organization_id == sample_organization.id
        assert obj.name == "Test Session"
        assert obj.id is not None
    
    def test_create_prevents_organization_id_override(
        self,
        setup_db: Session,
        test_crud: MultiTenantCRUD,
        sample_organization: Organization,
        premium_organization: Organization
    ):
        """Test that create prevents overriding organization_id"""
        # Arrange - Try to set wrong organization
        data = {
            "name": "Test Session",
            "organization_id": premium_organization.id  # Should be overridden
        }
        
        # Act
        obj = test_crud.create(setup_db, data, sample_organization.id)
        
        # Assert - Should use the provided org_id, not the one in data
        assert obj.organization_id == sample_organization.id
    
    def test_get_by_id_returns_correct_object(
        self,
        setup_db: Session,
        test_crud: MultiTenantCRUD,
        sample_organization: Organization
    ):
        """Test that get_by_id returns object with correct organization"""
        # Arrange
        obj = test_crud.create(setup_db, {"name": "Session 1"}, sample_organization.id)
        
        # Act
        retrieved = test_crud.get_by_id(setup_db, obj.id, sample_organization.id)
        
        # Assert
        assert retrieved is not None
        assert retrieved.id == obj.id
        assert retrieved.organization_id == sample_organization.id
    
    def test_get_by_id_with_wrong_org_returns_none(
        self,
        setup_db: Session,
        test_crud: MultiTenantCRUD,
        sample_organization: Organization,
        premium_organization: Organization
    ):
        """Test that get_by_id returns None when using wrong organization_id"""
        # Arrange
        obj = test_crud.create(setup_db, {"name": "Session 1"}, sample_organization.id)
        
        # Act - Try to get with different organization
        retrieved = test_crud.get_by_id(setup_db, obj.id, premium_organization.id)
        
        # Assert
        assert retrieved is None
    
    def test_get_multi_filters_by_organization(
        self,
        setup_db: Session,
        test_crud: MultiTenantCRUD,
        sample_organization: Organization,
        premium_organization: Organization
    ):
        """Test that get_multi only returns objects from the specified organization"""
        # Arrange - Create objects in different organizations
        obj1 = test_crud.create(setup_db, {"name": "Session 1"}, sample_organization.id)
        obj2 = test_crud.create(setup_db, {"name": "Session 2"}, sample_organization.id)
        obj3 = test_crud.create(setup_db, {"name": "Session 3"}, premium_organization.id)
        
        # Act
        org1_objects = test_crud.get_multi(setup_db, sample_organization.id)
        org2_objects = test_crud.get_multi(setup_db, premium_organization.id)
        
        # Assert
        assert len(org1_objects) == 2
        assert all(obj.organization_id == sample_organization.id for obj in org1_objects)
        
        assert len(org2_objects) == 1
        assert org2_objects[0].organization_id == premium_organization.id
    
    def test_get_multi_respects_pagination(
        self,
        setup_db: Session,
        test_crud: MultiTenantCRUD,
        sample_organization: Organization
    ):
        """Test that get_multi respects skip and limit parameters"""
        # Arrange - Create 5 objects
        for i in range(5):
            test_crud.create(setup_db, {"name": f"Session {i}"}, sample_organization.id)
        
        # Act
        page1 = test_crud.get_multi(setup_db, sample_organization.id, skip=0, limit=2)
        page2 = test_crud.get_multi(setup_db, sample_organization.id, skip=2, limit=2)
        
        # Assert
        assert len(page1) == 2
        assert len(page2) == 2
        assert page1[0].id != page2[0].id
    
    def test_update_modifies_object(
        self,
        setup_db: Session,
        test_crud: MultiTenantCRUD,
        sample_organization: Organization
    ):
        """Test that update successfully modifies an object"""
        # Arrange
        obj = test_crud.create(setup_db, {"name": "Original"}, sample_organization.id)
        
        # Act
        updated = test_crud.update(
            setup_db,
            obj.id,
            sample_organization.id,
            {"name": "Updated"}
        )
        
        # Assert
        assert updated is not None
        assert updated.id == obj.id
        assert updated.name == "Updated"
        assert updated.organization_id == sample_organization.id
    
    def test_update_with_wrong_org_returns_none(
        self,
        setup_db: Session,
        test_crud: MultiTenantCRUD,
        sample_organization: Organization,
        premium_organization: Organization
    ):
        """Test that update returns None when using wrong organization_id"""
        # Arrange
        obj = test_crud.create(setup_db, {"name": "Original"}, sample_organization.id)
        
        # Act - Try to update with different organization
        updated = test_crud.update(
            setup_db,
            obj.id,
            premium_organization.id,
            {"name": "Updated"}
        )
        
        # Assert
        assert updated is None
    
    def test_update_prevents_organization_change(
        self,
        setup_db: Session,
        test_crud: MultiTenantCRUD,
        sample_organization: Organization,
        premium_organization: Organization
    ):
        """Test that update prevents changing organization_id"""
        # Arrange
        obj = test_crud.create(setup_db, {"name": "Original"}, sample_organization.id)
        
        # Act - Try to change organization_id
        updated = test_crud.update(
            setup_db,
            obj.id,
            sample_organization.id,
            {"name": "Updated", "organization_id": premium_organization.id}
        )
        
        # Assert - organization_id should remain unchanged
        assert updated is not None
        assert updated.organization_id == sample_organization.id
    
    def test_delete_removes_object(
        self,
        setup_db: Session,
        test_crud: MultiTenantCRUD,
        sample_organization: Organization
    ):
        """Test that delete successfully removes an object"""
        # Arrange
        obj = test_crud.create(setup_db, {"name": "To Delete"}, sample_organization.id)
        
        # Act
        result = test_crud.delete(setup_db, obj.id, sample_organization.id)
        
        # Assert
        assert result is True
        assert test_crud.get_by_id(setup_db, obj.id, sample_organization.id) is None
    
    def test_delete_with_wrong_org_returns_false(
        self,
        setup_db: Session,
        test_crud: MultiTenantCRUD,
        sample_organization: Organization,
        premium_organization: Organization
    ):
        """Test that delete returns False when using wrong organization_id"""
        # Arrange
        obj = test_crud.create(setup_db, {"name": "To Delete"}, sample_organization.id)
        
        # Act - Try to delete with different organization
        result = test_crud.delete(setup_db, obj.id, premium_organization.id)
        
        # Assert
        assert result is False
        # Object should still exist
        assert test_crud.get_by_id(setup_db, obj.id, sample_organization.id) is not None
    
    def test_count_returns_correct_number(
        self,
        setup_db: Session,
        test_crud: MultiTenantCRUD,
        sample_organization: Organization,
        premium_organization: Organization
    ):
        """Test that count returns correct number per organization"""
        # Arrange
        for i in range(3):
            test_crud.create(setup_db, {"name": f"Org1 Session {i}"}, sample_organization.id)
        for i in range(2):
            test_crud.create(setup_db, {"name": f"Org2 Session {i}"}, premium_organization.id)
        
        # Act
        count1 = test_crud.count(setup_db, sample_organization.id)
        count2 = test_crud.count(setup_db, premium_organization.id)
        
        # Assert
        assert count1 == 3
        assert count2 == 2
