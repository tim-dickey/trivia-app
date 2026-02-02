"""
Tests for multi-tenancy middleware and dependencies
Validates JWT extraction, organization scoping, and security isolation
"""
import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from backend.core.multi_tenancy import (
    get_current_user,
    get_current_organization,
    require_organization_access
)
from backend.core.security import create_access_token
from backend.models.user import User, UserRole
from backend.models.organization import Organization
from unittest.mock import Mock


class TestGetCurrentUser:
    """Test suite for get_current_user dependency"""
    
    @pytest.mark.asyncio
    async def test_valid_token_returns_user(self, db: Session, sample_user: User):
        """Test that valid token returns the correct user"""
        # Arrange
        token = create_access_token(
            data={
                "sub": str(sample_user.id),
                "org_id": str(sample_user.organization_id),
                "roles": [sample_user.role.value]
            }
        )
        credentials = Mock()
        credentials.credentials = token
        
        # Act
        user = await get_current_user(credentials, db)
        
        # Assert
        assert user.id == sample_user.id
        assert user.email == sample_user.email
        assert user.organization_id == sample_user.organization_id
    
    @pytest.mark.asyncio
    async def test_invalid_token_raises_401(self, db: Session):
        """Test that invalid token raises 401 error"""
        # Arrange
        credentials = Mock()
        credentials.credentials = "invalid_token"
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(credentials, db)
        
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail["error"]["code"] == "INVALID_TOKEN"
    
    @pytest.mark.asyncio
    async def test_token_without_user_id_raises_401(self, db: Session):
        """Test that token without 'sub' claim raises 401"""
        # Arrange
        token = create_access_token(data={"org_id": str(uuid4())})
        credentials = Mock()
        credentials.credentials = token
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(credentials, db)
        
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail["error"]["code"] == "INVALID_TOKEN"
    
    @pytest.mark.asyncio
    async def test_token_without_org_id_raises_401(self, db: Session):
        """Test that token without 'org_id' claim raises 401"""
        # Arrange
        token = create_access_token(data={"sub": str(uuid4())})
        credentials = Mock()
        credentials.credentials = token
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(credentials, db)
        
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail["error"]["code"] == "INVALID_TOKEN"
    
    @pytest.mark.asyncio
    async def test_nonexistent_user_raises_401(self, db: Session, sample_organization: Organization):
        """Test that token for non-existent user raises 401"""
        # Arrange
        fake_user_id = uuid4()
        token = create_access_token(
            data={
                "sub": str(fake_user_id),
                "org_id": str(sample_organization.id),
                "roles": ["participant"]
            }
        )
        credentials = Mock()
        credentials.credentials = token
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(credentials, db)
        
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail["error"]["code"] == "USER_NOT_FOUND"
    
    @pytest.mark.asyncio
    async def test_wrong_organization_raises_401(self, db: Session, sample_user: User):
        """Test that token with wrong organization_id raises 401"""
        # Arrange
        wrong_org_id = uuid4()
        token = create_access_token(
            data={
                "sub": str(sample_user.id),
                "org_id": str(wrong_org_id),
                "roles": [sample_user.role.value]
            }
        )
        credentials = Mock()
        credentials.credentials = token
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(credentials, db)
        
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail["error"]["code"] == "USER_NOT_FOUND"


class TestGetCurrentOrganization:
    """Test suite for get_current_organization dependency"""
    
    @pytest.mark.asyncio
    async def test_returns_user_organization(self, db: Session, sample_user: User, sample_organization: Organization):
        """Test that it returns the organization of the current user"""
        # Act
        org = await get_current_organization(sample_user, db)
        
        # Assert
        assert org.id == sample_organization.id
        assert org.slug == sample_organization.slug
    
    @pytest.mark.asyncio
    async def test_user_with_deleted_org_raises_404(self, db: Session, sample_user: User, sample_organization: Organization):
        """Test that user with deleted organization raises 404"""
        # Arrange - Delete organization
        db.delete(sample_organization)
        db.commit()
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_current_organization(sample_user, db)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail["error"]["code"] == "ORG_NOT_FOUND"


class TestRequireOrganizationAccess:
    """Test suite for require_organization_access dependency"""
    
    def test_returns_organization_id(self, sample_user: User):
        """Test that it returns the organization ID from user"""
        # Act
        org_id = require_organization_access(sample_user)
        
        # Assert
        assert org_id == sample_user.organization_id


class TestMultiTenantIsolation:
    """Integration tests for multi-tenant data isolation"""
    
    @pytest.mark.asyncio
    async def test_users_cannot_access_other_org_data(
        self,
        db: Session,
        sample_user: User,
        other_org_user: User
    ):
        """Test that users cannot access data from other organizations via JWT"""
        # Arrange - Create token for user in org A
        token = create_access_token(
            data={
                "sub": str(sample_user.id),
                "org_id": str(sample_user.organization_id),
                "roles": [sample_user.role.value]
            }
        )
        credentials = Mock()
        credentials.credentials = token
        
        # Act - Get current user (should succeed)
        user = await get_current_user(credentials, db)
        
        # Assert - User belongs to correct organization
        assert user.organization_id == sample_user.organization_id
        assert user.organization_id != other_org_user.organization_id
    
    @pytest.mark.asyncio
    async def test_tampered_token_with_different_org_fails(
        self,
        db: Session,
        sample_user: User,
        premium_organization: Organization
    ):
        """Test that tampering with org_id in token fails authentication"""
        # Arrange - Create token with wrong organization_id
        token = create_access_token(
            data={
                "sub": str(sample_user.id),
                "org_id": str(premium_organization.id),  # Wrong org!
                "roles": [sample_user.role.value]
            }
        )
        credentials = Mock()
        credentials.credentials = token
        
        # Act & Assert - Should fail because user doesn't exist in that org
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(credentials, db)
        
        assert exc_info.value.status_code == 401
