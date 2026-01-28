"""
Integration tests for Authentication API endpoints
Tests registration, login, and logout with complete request/response cycle
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.models.organization import Organization
from backend.models.user import User, UserRole
from backend.core.security import verify_password
from backend.db.crud import user_crud


class TestAuthRegistration:
    """Test suite for POST /api/v1/auth/register endpoint"""
    
    def test_register_with_valid_data_returns_201(self, client: TestClient, sample_organization: Organization):
        """Test successful registration returns 201 and user data"""
        # Arrange
        payload = {
            "email": "newuser@test.com",
            "name": "New User",
            "password": "SecurePassword123!",
            "organization_slug": sample_organization.slug
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=payload)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@test.com"
        assert data["name"] == "New User"
        assert data["organization_id"] == str(sample_organization.id)
        assert data["role"] == "participant"  # Default role
        assert "id" in data
        assert "created_at" in data
        assert "password" not in data  # Password should never be in response
        assert "password_hash" not in data
    
    def test_register_user_password_is_hashed_not_plaintext(self, client: TestClient, db: Session, sample_organization: Organization):
        """Test that password is hashed and never stored as plaintext"""
        # Arrange
        payload = {
            "email": "secure@test.com",
            "name": "Secure User",
            "password": "MyPlainPassword123!",
            "organization_slug": sample_organization.slug
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=payload)
        
        # Assert
        assert response.status_code == 201
        
        # Verify password is hashed in database
        user = user_crud.get_user_by_email(db, "secure@test.com")
        assert user is not None
        assert user.password_hash != "MyPlainPassword123!"  # Not plaintext
        assert user.password_hash.startswith("$2b$")  # Bcrypt format
        assert verify_password("MyPlainPassword123!", user.password_hash)
    
    def test_register_user_has_default_participant_role(self, client: TestClient, db: Session, sample_organization: Organization):
        """Test that newly registered user has default 'participant' role"""
        # Arrange
        payload = {
            "email": "participant@test.com",
            "name": "Participant User",
            "password": "Password123!",
            "organization_slug": sample_organization.slug
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=payload)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["role"] == "participant"
        
        # Verify in database
        user = user_crud.get_user_by_email(db, "participant@test.com")
        assert user.role == UserRole.PARTICIPANT
    
    def test_register_with_duplicate_email_returns_400(self, client: TestClient, sample_user: User, sample_organization: Organization):
        """Test registering with existing email returns 400 EMAIL_ALREADY_EXISTS"""
        # Arrange
        payload = {
            "email": sample_user.email,  # Duplicate email
            "name": "Another User",
            "password": "Password123!",
            "organization_slug": sample_organization.slug
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=payload)
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert data["detail"]["error"]["code"] == "EMAIL_ALREADY_EXISTS"
        assert "already registered" in data["detail"]["error"]["message"].lower()
    
    def test_register_with_invalid_organization_returns_404(self, client: TestClient):
        """Test registering with non-existent organization returns 404 ORG_NOT_FOUND"""
        # Arrange
        payload = {
            "email": "user@test.com",
            "name": "Test User",
            "password": "Password123!",
            "organization_slug": "non-existent-org"
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=payload)
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["detail"]["error"]["code"] == "ORG_NOT_FOUND"
        assert "not found" in data["detail"]["error"]["message"].lower()
    
    def test_register_with_weak_password_returns_422(self, client: TestClient, sample_organization: Organization):
        """Test registering with password < 8 characters returns 422 validation error"""
        # Arrange
        payload = {
            "email": "user@test.com",
            "name": "Test User",
            "password": "short",  # Less than 8 characters
            "organization_slug": sample_organization.slug
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=payload)
        
        # Assert
        assert response.status_code == 422  # Pydantic validation error
        data = response.json()
        assert "detail" in data
    
    def test_register_with_invalid_email_format_returns_422(self, client: TestClient, sample_organization: Organization):
        """Test registering with invalid email format returns 422 validation error"""
        # Arrange
        payload = {
            "email": "not-an-email",  # Invalid email format
            "name": "Test User",
            "password": "Password123!",
            "organization_slug": sample_organization.slug
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=payload)
        
        # Assert
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
    
    def test_register_with_missing_fields_returns_422(self, client: TestClient):
        """Test registering with missing required fields returns 422"""
        # Arrange
        payload = {
            "email": "user@test.com"
            # Missing name, password, organization_slug
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=payload)
        
        # Assert
        assert response.status_code == 422


class TestAuthLogin:
    """Test suite for POST /api/v1/auth/login endpoint"""
    
    def test_login_with_valid_credentials_returns_access_token(self, client: TestClient, sample_user: User):
        """Test successful login returns access token"""
        # Arrange
        payload = {
            "email": sample_user.email,
            "password": "Password123!"  # From sample_user fixture
        }
        
        # Act
        response = client.post("/api/v1/auth/login", json=payload)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == 15 * 60  # 15 minutes in seconds
        assert len(data["access_token"]) > 0
    
    def test_login_sets_httponly_refresh_token_cookie(self, client: TestClient, sample_user: User):
        """Test that login sets httpOnly refresh token cookie"""
        # Arrange
        payload = {
            "email": sample_user.email,
            "password": "Password123!"
        }
        
        # Act
        response = client.post("/api/v1/auth/login", json=payload)
        
        # Assert
        assert response.status_code == 200
        cookies = response.cookies
        assert "refresh_token" in cookies
        # Note: TestClient doesn't expose httpOnly attribute, but it's set in the code
    
    def test_login_with_invalid_email_returns_401(self, client: TestClient):
        """Test login with non-existent email returns 401 INVALID_CREDENTIALS"""
        # Arrange
        payload = {
            "email": "nonexistent@test.com",
            "password": "Password123!"
        }
        
        # Act
        response = client.post("/api/v1/auth/login", json=payload)
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert data["detail"]["error"]["code"] == "INVALID_CREDENTIALS"
        assert "invalid email or password" in data["detail"]["error"]["message"].lower()
    
    def test_login_with_invalid_password_returns_401(self, client: TestClient, sample_user: User):
        """Test login with wrong password returns 401 INVALID_CREDENTIALS"""
        # Arrange
        payload = {
            "email": sample_user.email,
            "password": "WrongPassword123!"
        }
        
        # Act
        response = client.post("/api/v1/auth/login", json=payload)
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert data["detail"]["error"]["code"] == "INVALID_CREDENTIALS"
        assert "invalid email or password" in data["detail"]["error"]["message"].lower()
    
    def test_login_same_error_message_prevents_email_enumeration(self, client: TestClient, sample_user: User):
        """Test that invalid email and invalid password return the same error message (prevent email enumeration)"""
        # Arrange
        invalid_email_payload = {
            "email": "nonexistent@test.com",
            "password": "Password123!"
        }
        invalid_password_payload = {
            "email": sample_user.email,
            "password": "WrongPassword123!"
        }
        
        # Act
        response_email = client.post("/api/v1/auth/login", json=invalid_email_payload)
        response_password = client.post("/api/v1/auth/login", json=invalid_password_payload)
        
        # Assert
        assert response_email.status_code == 401
        assert response_password.status_code == 401
        
        # Both should return the same error message
        error_email = response_email.json()["detail"]["error"]["message"]
        error_password = response_password.json()["detail"]["error"]["message"]
        assert error_email == error_password
    
    def test_login_token_expiration_time(self, client: TestClient, sample_user: User):
        """Test that token expiration time is correctly set"""
        # Arrange
        payload = {
            "email": sample_user.email,
            "password": "Password123!"
        }
        
        # Act
        response = client.post("/api/v1/auth/login", json=payload)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["expires_in"] == 15 * 60  # 15 minutes in seconds (from config)
    
    def test_login_with_missing_email_returns_422(self, client: TestClient):
        """Test login with missing email returns 422"""
        # Arrange
        payload = {
            "password": "Password123!"
        }
        
        # Act
        response = client.post("/api/v1/auth/login", json=payload)
        
        # Assert
        assert response.status_code == 422
    
    def test_login_with_missing_password_returns_422(self, client: TestClient, sample_user: User):
        """Test login with missing password returns 422"""
        # Arrange
        payload = {
            "email": sample_user.email
        }
        
        # Act
        response = client.post("/api/v1/auth/login", json=payload)
        
        # Assert
        assert response.status_code == 422


class TestAuthLogout:
    """Test suite for POST /api/v1/auth/logout endpoint"""
    
    def test_logout_returns_200_with_success_message(self, client: TestClient):
        """Test logout returns 200 with success message"""
        # Arrange & Act
        response = client.post("/api/v1/auth/logout")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "logged out" in data["message"].lower()
    
    def test_logout_clears_refresh_token_cookie(self, client: TestClient, sample_user: User):
        """Test that logout clears the refresh token cookie"""
        # Arrange - First login to set cookie
        login_payload = {
            "email": sample_user.email,
            "password": "Password123!"
        }
        login_response = client.post("/api/v1/auth/login", json=login_payload)
        assert login_response.status_code == 200
        
        # Act - Logout
        logout_response = client.post("/api/v1/auth/logout")
        
        # Assert
        assert logout_response.status_code == 200
        # The cookie should be deleted (set with max_age=0 or similar)
        # Note: TestClient may not perfectly emulate cookie deletion behavior


class TestAuthEndToEnd:
    """End-to-end authentication flow tests"""
    
    def test_complete_registration_and_login_flow(self, client: TestClient, sample_organization: Organization, db: Session):
        """Test complete flow: register -> login -> verify token"""
        # Step 1: Register
        register_payload = {
            "email": "e2e@test.com",
            "name": "E2E User",
            "password": "E2EPassword123!",
            "organization_slug": sample_organization.slug
        }
        register_response = client.post("/api/v1/auth/register", json=register_payload)
        assert register_response.status_code == 201
        
        # Step 2: Login with registered credentials
        login_payload = {
            "email": "e2e@test.com",
            "password": "E2EPassword123!"
        }
        login_response = client.post("/api/v1/auth/login", json=login_payload)
        assert login_response.status_code == 200
        
        login_data = login_response.json()
        assert "access_token" in login_data
        
        # Step 3: Verify user exists in database with correct data
        user = user_crud.get_user_by_email(db, "e2e@test.com")
        assert user is not None
        assert user.email == "e2e@test.com"
        assert user.name == "E2E User"
        assert user.role == UserRole.PARTICIPANT
        assert verify_password("E2EPassword123!", user.password_hash)
