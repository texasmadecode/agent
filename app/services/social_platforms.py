"""
Social media platform integrations.

This module provides unified interfaces for posting to different
social media platforms including Instagram, Facebook, Twitter, LinkedIn, and TikTok.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from app.core.config import settings
from app.core.security import encryption_manager

logger = logging.getLogger(__name__)


class BasePlatformAPI:
    """Base class for social media platform APIs."""
    
    def __init__(self, credentials: Dict[str, str]):
        """Initialize with encrypted credentials."""
        self.credentials = credentials
        self.platform_name = "base"
    
    async def post_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Post content to the platform."""
        raise NotImplementedError("Subclasses must implement post_content")
    
    async def get_post_analytics(self, post_id: str) -> Dict[str, Any]:
        """Get analytics for a specific post."""
        raise NotImplementedError("Subclasses must implement get_post_analytics")
    
    async def delete_post(self, post_id: str) -> bool:
        """Delete a post from the platform."""
        raise NotImplementedError("Subclasses must implement delete_post")
    
    def _decrypt_credentials(self) -> Dict[str, str]:
        """Decrypt stored credentials."""
        decrypted = {}
        for key, encrypted_value in self.credentials.items():
            try:
                decrypted[key] = encryption_manager.decrypt_credentials(encrypted_value)
            except Exception as e:
                logger.error(f"Error decrypting credential {key}: {e}")
                decrypted[key] = encrypted_value  # Fallback to original if decryption fails
        return decrypted


