"""
Integration tests for multi-tenant data isolation
Tests end-to-end scenarios to validate tenant boundaries are never crossed
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.models.user import User, UserRole
from backend.models.organization import Organization
from backend.core.security import create_access_token


class TestTenantIsolation:
    """Integration tests for tenant isolation via API endpoints"""
    
    def test_user_cannot_access_other_org_data_with_id_guessing(
        self,
        db: Session,
        sample_user: User,
        other_org_user: User
    ):
        """Test that knowing another org's user ID doesn't grant access"""
        # Arrange - Create tokens for both users
        user1_token = create_access_token(
            data={
                "sub": str(sample_user.id),
                "org_id": str(sample_user.organization_id),
                "roles": [sample_user.role.value]
            }
        )
        
        user2_token = create_access_token(
            data={
                "sub": str(other_org_user.id),
                "org_id": str(other_org_user.organization_id),
                "roles": [other_org_user.role.value]
            }
        )
        
        # Verify tokens are valid and contain correct organization IDs
        from backend.core.security import decode_token
        
        payload1 = decode_token(user1_token)
        payload2 = decode_token(user2_token)
        
        assert payload1["org_id"] != payload2["org_id"]
        assert payload1["sub"] == str(sample_user.id)
        assert payload2["sub"] == str(other_org_user.id)
        
        # Test actual data access isolation - user cannot access other org's data
        from backend.db.crud.base import MultiTenantCRUD
        from backend.models.user import User as UserModel
        
        user_crud = MultiTenantCRUD(UserModel)
        
        # Try to access other_org_user's data using sample_user's organization
        result = user_crud.get_by_id(db, other_org_user.id, sample_user.organization_id)
        assert result is None  # Should not be able to access cross-org data


class TestTokenSecurity:
    """Test JWT token security and organization validation"""
    
    @pytest.mark.asyncio
    async def test_token_with_modified_org_id_fails(
        self,
        db: Session,
        sample_user: User,
        premium_organization: Organization
    ):
        """Test that modifying org_id in token fails authentication"""
        from backend.core.multi_tenancy import get_current_user
        from unittest.mock import Mock
        
        # Arrange - Create token with wrong org_id
        token = create_access_token(
            data={
                "sub": str(sample_user.id),
                "org_id": str(premium_organization.id),  # Wrong org!
                "roles": [sample_user.role.value]
            }
        )
        credentials = Mock()
        credentials.credentials = token
        
        # Act & Assert - Should fail because user doesn't belong to that org
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(credentials, db)
        
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail["error"]["code"] == "USER_NOT_FOUND"
    
    @pytest.mark.asyncio
    async def test_token_without_org_id_fails(self, db: Session, sample_user: User):
        """Test that token without org_id claim fails"""
        from backend.core.multi_tenancy import get_current_user
        from unittest.mock import Mock
        
        # Arrange - Create token missing org_id
        token = create_access_token(
            data={
                "sub": str(sample_user.id),
                "roles": [sample_user.role.value]
            }
        )
        credentials = Mock()
        credentials.credentials = token
        
        # Act & Assert
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(credentials, db)
        
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail["error"]["code"] == "INVALID_TOKEN"


class TestCRUDIsolation:
    """Test CRUD operations maintain tenant isolation"""
    
    def test_create_automatically_assigns_org_id(
        self,
        db: Session,
        sample_organization: Organization,
        premium_organization: Organization
    ):
        """Test that create operations enforce organization assignment"""
        from backend.db.crud.base import MultiTenantCRUD
        from backend.models.user import User
        
        # Note: User model has organization_id
        user_crud = MultiTenantCRUD(User)
        
        # Arrange - Try to create with wrong org_id in data
        user_data = {
            "email": "test@example.com",
            "name": "Test User",
            "password_hash": "hashed",
            "organization_id": premium_organization.id,  # Should be ignored
            "role": UserRole.PARTICIPANT
        }
        
        # Act - Create with correct org_id parameter
        user = user_crud.create(db, user_data, sample_organization.id)
        
        # Assert - Should use parameter org_id, not data org_id
        assert user.organization_id == sample_organization.id
        assert user.organization_id != premium_organization.id
    
    def test_update_prevents_org_id_change(
        self,
        db: Session,
        sample_user: User,
        premium_organization: Organization
    ):
        """Test that update operations prevent changing organization_id"""
        from backend.db.crud.base import MultiTenantCRUD
        from backend.models.user import User
        
        user_crud = MultiTenantCRUD(User)
        
        # Arrange - Try to update with different org_id
        update_data = {
            "name": "Updated Name",
            "organization_id": premium_organization.id  # Should be stripped
        }
        
        # Act
        updated_user = user_crud.update(
            db,
            sample_user.id,
            sample_user.organization_id,
            update_data
        )
        
        # Assert - Organization should not change
        assert updated_user.organization_id == sample_user.organization_id
        assert updated_user.name == "Updated Name"
    
    def test_get_by_id_respects_org_boundary(
        self,
        db: Session,
        sample_user: User,
        premium_organization: Organization
    ):
        """Test that get_by_id returns None for cross-org access"""
        from backend.db.crud.base import MultiTenantCRUD
        from backend.models.user import User
        
        user_crud = MultiTenantCRUD(User)
        
        # Act - Try to get user with wrong organization
        result = user_crud.get_by_id(db, sample_user.id, premium_organization.id)
        
        # Assert - Should return None
        assert result is None
    
    def test_get_multi_filters_by_organization(
        self,
        db: Session,
        sample_user: User,
        facilitator_user: User,
        other_org_user: User,
        sample_organization: Organization
    ):
        """Test that get_multi only returns records from correct org"""
        from backend.db.crud.base import MultiTenantCRUD
        from backend.models.user import User
        
        user_crud = MultiTenantCRUD(User)
        
        # Act - Get all users for sample_organization
        users = user_crud.get_multi(db, sample_organization.id, skip=0, limit=100)
        
        # Assert - Should only include users from sample_organization
        user_ids = [user.id for user in users]
        assert sample_user.id in user_ids
        assert facilitator_user.id in user_ids
        assert other_org_user.id not in user_ids  # Different org
    
    def test_delete_respects_org_boundary(
        self,
        db: Session,
        sample_user: User,
        premium_organization: Organization
    ):
        """Test that delete fails for cross-org access"""
        from backend.db.crud.base import MultiTenantCRUD
        from backend.models.user import User
        
        user_crud = MultiTenantCRUD(User)
        
        # Act - Try to delete user with wrong organization
        success = user_crud.delete(db, sample_user.id, premium_organization.id)
        
        # Assert - Should fail (return False)
        assert success is False
        
        # Verify user still exists
        user = user_crud.get_by_id(db, sample_user.id, sample_user.organization_id)
        assert user is not None


class TestAuthenticationFlow:
    """Test authentication flow maintains organization context"""
    
    def test_login_includes_org_id_in_token(
        self,
        client: TestClient,
        sample_user: User
    ):
        """Test that login returns token with org_id claim"""
        # Arrange
        login_data = {
            "email": sample_user.email,
            "password": "Password123!"
        }
        
        # Act
        response = client.post("/api/v1/auth/login", json=login_data)
        
        # Assert
        assert response.status_code == 200
        token = response.json()["access_token"]
        
        # Decode token and verify org_id
        from backend.core.security import decode_token
        payload = decode_token(token)
        
        assert payload is not None
        assert payload["org_id"] == str(sample_user.organization_id)
        assert payload["sub"] == str(sample_user.id)
    
    def test_register_assigns_user_to_organization(
        self,
        client: TestClient,
        sample_organization: Organization
    ):
        """Test that registration assigns user to correct organization"""
        # Arrange
        register_data = {
            "email": "newuser@example.com",
            "name": "New User",
            "password": "SecurePass123!",
            "organization_slug": sample_organization.slug
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=register_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["organization_id"] == str(sample_organization.id)


class TestMultiTenantScenarios:
    """Test realistic multi-tenant scenarios"""
    
    def test_two_orgs_cannot_see_each_others_data(
        self,
        db: Session,
        sample_organization: Organization,
        premium_organization: Organization
    ):
        """Test complete isolation between two organizations"""
        from backend.db.crud.base import MultiTenantCRUD
        from backend.models.user import User
        from backend.core.security import hash_password
        
        user_crud = MultiTenantCRUD(User)
        
        # Arrange - Create users in both orgs
        org1_user1 = user_crud.create(
            db,
            {
                "email": "user1@org1.com",
                "name": "Org1 User1",
                "password_hash": hash_password("pass"),
                "role": UserRole.PARTICIPANT
            },
            sample_organization.id
        )
        
        org1_user2 = user_crud.create(
            db,
            {
                "email": "user2@org1.com",
                "name": "Org1 User2",
                "password_hash": hash_password("pass"),
                "role": UserRole.PARTICIPANT
            },
            sample_organization.id
        )
        
        org2_user1 = user_crud.create(
            db,
            {
                "email": "user1@org2.com",
                "name": "Org2 User1",
                "password_hash": hash_password("pass"),
                "role": UserRole.PARTICIPANT
            },
            premium_organization.id
        )
        
        # Act - Query users for each org
        org1_users = user_crud.get_multi(db, sample_organization.id)
        org2_users = user_crud.get_multi(db, premium_organization.id)
        
        # Assert - Each org sees only their users
        org1_user_ids = [u.id for u in org1_users]
        org2_user_ids = [u.id for u in org2_users]
        
        # Org1 sees their users
        assert org1_user1.id in org1_user_ids
        assert org1_user2.id in org1_user_ids
        
        # Org1 doesn't see org2 users
        assert org2_user1.id not in org1_user_ids
        
        # Org2 sees their users
        assert org2_user1.id in org2_user_ids
        
        # Org2 doesn't see org1 users
        assert org1_user1.id not in org2_user_ids
        assert org1_user2.id not in org2_user_ids
    
    def test_admin_cannot_access_other_org_even_with_admin_role(
        self,
        db: Session,
        admin_user: User,
        other_org_user: User
    ):
        """Test that admin role doesn't grant cross-org access"""
        from backend.db.crud.base import MultiTenantCRUD
        from backend.models.user import User
        
        user_crud = MultiTenantCRUD(User)
        
        # Act - Admin tries to access user from different org
        result = user_crud.get_by_id(
            db,
            other_org_user.id,
            admin_user.organization_id  # Admin's org, not other user's org
        )
        
        # Assert - Should fail even though requester is admin
        assert result is None


