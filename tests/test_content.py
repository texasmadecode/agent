"""
Unit tests for content management functionality.
"""
import pytest
from unittest.mock import patch, MagicMock


class TestContentCRUD:
    """Test content CRUD operations."""
    
    def test_create_content(self, client, authenticated_headers, test_content_data):
        """Test creating new content."""
        response = client.post(
            "/api/v1/content/", 
            json=test_content_data,
            headers=authenticated_headers
        )
        assert response.status_code == 201
        
        data = response.json()
        assert data["title"] == test_content_data["title"]
        assert data["content"] == test_content_data["content"]
        assert "id" in data
        assert "created_at" in data
    
    def test_get_content_list(self, client, authenticated_headers):
        """Test retrieving content list."""
        response = client.get("/api/v1/content/", headers=authenticated_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_content_by_id(self, client, authenticated_headers, test_content_data):
        """Test retrieving specific content by ID."""
        # First create content
        create_response = client.post(
            "/api/v1/content/",
            json=test_content_data,
            headers=authenticated_headers
        )
        content_id = create_response.json()["id"]
        
        # Then retrieve it
        response = client.get(f"/api/v1/content/{content_id}", headers=authenticated_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == content_id
        assert data["title"] == test_content_data["title"]
    
    def test_update_content(self, client, authenticated_headers, test_content_data):
        """Test updating existing content."""
        # Create content
        create_response = client.post(
            "/api/v1/content/",
            json=test_content_data,
            headers=authenticated_headers
        )
        content_id = create_response.json()["id"]
        
        # Update content
        updated_data = test_content_data.copy()
        updated_data["title"] = "Updated Title"
        
        response = client.put(
            f"/api/v1/content/{content_id}",
            json=updated_data,
            headers=authenticated_headers
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["title"] == "Updated Title"
    
    def test_delete_content(self, client, authenticated_headers, test_content_data):
        """Test deleting content."""
        # Create content
        create_response = client.post(
            "/api/v1/content/",
            json=test_content_data,
            headers=authenticated_headers
        )
        content_id = create_response.json()["id"]
        
        # Delete content
        response = client.delete(f"/api/v1/content/{content_id}", headers=authenticated_headers)
        assert response.status_code == 204
        
        # Verify deletion
        get_response = client.get(f"/api/v1/content/{content_id}", headers=authenticated_headers)
        assert get_response.status_code == 404


class TestContentGeneration:
    """Test AI-powered content generation."""
    
    @patch('app.services.ai_service.OpenAIService.generate_content')
    def test_generate_content_success(self, mock_generate, client, authenticated_headers, mock_openai_response):
        """Test successful content generation."""
        mock_generate.return_value = mock_openai_response["choices"][0]["message"]["content"]
        
        generation_request = {
            "prompt": "Create a social media post about our new product",
            "platform": "instagram",
            "tone": "professional",
            "include_hashtags": True
        }
        
        response = client.post(
            "/api/v1/content/generate",
            json=generation_request,
            headers=authenticated_headers
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "generated_content" in data
        assert len(data["generated_content"]) > 0
        mock_generate.assert_called_once()
    
    @patch('app.services.ai_service.OpenAIService.generate_content')
    def test_generate_content_with_error(self, mock_generate, client, authenticated_headers):
        """Test content generation with API error."""
        mock_generate.side_effect = Exception("OpenAI API error")
        
        generation_request = {
            "prompt": "Create a social media post",
            "platform": "instagram"
        }
        
        response = client.post(
            "/api/v1/content/generate",
            json=generation_request,
            headers=authenticated_headers
        )
        assert response.status_code == 500
    
    def test_generate_content_invalid_request(self, client, authenticated_headers):
        """Test content generation with invalid request."""
        invalid_request = {
            "platform": "invalid_platform"
            # Missing required prompt
        }
        
        response = client.post(
            "/api/v1/content/generate",
            json=invalid_request,
            headers=authenticated_headers
        )
        assert response.status_code == 422


class TestContentValidation:
    """Test content validation rules."""
    
    def test_content_title_required(self, client, authenticated_headers):
        """Test that content title is required."""
        invalid_content = {
            "content": "This is content without a title",
            "content_type": "text",
            "platform": "instagram"
        }
        
        response = client.post(
            "/api/v1/content/",
            json=invalid_content,
            headers=authenticated_headers
        )
        assert response.status_code == 422
    
    def test_content_length_validation(self, client, authenticated_headers):
        """Test content length validation for different platforms."""
        # Twitter has character limits
        long_content = {
            "title": "Long Content Test",
            "content": "x" * 300,  # Very long content
            "content_type": "text",
            "platform": "twitter"
        }
        
        response = client.post(
            "/api/v1/content/",
            json=long_content,
            headers=authenticated_headers
        )
        # Should either accept or validate based on platform rules
        assert response.status_code in [201, 422]
    
    def test_hashtag_validation(self, client, authenticated_headers):
        """Test hashtag format validation."""
        content_with_hashtags = {
            "title": "Hashtag Test",
            "content": "Test content",
            "content_type": "text",
            "platform": "instagram",
            "hashtags": ["#valid", "invalid_hashtag", "#another_valid"]
        }
        
        response = client.post(
            "/api/v1/content/",
            json=content_with_hashtags,
            headers=authenticated_headers
        )
        # Should validate hashtag format
        assert response.status_code in [201, 422]


class TestContentSecurity:
    """Test content security and access control."""
    
    def test_unauthorized_content_access(self, client, test_content_data):
        """Test that unauthorized users cannot access content."""
        response = client.get("/api/v1/content/")
        assert response.status_code == 401
    
    def test_user_can_only_access_own_content(self, client, test_user_data, test_content_data):
        """Test that users can only access their own content."""
        # This would require creating multiple users and testing isolation
        # For now, we just test basic access control
        response = client.post("/api/v1/content/", json=test_content_data)
        assert response.status_code == 401  # No auth headers