class InstagramAPI(BasePlatformAPI):
    """Instagram API integration."""
    
    def __init__(self, credentials: Dict[str, str]):
        super().__init__(credentials)
        self.platform_name = "instagram"
        self.base_url = "https://graph.instagram.com"
    
    async def post_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Post content to Instagram.
        
        Args:
            content: Content data including caption, media_urls, etc.
            
        Returns:
            Post result with platform post ID
        """
        try:
            creds = self._decrypt_credentials()
            
            # Mock Instagram posting logic
            # In a real implementation, you would:
            # 1. Upload media to Instagram
            # 2. Create media container
            # 3. Publish the container
            
            post_data = {
                "caption": content.get("caption", ""),
                "image_url": content.get("media_urls", [None])[0] if content.get("media_urls") else None,
                "access_token": creds.get("access_token")
            }
            
            # Simulate API response
            platform_post_id = f"ig_{int(datetime.utcnow().timestamp())}"
            
            logger.info(f"Posted to Instagram: {platform_post_id}")
            
            return {
                "success": True,
                "platform_post_id": platform_post_id,
                "platform": "instagram",
                "posted_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error posting to Instagram: {e}")
            return {
                "success": False,
                "error": str(e),
                "platform": "instagram"
            }
    
    async def get_post_analytics(self, post_id: str) -> Dict[str, Any]:
        """Get Instagram post analytics."""
        try:
            # Mock analytics data
            analytics = {
                "post_id": post_id,
                "platform": "instagram",
                "likes": 127,
                "comments": 15,
                "shares": 8,
                "saves": 23,
                "reach": 1500,
                "impressions": 2100,
                "engagement_rate": 8.5,
                "collected_at": datetime.utcnow().isoformat()
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting Instagram analytics for {post_id}: {e}")
            return {}


class FacebookAPI(BasePlatformAPI):
    """Facebook API integration."""
    
    def __init__(self, credentials: Dict[str, str]):
        super().__init__(credentials)
        self.platform_name = "facebook"
        self.base_url = "https://graph.facebook.com"
    
    async def post_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Post content to Facebook."""
        try:
            creds = self._decrypt_credentials()
            
            # Mock Facebook posting logic
            platform_post_id = f"fb_{int(datetime.utcnow().timestamp())}"
            
            logger.info(f"Posted to Facebook: {platform_post_id}")
            
            return {
                "success": True,
                "platform_post_id": platform_post_id,
                "platform": "facebook",
                "posted_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error posting to Facebook: {e}")
            return {
                "success": False,
                "error": str(e),
                "platform": "facebook"
            }
    
    async def get_post_analytics(self, post_id: str) -> Dict[str, Any]:
        """Get Facebook post analytics."""
        try:
            analytics = {
                "post_id": post_id,
                "platform": "facebook",
                "likes": 89,
                "comments": 12,
                "shares": 25,
                "reach": 1200,
                "impressions": 1800,
                "engagement_rate": 6.8,
                "collected_at": datetime.utcnow().isoformat()
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting Facebook analytics for {post_id}: {e}")
            return {}


class TwitterAPI(BasePlatformAPI):
    """Twitter API integration."""
    
    def __init__(self, credentials: Dict[str, str]):
        super().__init__(credentials)
        self.platform_name = "twitter"
        self.base_url = "https://api.twitter.com"
    
    async def post_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Post content to Twitter."""
        try:
            creds = self._decrypt_credentials()
            
            # Mock Twitter posting logic
            platform_post_id = f"tw_{int(datetime.utcnow().timestamp())}"
            
            logger.info(f"Posted to Twitter: {platform_post_id}")
            
            return {
                "success": True,
                "platform_post_id": platform_post_id,
                "platform": "twitter",
                "posted_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error posting to Twitter: {e}")
            return {
                "success": False,
                "error": str(e),
                "platform": "twitter"
            }
    
    async def get_post_analytics(self, post_id: str) -> Dict[str, Any]:
        """Get Twitter post analytics."""
        try:
            analytics = {
                "post_id": post_id,
                "platform": "twitter",
                "likes": 45,
                "retweets": 12,
                "replies": 8,
                "views": 890,
                "engagement_rate": 4.8,
                "collected_at": datetime.utcnow().isoformat()
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting Twitter analytics for {post_id}: {e}")
            return {}


class LinkedInAPI(BasePlatformAPI):
    """LinkedIn API integration."""
    
    def __init__(self, credentials: Dict[str, str]):
        super().__init__(credentials)
        self.platform_name = "linkedin"
        self.base_url = "https://api.linkedin.com"
    
    async def post_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Post content to LinkedIn."""
        try:
            creds = self._decrypt_credentials()
            
            # Mock LinkedIn posting logic
            platform_post_id = f"ln_{int(datetime.utcnow().timestamp())}"
            
            logger.info(f"Posted to LinkedIn: {platform_post_id}")
            
            return {
                "success": True,
                "platform_post_id": platform_post_id,
                "platform": "linkedin",
                "posted_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error posting to LinkedIn: {e}")
            return {
                "success": False,
                "error": str(e),
                "platform": "linkedin"
            }
    
    async def get_post_analytics(self, post_id: str) -> Dict[str, Any]:
        """Get LinkedIn post analytics."""
        try:
            analytics = {
                "post_id": post_id,
                "platform": "linkedin",
                "likes": 67,
                "comments": 9,
                "shares": 15,
                "views": 1200,
                "engagement_rate": 7.6,
                "collected_at": datetime.utcnow().isoformat()
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting LinkedIn analytics for {post_id}: {e}")
            return {}


class PlatformManager:
    """Manager for all social media platform APIs."""
    
    def __init__(self):
        """Initialize platform manager."""
        self.platforms = {}
    
    def get_platform_api(self, platform: str, credentials: Dict[str, str]) -> BasePlatformAPI:
        """Get API instance for a specific platform."""
        platform_classes = {
            "instagram": InstagramAPI,
            "facebook": FacebookAPI,
            "twitter": TwitterAPI,
            "linkedin": LinkedInAPI
        }
        
        if platform not in platform_classes:
            raise ValueError(f"Unsupported platform: {platform}")
        
        return platform_classes[platform](credentials)
    
    async def post_to_platform(self, platform: str, credentials: Dict[str, str], content: Dict[str, Any]) -> Dict[str, Any]:
        """Post content to a specific platform."""
        try:
            api = self.get_platform_api(platform, credentials)
            result = await api.post_content(content)
            return result
            
        except Exception as e:
            logger.error(f"Error posting to {platform}: {e}")
            return {
                "success": False,
                "error": str(e),
                "platform": platform
            }
    
    async def get_platform_analytics(self, platform: str, credentials: Dict[str, str], post_id: str) -> Dict[str, Any]:
        """Get analytics from a specific platform."""
        try:
            api = self.get_platform_api(platform, credentials)
            analytics = await api.get_post_analytics(post_id)
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting analytics from {platform}: {e}")
            return {}


# Create global platform manager instance
platform_manager = PlatformManager()
