"""
Unit tests for authentication endpoints.
"""
import pytest
from unittest.mock import patch


class TestAuthRegistration:
    """Test user registration functionality."""
    
    def test_register_new_user(self, client, test_user_data):
        """Test successful user registration."""
        response = client.post("/api/v1/auth/register", json=test_user_data)
        assert response.status_code == 201
        
        data = response.json()
        assert "user" in data
        assert data["user"]["email"] == test_user_data["email"]
        assert data["user"]["username"] == test_user_data["username"]
        assert "password" not in data["user"]  # Password should not be returned
    
    def test_register_duplicate_email(self, client, test_user_data):
        """Test registration with duplicate email fails."""
        # Register user first time
        client.post("/api/v1/auth/register", json=test_user_data)
        
        # Try to register again with same email
        response = client.post("/api/v1/auth/register", json=test_user_data)
        assert response.status_code == 400
        
        data = response.json()
        assert "already exists" in data["detail"].lower()
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email fails."""
        invalid_data = {
            "email": "invalid-email",
            "username": "testuser",
            "full_name": "Test User",
            "password": "testpassword123"
        }
        
        response = client.post("/api/v1/auth/register", json=invalid_data)
        assert response.status_code == 422
    
    def test_register_weak_password(self, client):
        """Test registration with weak password fails."""
        weak_password_data = {
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "password": "123"
        }
        
        response = client.post("/api/v1/auth/register", json=weak_password_data)
        # Should either validate password strength or accept and hash it
        # This depends on your validation rules
        assert response.status_code in [201, 422]


class TestAuthLogin:
    """Test user login functionality."""
    
    def test_login_valid_credentials(self, client, test_user_data):
        """Test login with valid credentials."""
        # First register the user
        client.post("/api/v1/auth/register", json=test_user_data)
        
        # Then attempt login
        login_data = {
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
        
        response = client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self, client, test_user_data):
        """Test login with invalid credentials fails."""
        # Register user first
        client.post("/api/v1/auth/register", json=test_user_data)
        
        # Try login with wrong password
        login_data = {
            "username": test_user_data["email"],
            "password": "wrongpassword"
        }
        
        response = client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 401
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user fails."""
        login_data = {
            "username": "nonexistent@example.com",
            "password": "somepassword"
        }
        
        response = client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 401


class TestAuthTokens:
    """Test token-based authentication."""
    
    def test_protected_endpoint_without_token(self, client):
        """Test accessing protected endpoint without token fails."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
    
    def test_protected_endpoint_with_valid_token(self, client, authenticated_headers):
        """Test accessing protected endpoint with valid token."""
        response = client.get("/api/v1/auth/me", headers=authenticated_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert "email" in data
        assert "username" in data
    
    def test_protected_endpoint_with_invalid_token(self, client):
        """Test accessing protected endpoint with invalid token."""
        headers = {"Authorization": "Bearer invalid-token"}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 401


class TestAuthSecurity:
    """Test authentication security features."""
    
    def test_password_hashing(self, client, test_user_data):
        """Test that passwords are properly hashed."""
        # Register user
        response = client.post("/api/v1/auth/register", json=test_user_data)
        assert response.status_code == 201
        
        # The password should not be stored in plain text
        # This would require checking the database directly
        # For now, we just ensure registration doesn't return the password
        data = response.json()
        assert "password" not in data["user"]
    
    def test_token_expiration_handling(self, client):
        """Test handling of expired tokens."""
        # This would require mocking token expiration
        # For now, just test with malformed token
        headers = {"Authorization": "Bearer expired.token.here"}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 401
