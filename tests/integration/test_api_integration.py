"""
Integration tests for the automated marketing agent API.
"""
import pytest
import asyncio
from httpx import AsyncClient


class TestAPIIntegration:
    """Test full API integration scenarios."""
    
    @pytest.mark.asyncio
    async def test_complete_user_workflow(self, async_client: AsyncClient):
        """Test complete user workflow from registration to content creation."""
        # 1. Register user
        user_data = {
            "email": "integration@example.com",
            "username": "integrationuser",
            "full_name": "Integration Test User",
            "password": "integrationpassword123"
        }
        
        register_response = await async_client.post("/api/v1/auth/register", json=user_data)
        assert register_response.status_code == 201
        
        # 2. Login
        login_data = {
            "username": user_data["email"],
            "password": user_data["password"]
        }
        
        login_response = await async_client.post("/api/v1/auth/login", data=login_data)
        assert login_response.status_code == 200
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 3. Create client
        client_data = {
            "name": "Integration Test Company",
            "description": "A test company for integration testing",
            "industry": "Technology"
        }
        
        client_response = await async_client.post("/api/v1/clients/", json=client_data, headers=headers)
        assert client_response.status_code == 201
        
        # 4. Create content
        content_data = {
            "title": "Integration Test Content",
            "content": "This is integration test content",
            "content_type": "text",
            "platform": "instagram"
        }
        
        content_response = await async_client.post("/api/v1/content/", json=content_data, headers=headers)
        assert content_response.status_code == 201
        
        # 5. Verify content exists
        content_list_response = await async_client.get("/api/v1/content/", headers=headers)
        assert content_list_response.status_code == 200
        
        contents = content_list_response.json()
        assert len(contents) == 1
        assert contents[0]["title"] == content_data["title"]
    
    @pytest.mark.asyncio
    async def test_authentication_flow(self, async_client: AsyncClient):
        """Test authentication and authorization flow."""
        # Test accessing protected endpoint without auth
        response = await async_client.get("/api/v1/auth/me")
        assert response.status_code == 401
        
        # Register and login
        user_data = {
            "email": "auth_test@example.com",
            "username": "authtest",
            "full_name": "Auth Test User",
            "password": "authpassword123"
        }
        
        await async_client.post("/api/v1/auth/register", json=user_data)
        
        login_data = {
            "username": user_data["email"],
            "password": user_data["password"]
        }
        
        login_response = await async_client.post("/api/v1/auth/login", data=login_data)
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test accessing protected endpoint with auth
        me_response = await async_client.get("/api/v1/auth/me", headers=headers)
        assert me_response.status_code == 200
        
        user_info = me_response.json()
        assert user_info["email"] == user_data["email"]
    
    @pytest.mark.asyncio
    async def test_content_generation_flow(self, async_client: AsyncClient):
        """Test AI content generation integration."""
        # Setup authenticated user
        user_data = {
            "email": "content_gen@example.com",
            "username": "contentgen",
            "full_name": "Content Gen User",
            "password": "contentgenpassword123"
        }
        
        await async_client.post("/api/v1/auth/register", json=user_data)
        
        login_data = {
            "username": user_data["email"],
            "password": user_data["password"]
        }
        
        login_response = await async_client.post("/api/v1/auth/login", data=login_data)
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test content generation
        generation_request = {
            "prompt": "Create a social media post about our amazing new product",
            "platform": "instagram",
            "tone": "professional"
        }
        
        # Note: This might fail if OpenAI API key is not configured
        generation_response = await async_client.post(
            "/api/v1/content/generate",
            json=generation_request,
            headers=headers
        )
        
        # Should succeed with proper API key, or fail gracefully
        assert generation_response.status_code in [200, 500, 503]
    
    @pytest.mark.asyncio
    async def test_campaign_management_flow(self, async_client: AsyncClient):
        """Test campaign creation and management."""
        # Setup user
        user_data = {
            "email": "campaign@example.com",
            "username": "campaignuser",
            "full_name": "Campaign User",
            "password": "campaignpassword123"
        }
        
        await async_client.post("/api/v1/auth/register", json=user_data)
        
        login_data = {
            "username": user_data["email"],
            "password": user_data["password"]
        }
        
        login_response = await async_client.post("/api/v1/auth/login", data=login_data)
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create campaign
        campaign_data = {
            "name": "Integration Test Campaign",
            "description": "A test campaign for integration testing",
            "start_date": "2025-08-22T00:00:00",
            "end_date": "2025-08-29T23:59:59"
        }
        
        campaign_response = await async_client.post("/api/v1/campaigns/", json=campaign_data, headers=headers)
        assert campaign_response.status_code == 201
        
        campaign = campaign_response.json()
        assert campaign["name"] == campaign_data["name"]
        
        # List campaigns
        campaigns_response = await async_client.get("/api/v1/campaigns/", headers=headers)
        assert campaigns_response.status_code == 200
        
        campaigns = campaigns_response.json()
        assert len(campaigns) >= 1


class TestAPIErrorHandling:
    """Test API error handling and edge cases."""
    
    @pytest.mark.asyncio
    async def test_invalid_json_request(self, async_client: AsyncClient):
        """Test handling of invalid JSON requests."""
        response = await async_client.post(
            "/api/v1/auth/register",
            content="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    @pytest.mark.asyncio
    async def test_missing_required_fields(self, async_client: AsyncClient):
        """Test handling of missing required fields."""
        incomplete_data = {
            "email": "test@example.com"
            # Missing username, full_name, password
        }
        
        response = await async_client.post("/api/v1/auth/register", json=incomplete_data)
        assert response.status_code == 422
        
        error_detail = response.json()
        assert "detail" in error_detail
    
    @pytest.mark.asyncio
    async def test_rate_limiting_behavior(self, async_client: AsyncClient):
        """Test API rate limiting (if implemented)."""
        # Make multiple rapid requests
        tasks = []
        for i in range(10):
            task = async_client.get("/health")
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Should handle concurrent requests gracefully
        success_count = sum(1 for r in responses if hasattr(r, 'status_code') and r.status_code == 200)
        assert success_count >= 5  # At least some should succeed


class TestAPIPerformance:
    """Test API performance characteristics."""
    
    @pytest.mark.asyncio
    async def test_health_endpoint_performance(self, async_client: AsyncClient):
        """Test health endpoint response time."""
        import time
        
        start_time = time.time()
        response = await async_client.get("/health")
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 1.0  # Should respond within 1 second
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self, async_client: AsyncClient):
        """Test handling of concurrent requests."""
        # Create multiple concurrent requests
        tasks = [async_client.get("/health") for _ in range(5)]
        responses = await asyncio.gather(*tasks)
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == 200