class TestSecurityVulnerabilities:
    """Test against common multi-tenant security vulnerabilities"""
    
    def test_idor_vulnerability_prevented(
        self,
        db: Session,
        sample_user: User,
        other_org_user: User
    ):
        """Test IDOR (Insecure Direct Object Reference) is prevented"""
        from backend.db.crud.base import MultiTenantCRUD
        from backend.models.user import User
        
        user_crud = MultiTenantCRUD(User)
        
        # Attacker knows victim's user ID
        victim_id = other_org_user.id
        attacker_org_id = sample_user.organization_id
        
        # Act - Attacker tries to access victim's data
        result = user_crud.get_by_id(db, victim_id, attacker_org_id)
        
        # Assert - Should fail
        assert result is None
    
    def test_mass_assignment_vulnerability_prevented(
        self,
        db: Session,
        sample_user: User,
        premium_organization: Organization
    ):
        """Test that mass assignment cannot change organization_id"""
        from backend.db.crud.base import MultiTenantCRUD
        from backend.models.user import User
        
        user_crud = MultiTenantCRUD(User)
        
        # Arrange - Malicious update with organization_id
        malicious_update = {
            "name": "Updated",
            "organization_id": premium_organization.id  # Try to switch orgs
        }
        
        # Act
        updated = user_crud.update(
            db,
            sample_user.id,
            sample_user.organization_id,
            malicious_update
        )
        
        # Assert - Organization should not change
        assert updated.organization_id == sample_user.organization_id
        assert updated.organization_id != premium_organization.id
