"""
Test configuration and fixtures for the automated marketing agent.
"""
import os
import pytest
import asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.core.config import get_settings
from app.core.database import get_db, Base
from app.models.user import User
from app.models.content import Client

# Test database URL
TEST_DATABASE_URL = "sqlite:///./test_marketing_agent.db"

# Create test engine
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    # Create all tables
    Base.metadata.create_all(bind=test_engine)
    
    # Create session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override."""
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client."""
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "testpassword123"
    }


@pytest.fixture
def test_client_data():
    """Sample client data for testing."""
    return {
        "name": "Test Company",
        "description": "A test company for marketing",
        "industry": "Technology",
        "brand_voice": "Professional and friendly"
    }


@pytest.fixture
def test_content_data():
    """Sample content data for testing."""
    return {
        "title": "Test Content",
        "content": "This is test content for social media posting.",
        "content_type": "text",
        "platform": "instagram",
        "hashtags": ["#test", "#marketing"]
    }


@pytest.fixture
def authenticated_headers(client, test_user_data):
    """Get authentication headers for API requests."""
    # First create a user
    client.post("/api/v1/auth/register", json=test_user_data)
    
    # Then login to get token
    login_data = {
        "username": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response."""
    return {
        "choices": [
            {
                "message": {
                    "content": "This is a generated social media post about your amazing product! #awesome #marketing"
                }
            }
        ]
    }


@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup test environment variables."""
    os.environ["ENVIRONMENT"] = "test"
    os.environ["SECRET_KEY"] = "test-secret-key"
    os.environ["DATABASE_URL"] = TEST_DATABASE_URL
    os.environ["OPENAI_API_KEY"] = "sk-test-key"
    yield
    # Cleanup is handled automatically when fixture goes out of scope
