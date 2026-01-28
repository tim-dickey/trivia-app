"""
Unit tests for Organization CRUD operations
Tests create, read, update operations and constraints
"""
import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid

from backend.db.crud import organization_crud
from backend.schemas.organization import OrganizationCreate
from backend.models.organization import Organization, PlanType  # noqa: F401


class TestOrganizationCRUD:
    """Test suite for Organization CRUD operations"""
    
    def test_create_organization_success(self, db: Session):
        """Test creating an organization successfully"""
        # Arrange
        org_data = OrganizationCreate(
            name="Test Organization",
            slug="test-org",
            plan=PlanType.FREE
        )
        
        # Act
        org = organization_crud.create_organization(db, org_data)
        
        # Assert
        assert org.id is not None
        assert org.name == "Test Organization"
        assert org.slug == "test-org"
        assert org.plan == PlanType.FREE
        assert org.created_at is not None
    
    def test_create_organization_with_premium_plan(self, db: Session):
        """Test creating an organization with premium plan"""
        # Arrange
        org_data = OrganizationCreate(
            name="Premium Org",
            slug="premium-org",
            plan=PlanType.PREMIUM
        )
        
        # Act
        org = organization_crud.create_organization(db, org_data)
        
        # Assert
        assert org.plan == PlanType.PREMIUM
    
    def test_get_organization_by_id_success(self, db: Session):
        """Test retrieving an organization by ID"""
        # Arrange
        org_data = OrganizationCreate(
            name="Test Organization",
            slug="test-org",
            plan=PlanType.FREE
        )
        created_org = organization_crud.create_organization(db, org_data)
        
        # Act
        retrieved_org = organization_crud.get_organization_by_id(db, created_org.id)
        
        # Assert
        assert retrieved_org is not None
        assert retrieved_org.id == created_org.id
        assert retrieved_org.name == "Test Organization"
        assert retrieved_org.slug == "test-org"
    
    def test_get_organization_by_id_not_found(self, db: Session):
        """Test retrieving a non-existent organization by ID returns None"""
        # Arrange
        non_existent_id = uuid.uuid4()
        
        # Act
        result = organization_crud.get_organization_by_id(db, non_existent_id)
        
        # Assert
        assert result is None
    
    def test_get_organization_by_slug_success(self, db: Session):
        """Test retrieving an organization by slug"""
        # Arrange
        org_data = OrganizationCreate(
            name="Test Organization",
            slug="test-org",
            plan=PlanType.FREE
        )
        created_org = organization_crud.create_organization(db, org_data)
        
        # Act
        retrieved_org = organization_crud.get_organization_by_slug(db, "test-org")
        
        # Assert
        assert retrieved_org is not None
        assert retrieved_org.id == created_org.id
        assert retrieved_org.slug == "test-org"
    
    def test_get_organization_by_slug_not_found(self, db: Session):
        """Test retrieving a non-existent organization by slug returns None"""
        # Arrange & Act
        result = organization_crud.get_organization_by_slug(db, "non-existent-slug")
        
        # Assert
        assert result is None
    
    def test_get_organizations_list(self, db: Session):
        """Test listing multiple organizations"""
        # Arrange
        orgs_data = [
            OrganizationCreate(name="Org 1", slug="org-1", plan=PlanType.FREE),
            OrganizationCreate(name="Org 2", slug="org-2", plan=PlanType.PREMIUM),
            OrganizationCreate(name="Org 3", slug="org-3", plan=PlanType.ENTERPRISE),
        ]
        for org_data in orgs_data:
            organization_crud.create_organization(db, org_data)
        
        # Act
        result = organization_crud.get_organizations(db)
        
        # Assert
        assert len(result) == 3
        slugs = [org.slug for org in result]
        assert "org-1" in slugs
        assert "org-2" in slugs
        assert "org-3" in slugs
    
    def test_get_organizations_with_pagination(self, db: Session):
        """Test listing organizations with skip and limit"""
        # Arrange
        for i in range(5):
            org_data = OrganizationCreate(
                name=f"Org {i}",
                slug=f"org-{i}",
                plan=PlanType.FREE
            )
            organization_crud.create_organization(db, org_data)
        
        # Act
        result = organization_crud.get_organizations(db, skip=2, limit=2)
        
        # Assert
        assert len(result) == 2
    
    def test_create_organization_with_duplicate_slug_fails(self, db: Session):
        """Test that creating an organization with duplicate slug fails"""
        # Arrange
        org_data1 = OrganizationCreate(
            name="First Org",
            slug="duplicate-slug",
            plan=PlanType.FREE
        )
        organization_crud.create_organization(db, org_data1)
        
        org_data2 = OrganizationCreate(
            name="Second Org",
            slug="duplicate-slug",  # Duplicate
            plan=PlanType.PREMIUM
        )
        
        # Act & Assert
        with pytest.raises(IntegrityError):
            organization_crud.create_organization(db, org_data2)
    
    def test_slug_uniqueness_enforcement(self, db: Session):
        """Test that slug uniqueness is enforced at database level"""
        # Arrange
        org1 = Organization(
            id=uuid.uuid4(),
            name="Org 1",
            slug="same-slug",
            plan=PlanType.FREE
        )
        db.add(org1)
        db.commit()
        
        org2 = Organization(
            id=uuid.uuid4(),
            name="Org 2",
            slug="same-slug",  # Duplicate
            plan=PlanType.PREMIUM
        )
        db.add(org2)
        
        # Act & Assert
        with pytest.raises(IntegrityError):
            db.commit()
    
    def test_get_organizations_empty_list(self, db: Session):
        """Test listing organizations when none exist"""
        # Arrange & Act
        result = organization_crud.get_organizations(db)
        
        # Assert
        assert result == []
    
    def test_create_organization_all_plan_types(self, db: Session):
        """Test creating organizations with all plan types"""
        # Arrange & Act & Assert
        for plan in [PlanType.FREE, PlanType.PREMIUM, PlanType.ENTERPRISE]:
            org_data = OrganizationCreate(
                name=f"{plan.value} Organization",
                slug=f"{plan.value}-org",
                plan=plan
            )
            org = organization_crud.create_organization(db, org_data)
            assert org.plan == plan
