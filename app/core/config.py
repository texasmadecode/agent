"""
Configuration management for the Automated Marketing Agent.

This module handles all application settings and environment variables,
providing a centralized configuration system with validation.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application settings
    DEBUG: bool = Field(default=True, env="DEBUG")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    SECRET_KEY: str = Field(default="dev-secret-key-change-in-production", env="SECRET_KEY")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Database settings - using SQLite for development
    DATABASE_URL: str = Field(default="sqlite:///./marketing_agent.db", env="DATABASE_URL")
    
    # Redis settings
    REDIS_URL: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    
    # OpenAI API settings
    OPENAI_API_KEY: str = Field(default="your-openai-key-here", env="OPENAI_API_KEY")
    
    # Social Media API settings
    TWITTER_API_KEY: Optional[str] = Field(default=None, env="TWITTER_API_KEY")
    TWITTER_API_SECRET: Optional[str] = Field(default=None, env="TWITTER_API_SECRET")
    TWITTER_ACCESS_TOKEN: Optional[str] = Field(default=None, env="TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_TOKEN_SECRET: Optional[str] = Field(default=None, env="TWITTER_ACCESS_TOKEN_SECRET")
    
    FACEBOOK_APP_ID: Optional[str] = Field(default=None, env="FACEBOOK_APP_ID")
    FACEBOOK_APP_SECRET: Optional[str] = Field(default=None, env="FACEBOOK_APP_SECRET")
    FACEBOOK_ACCESS_TOKEN: Optional[str] = Field(default=None, env="FACEBOOK_ACCESS_TOKEN")
    
    INSTAGRAM_CLIENT_ID: Optional[str] = Field(default=None, env="INSTAGRAM_CLIENT_ID")
    INSTAGRAM_CLIENT_SECRET: Optional[str] = Field(default=None, env="INSTAGRAM_CLIENT_SECRET")
    INSTAGRAM_ACCESS_TOKEN: Optional[str] = Field(default=None, env="INSTAGRAM_ACCESS_TOKEN")
    
    LINKEDIN_CLIENT_ID: Optional[str] = Field(default=None, env="LINKEDIN_CLIENT_ID")
    LINKEDIN_CLIENT_SECRET: Optional[str] = Field(default=None, env="LINKEDIN_CLIENT_SECRET")
    
    # File upload settings
    UPLOAD_DIR: str = Field(default="./uploads", env="UPLOAD_DIR")
    MAX_UPLOAD_SIZE: int = Field(default=10485760, env="MAX_UPLOAD_SIZE")  # 10MB
    
    # Email settings for notifications
    SMTP_HOST: Optional[str] = Field(default=None, env="SMTP_HOST")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USER: Optional[str] = Field(default=None, env="SMTP_USER")
    SMTP_PASSWORD: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    
    # Analytics settings
    ANALYTICS_RETENTION_DAYS: int = Field(default=365, env="ANALYTICS_RETENTION_DAYS")
    REPORT_GENERATION_TIME: str = Field(default="08:00", env="REPORT_GENERATION_TIME")
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()


def get_database_url() -> str:
    """Get the database URL with proper formatting."""
    return settings.DATABASE_URL


def get_redis_url() -> str:
    """Get the Redis URL with proper formatting."""
    return settings.REDIS_URL


def is_social_platform_configured(platform: str) -> bool:
    """Check if a social media platform is properly configured."""
    platform_configs = {
        "twitter": all([
            settings.TWITTER_API_KEY,
            settings.TWITTER_API_SECRET,
            settings.TWITTER_ACCESS_TOKEN,
            settings.TWITTER_ACCESS_TOKEN_SECRET
        ]),
        "facebook": all([
            settings.FACEBOOK_APP_ID,
            settings.FACEBOOK_APP_SECRET,
            settings.FACEBOOK_ACCESS_TOKEN
        ]),
        "instagram": all([
            settings.INSTAGRAM_CLIENT_ID,
            settings.INSTAGRAM_CLIENT_SECRET,
            settings.INSTAGRAM_ACCESS_TOKEN
        ]),
        "linkedin": all([
            settings.LINKEDIN_CLIENT_ID,
            settings.LINKEDIN_CLIENT_SECRET
        ])
    }
    
    return platform_configs.get(platform.lower(), False)


def get_configured_platforms() -> list[str]:
    """Get a list of all configured social media platforms."""
    platforms = ["twitter", "facebook", "instagram", "linkedin"]
    return [platform for platform in platforms if is_social_platform_configured(platform)]
