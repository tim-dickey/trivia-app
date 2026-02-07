"""
Tests for Security Headers Middleware

Validates that all security headers are correctly added to HTTP responses
and that the middleware doesn't break existing application functionality.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.models.user import User
from backend.models.organization import Organization


class TestSecurityHeadersMiddleware:
    """Test suite for security headers middleware"""
    
    def test_health_endpoint_has_all_security_headers(self, client: TestClient):
        """Test that health check endpoint includes all security headers"""
        # Act
        response = client.get("/health")
        
        # Assert
        assert response.status_code == 200
        
        # Check all security headers are present
        assert "Strict-Transport-Security" in response.headers
        assert "Content-Security-Policy" in response.headers
        assert "X-Frame-Options" in response.headers
        assert "X-Content-Type-Options" in response.headers
        assert "X-XSS-Protection" in response.headers
    
    def test_hsts_header_has_correct_value(self, client: TestClient):
        """Test HSTS header enforces HTTPS with 1 year max-age"""
        # Act
        response = client.get("/health")
        
        # Assert
        hsts_header = response.headers.get("Strict-Transport-Security")
        assert hsts_header == "max-age=31536000; includeSubDomains"
        
        # Verify it includes required directives
        assert "max-age=31536000" in hsts_header  # 1 year in seconds
        assert "includeSubDomains" in hsts_header
    
    def test_csp_header_has_correct_value(self, client: TestClient):
        """Test CSP header restricts resource loading appropriately"""
        # Act
        response = client.get("/health")
        
        # Assert
        csp_header = response.headers.get("Content-Security-Policy")
        
        # Verify all required CSP directives are present
        assert "default-src 'self'" in csp_header
        assert "script-src 'self' 'unsafe-inline'" in csp_header
        assert "style-src 'self' 'unsafe-inline'" in csp_header
        assert "img-src 'self' data: https:" in csp_header
        assert "font-src 'self' data:" in csp_header
        assert "connect-src 'self' ws: wss:" in csp_header
    
    def test_x_frame_options_prevents_clickjacking(self, client: TestClient):
        """Test X-Frame-Options header prevents framing"""
        # Act
        response = client.get("/health")
        
        # Assert
        assert response.headers.get("X-Frame-Options") == "DENY"
    
    def test_x_content_type_options_prevents_mime_sniffing(self, client: TestClient):
        """Test X-Content-Type-Options prevents MIME sniffing"""
        # Act
        response = client.get("/health")
        
        # Assert
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
    
    def test_x_xss_protection_header_is_present(self, client: TestClient):
        """Test X-XSS-Protection header is present for legacy browsers"""
        # Act
        response = client.get("/health")
        
        # Assert
        assert response.headers.get("X-XSS-Protection") == "1; mode=block"
    
    def test_root_endpoint_has_security_headers(self, client: TestClient):
        """Test that root endpoint also has security headers"""
        # Act
        response = client.get("/")
        
        # Assert
        assert response.status_code == 200
        assert "Strict-Transport-Security" in response.headers
        assert "Content-Security-Policy" in response.headers
        assert "X-Frame-Options" in response.headers
    
    def test_api_endpoints_have_security_headers(
        self, 
        client: TestClient, 
        sample_organization: Organization
    ):
        """Test that API endpoints have security headers"""
        # Arrange
        payload = {
            "email": "sectest@test.com",
            "name": "Security Test User",
            "password": "SecurePass123!",
            "organization_slug": sample_organization.slug
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=payload)
        
        # Assert
        assert response.status_code == 201
        assert "Strict-Transport-Security" in response.headers
        assert "Content-Security-Policy" in response.headers
        assert "X-Frame-Options" in response.headers
        assert "X-Content-Type-Options" in response.headers
        assert "X-XSS-Protection" in response.headers
    
    def test_error_responses_have_security_headers(self, client: TestClient):
        """Test that error responses also include security headers"""
        # Act - Request non-existent endpoint
        response = client.get("/api/v1/nonexistent")
        
        # Assert
        assert response.status_code == 404
        assert "Strict-Transport-Security" in response.headers
        assert "Content-Security-Policy" in response.headers
        assert "X-Frame-Options" in response.headers
    
    def test_authenticated_endpoints_have_security_headers(
        self, 
        client: TestClient,
        auth_headers: dict
    ):
        """Test that authenticated endpoints include security headers"""
        # Act - Try to access authenticated endpoint (will fail but should have headers)
        response = client.get("/api/v1/users/me", headers=auth_headers)
        
        # Assert - Response should have security headers regardless of success
        assert "Strict-Transport-Security" in response.headers
        assert "Content-Security-Policy" in response.headers
    
    def test_security_headers_do_not_break_json_responses(
        self,
        client: TestClient,
        sample_organization: Organization
    ):
        """Test that security headers don't interfere with JSON response parsing"""
        # Arrange
        payload = {
            "email": "jsontest@test.com",
            "name": "JSON Test User",
            "password": "JsonPass123!",
            "organization_slug": sample_organization.slug
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=payload)
        
        # Assert - Response should be valid JSON with security headers
        assert response.status_code == 201
        data = response.json()  # Should parse without error
        assert data["email"] == "jsontest@test.com"
        assert "Strict-Transport-Security" in response.headers
    
    def test_all_security_headers_present_together(self, client: TestClient):
        """Test that all 5 security headers are present in every response"""
        # Act
        response = client.get("/health")
        
        # Assert - Count security headers
        security_headers = [
            "Strict-Transport-Security",
            "Content-Security-Policy", 
            "X-Frame-Options",
            "X-Content-Type-Options",
            "X-XSS-Protection"
        ]
        
        for header in security_headers:
            assert header in response.headers, f"Missing security header: {header}"
    
    def test_middleware_processes_requests_correctly(
        self,
        client: TestClient
    ):
        """Test that middleware doesn't break request processing"""
        # Act
        response = client.get("/health")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        # Verify security headers are added (count the 5 specific headers)
        security_headers = [
            "Strict-Transport-Security",
            "Content-Security-Policy", 
            "X-Frame-Options",
            "X-Content-Type-Options",
            "X-XSS-Protection"
        ]
        present_headers = [h for h in security_headers if h in response.headers]
        assert len(present_headers) == 5, f"Expected 5 security headers, found {len(present_headers)}"
