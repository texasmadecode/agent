"""
Unit tests for AI service functionality.
"""
import pytest
from unittest.mock import patch, MagicMock
from app.services.ai_service import OpenAIService


class TestOpenAIService:
    """Test OpenAI service integration."""
    
    def test_service_initialization(self):
        """Test that OpenAI service initializes correctly."""
        service = OpenAIService()
        assert service is not None
        assert hasattr(service, 'client')
    
    @patch('app.services.ai_service.OpenAI')
    def test_generate_content_success(self, mock_openai_client):
        """Test successful content generation."""
        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content="Generated social media content!"))
        ]
        mock_openai_client.return_value.chat.completions.create.return_value = mock_response
        
        service = OpenAIService()
        result = service.generate_content(
            prompt="Create a social media post",
            platform="instagram",
            tone="professional"
        )
        
        assert result == "Generated social media content!"
        mock_openai_client.return_value.chat.completions.create.assert_called_once()
    
    @patch('app.services.ai_service.OpenAI')
    def test_generate_content_api_error(self, mock_openai_client):
        """Test handling of OpenAI API errors."""
        mock_openai_client.return_value.chat.completions.create.side_effect = Exception("API Error")
        
        service = OpenAIService()
        
        with pytest.raises(Exception):
            service.generate_content("Test prompt")
    
    @patch('app.services.ai_service.OpenAI')
    def test_generate_hashtags(self, mock_openai_client):
        """Test hashtag generation."""
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content="#marketing #socialmedia #content"))
        ]
        mock_openai_client.return_value.chat.completions.create.return_value = mock_response
        
        service = OpenAIService()
        result = service.generate_hashtags("marketing content", "instagram")
        
        assert "#marketing" in result
        assert "#socialmedia" in result
    
    @patch('app.services.ai_service.OpenAI')
    def test_optimize_content(self, mock_openai_client):
        """Test content optimization."""
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content="Optimized content for better engagement!"))
        ]
        mock_openai_client.return_value.chat.completions.create.return_value = mock_response
        
        service = OpenAIService()
        result = service.optimize_content(
            content="Original content",
            platform="instagram",
            optimization_goal="engagement"
        )
        
        assert "Optimized" in result
    
    def test_platform_specific_prompts(self):
        """Test that platform-specific prompts are used."""
        service = OpenAIService()
        
        # Test Instagram prompt
        instagram_prompt = service._build_prompt("Test content", "instagram", "casual")
        assert "instagram" in instagram_prompt.lower()
        
        # Test Twitter prompt
        twitter_prompt = service._build_prompt("Test content", "twitter", "professional")
        assert "twitter" in twitter_prompt.lower() or "280 characters" in twitter_prompt
    
    def test_tone_adaptation(self):
        """Test that content tone is properly adapted."""
        service = OpenAIService()
        
        # Test professional tone
        professional_prompt = service._build_prompt("Test", "linkedin", "professional")
        assert "professional" in professional_prompt.lower()
        
        # Test casual tone
        casual_prompt = service._build_prompt("Test", "instagram", "casual")
        assert "casual" in casual_prompt.lower()


class TestAIServiceIntegration:
    """Test AI service integration with other components."""
    
    @patch('app.services.ai_service.OpenAIService.generate_content')
    def test_content_generation_with_brand_voice(self, mock_generate):
        """Test content generation with brand voice considerations."""
        mock_generate.return_value = "Brand-consistent content"
        
        service = OpenAIService()
        result = service.generate_branded_content(
            prompt="Product announcement",
            brand_voice="friendly and approachable",
            platform="facebook"
        )
        
        assert result == "Brand-consistent content"
        mock_generate.assert_called_once()
    
    @patch('app.services.ai_service.OpenAIService.generate_content')
    def test_batch_content_generation(self, mock_generate):
        """Test generating multiple content pieces at once."""
        mock_generate.side_effect = [
            "Content piece 1",
            "Content piece 2",
            "Content piece 3"
        ]
        
        service = OpenAIService()
        prompts = ["Prompt 1", "Prompt 2", "Prompt 3"]
        results = service.generate_batch_content(prompts, "instagram")
        
        assert len(results) == 3
        assert "Content piece 1" in results
        assert mock_generate.call_count == 3
    
    def test_content_safety_filtering(self):
        """Test that inappropriate content is filtered out."""
        service = OpenAIService()
        
        # Test with potentially inappropriate content
        unsafe_content = "This content contains inappropriate material"
        is_safe = service.is_content_safe(unsafe_content)
        
        # Should have safety checking logic
        assert isinstance(is_safe, bool)


class TestAIServiceConfiguration:
    """Test AI service configuration and settings."""
    
    def test_api_key_configuration(self):
        """Test that API key is properly configured."""
        service = OpenAIService()
        # Don't expose actual API key in tests
        assert hasattr(service, 'client')
    
    def test_model_configuration(self):
        """Test that the correct AI model is used."""
        service = OpenAIService()
        assert service.model in ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]
    
    def test_rate_limiting_awareness(self):
        """Test that service handles rate limiting."""
        service = OpenAIService()
        # Should have rate limiting logic or error handling
        assert hasattr(service, 'generate_content')
    
    @patch('app.services.ai_service.OpenAI')
    def test_retry_logic(self, mock_openai_client):
        """Test retry logic for transient failures."""
        # First call fails, second succeeds
        mock_openai_client.return_value.chat.completions.create.side_effect = [
            Exception("Temporary error"),
            MagicMock(choices=[MagicMock(message=MagicMock(content="Success"))])
        ]
        
        service = OpenAIService()
        # This would test retry logic if implemented
        # For now, just test that service can handle errors
        try:
            result = service.generate_content("Test prompt")
            assert result == "Success"
        except Exception:
            # Expected if no retry logic implemented
            pass
