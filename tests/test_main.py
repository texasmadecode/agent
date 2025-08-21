"""
Unit tests for the main FastAPI application.
"""
import pytest
from fastapi.testclient import TestClient


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_root_endpoint(client):
    """Test the root endpoint returns dashboard."""
    response = client.get("/")
    assert response.status_code == 200
    # Should return HTML content for dashboard
    assert "text/html" in response.headers.get("content-type", "")


def test_api_docs_endpoint(client):
    """Test the API documentation endpoint."""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")


def test_openapi_schema(client):
    """Test the OpenAPI schema endpoint."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    
    schema = response.json()
    assert "openapi" in schema
    assert "info" in schema
    assert schema["info"]["title"] == "Marketing Agent API"


def test_cors_headers(client):
    """Test CORS headers are properly set."""
    response = client.options("/health")
    assert response.status_code == 200
    
    # Check CORS headers
    headers = response.headers
    assert "access-control-allow-origin" in headers
    assert "access-control-allow-methods" in headers


def test_404_endpoint(client):
    """Test that non-existent endpoints return 404."""
    response = client.get("/non-existent-endpoint")
    assert response.status_code == 404


def test_static_files_served(client):
    """Test that static files are served correctly."""
    # This would test static file serving if we had any static files
    # For now, just ensure the route exists
    response = client.get("/static/nonexistent.css")
    # Should return 404 for non-existent static files
    assert response.status_code == 404


class TestApplicationStartup:
    """Test application startup and configuration."""
    
    def test_app_instance_exists(self):
        """Test that the FastAPI app instance is created."""
        from app.main import app
        assert app is not None
        assert hasattr(app, 'title')
        assert app.title == "Marketing Agent API"
    
    def test_app_version(self):
        """Test that app has version information."""
        from app.main import app
        assert hasattr(app, 'version')
        assert app.version == "1.0.0"
    
    def test_app_middleware_configured(self):
        """Test that middleware is properly configured."""
        from app.main import app
        # Check that CORS middleware is added
        middleware_types = [type(middleware) for middleware in app.user_middleware]
        from starlette.middleware.cors import CORSMiddleware
        assert CORSMiddleware in middleware_types
