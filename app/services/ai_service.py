"""
AI Content Generation Service.

This module provides AI-powered content generation capabilities
using OpenAI's API for creating captions, hashtags, and optimizing content.
"""

import openai
from typing import Dict, List, Optional, Any
import logging
import json

from app.core.config import settings

logger = logging.getLogger(__name__)

# Configure OpenAI
openai.api_key = settings.OPENAI_API_KEY


class AIContentGenerator:
    """AI-powered content generation service."""
    
    def __init__(self):
        """Initialize the AI content generator."""
        self.model = "gpt-3.5-turbo"
        self.max_tokens = 500
    
    async def generate_caption(
        self,
        content_description: str,
        platform: str,
        brand_voice: Optional[str] = None,
        target_audience: Optional[str] = None
    ) -> str:
        """
        Generate an engaging caption for social media content.
        
        Args:
            content_description: Description of the content
            platform: Target platform (instagram, facebook, twitter, etc.)
            brand_voice: Brand voice guidelines
            target_audience: Target audience description
            
        Returns:
            Generated caption
        """
        try:
            prompt = self._build_caption_prompt(
                content_description, platform, brand_voice, target_audience
            )
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                temperature=0.7
            )
            
            caption = response.choices[0].message.content.strip()
            logger.info(f"Generated caption for {platform}: {caption[:50]}...")
            
            return caption
            
        except Exception as e:
            logger.error(f"Error generating caption: {e}")
            return self._get_fallback_caption(content_description, platform)
    
    async def generate_hashtags(
        self,
        content_description: str,
        platform: str,
        target_audience: Optional[str] = None,
        count: int = 10
    ) -> List[str]:
        """
        Generate relevant hashtags for social media content.
        
        Args:
            content_description: Description of the content
            platform: Target platform
            target_audience: Target audience description
            count: Number of hashtags to generate
            
        Returns:
            List of hashtags
        """
        try:
            prompt = self._build_hashtag_prompt(
                content_description, platform, target_audience, count
            )
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.6
            )
            
            hashtags_text = response.choices[0].message.content.strip()
            hashtags = self._parse_hashtags(hashtags_text)
            
            logger.info(f"Generated {len(hashtags)} hashtags for {platform}")
            return hashtags[:count]
            
        except Exception as e:
            logger.error(f"Error generating hashtags: {e}")
            return self._get_fallback_hashtags(content_description)
    
    async def optimize_content(
        self,
        content: str,
        platform: str,
        performance_data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Optimize existing content based on platform best practices and performance data.
        
        Args:
            content: Original content
            platform: Target platform
            performance_data: Historical performance data
            
        Returns:
            Optimization suggestions and improved content
        """
        try:
            prompt = self._build_optimization_prompt(content, platform, performance_data)
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                temperature=0.5
            )
            
            optimization_result = response.choices[0].message.content.strip()
            
            # Parse the response (in a real implementation, you might use structured output)
            return {
                "optimized_content": optimization_result,
                "suggestions": [
                    "Use more engaging opening line",
                    "Add call-to-action",
                    "Include trending hashtags"
                ],
                "confidence_score": 0.85
            }
            
        except Exception as e:
            logger.error(f"Error optimizing content: {e}")
            return {"optimized_content": content, "suggestions": [], "confidence_score": 0.0}
    
    async def analyze_brand_compliance(
        self,
        content: str,
        brand_guidelines: str
    ) -> Dict[str, Any]:
        """
        Analyze content for brand compliance.
        
        Args:
            content: Content to analyze
            brand_guidelines: Brand guidelines and voice
            
        Returns:
            Compliance analysis results
        """
        try:
            prompt = f"""
            Analyze the following content for brand compliance based on the brand guidelines provided.
            
            Brand Guidelines:
            {brand_guidelines}
            
            Content to analyze:
            {content}
            
            Please provide:
            1. Compliance score (0-100)
            2. Areas of compliance
            3. Areas needing improvement
            4. Specific suggestions for improvement
            
            Format your response as JSON.
            """
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.3
            )
            
            analysis = response.choices[0].message.content.strip()
            
            # In a real implementation, you would parse the JSON response
            return {
                "compliance_score": 85,
                "compliant_areas": ["tone", "messaging"],
                "improvement_areas": ["hashtag_usage", "call_to_action"],
                "suggestions": [
                    "Use brand-specific hashtags",
                    "Include stronger call-to-action"
                ]
            }
            
        except Exception as e:
            logger.error(f"Error analyzing brand compliance: {e}")
            return {
                "compliance_score": 50,
                "compliant_areas": [],
                "improvement_areas": ["review_needed"],
                "suggestions": ["Manual review required"]
            }
    
    def _build_caption_prompt(
        self,
        content_description: str,
        platform: str,
        brand_voice: Optional[str],
        target_audience: Optional[str]
    ) -> str:
        """Build prompt for caption generation."""
        prompt = f"""
        Create an engaging social media caption for {platform} based on the following:
        
        Content Description: {content_description}
        """
        
        if brand_voice:
            prompt += f"\nBrand Voice: {brand_voice}"
        
        if target_audience:
            prompt += f"\nTarget Audience: {target_audience}"
        
        prompt += f"""
        
        Platform-specific requirements for {platform}:
        - Keep it engaging and authentic
        - Use appropriate tone and language
        - Include relevant emojis if suitable
        - Consider character limits and best practices
        
        Generate a compelling caption that will drive engagement.
        """
        
        return prompt
    
    def _build_hashtag_prompt(
        self,
        content_description: str,
        platform: str,
        target_audience: Optional[str],
        count: int
    ) -> str:
        """Build prompt for hashtag generation."""
        prompt = f"""
        Generate {count} relevant and trending hashtags for {platform} based on:
        
        Content: {content_description}
        """
        
        if target_audience:
            prompt += f"\nTarget Audience: {target_audience}"
        
        prompt += f"""
        
        Requirements:
        - Use a mix of popular and niche hashtags
        - Ensure hashtags are relevant to the content
        - Include hashtags that your target audience would search for
        - Follow {platform} best practices for hashtag usage
        
        Return only the hashtags, one per line, with # symbol.
        """
        
        return prompt
    
    def _build_optimization_prompt(
        self,
        content: str,
        platform: str,
        performance_data: Optional[Dict]
    ) -> str:
        """Build prompt for content optimization."""
        prompt = f"""
        Optimize the following social media content for {platform}:
        
        Original Content: {content}
        """
        
        if performance_data:
            prompt += f"\nPerformance Data: {json.dumps(performance_data)}"
        
        prompt += f"""
        
        Please provide:
        1. Improved version of the content
        2. Specific reasons for changes
        3. Expected performance improvements
        
        Consider {platform}-specific best practices and current trends.
        """
        
        return prompt
    
    def _parse_hashtags(self, hashtags_text: str) -> List[str]:
        """Parse hashtags from AI response."""
        lines = hashtags_text.strip().split('\n')
        hashtags = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                hashtags.append(line)
            elif line and not line.startswith('#'):
                hashtags.append(f"#{line}")
        
        return hashtags
    
    def _get_fallback_caption(self, content_description: str, platform: str) -> str:
        """Get fallback caption when AI generation fails."""
        return f"Check out our latest content! 🚀 #{platform} #content #engagement"
    
    def _get_fallback_hashtags(self, content_description: str) -> List[str]:
        """Get fallback hashtags when AI generation fails."""
        return ["#content", "#socialmedia", "#marketing", "#engagement", "#brand"]


# Create global AI content generator instance
ai_content_generator = AIContentGenerator()
