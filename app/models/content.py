"""
Content management models.

This module defines database models for content items,
posts, media files, and content analytics.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum

from app.core.database import Base


class ContentType(str, Enum):
    """Content type enumeration."""
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    GIF = "gif"
    CAROUSEL = "carousel"
    STORY = "story"


class PostStatus(str, Enum):
    """Post status enumeration."""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    POSTED = "posted"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ContentItem(Base):
    """Content repository model."""
    
    __tablename__ = "content_items"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, nullable=False)  # Foreign key to clients table
    
    # Content details
    title = Column(String(255))
    description = Column(Text)
    content_type = Column(String(50), nullable=False)  # text, image, video, etc.
    content_data = Column(Text)  # Main content (text, file path, etc.)
    
    # AI-generated metadata
    ai_generated = Column(Boolean, default=False)
    ai_prompt = Column(Text)  # Original AI prompt used
    ai_metadata = Column(JSON)  # AI analysis results
    
    # Content categorization
    tags = Column(JSON)  # Content tags
    categories = Column(JSON)  # Content categories
    keywords = Column(JSON)  # SEO keywords
    
    # Media information (for images/videos)
    file_path = Column(String(500))
    file_size = Column(Integer)
    file_format = Column(String(50))
    dimensions = Column(JSON)  # width, height for images/videos
    duration = Column(Float)  # Duration in seconds for videos
    
    # Content settings
    brand_compliant = Column(Boolean, default=True)
    approval_required = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=False)
    approved_by = Column(String(255))
    approved_at = Column(DateTime(timezone=True))
    
    # Usage tracking
    usage_count = Column(Integer, default=0)
    last_used = Column(DateTime(timezone=True))
    performance_score = Column(Float)  # Based on engagement metrics
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    client = relationship("Client", back_populates="content_items")
    posts = relationship("Post", back_populates="content_item")


class ScheduledPost(Base):
    """Scheduled post model."""
    
    __tablename__ = "scheduled_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, nullable=False)  # Foreign key to clients table
    campaign_id = Column(Integer)  # Optional foreign key to campaigns table
    content_item_id = Column(Integer)  # Foreign key to content_items table
    
    # Platform and account
    platform = Column(String(50), nullable=False)
    account_id = Column(String(255))  # Platform-specific account ID
    
    # Post content
    caption = Column(Text)
    hashtags = Column(JSON)  # List of hashtags
    mentions = Column(JSON)  # List of mentions
    media_urls = Column(JSON)  # URLs to media files
    
    # Scheduling
    scheduled_time = Column(DateTime(timezone=True), nullable=False)
    timezone = Column(String(100), default="UTC")
    
    # AI optimization
    ai_optimized = Column(Boolean, default=False)
    ai_suggestions = Column(JSON)  # AI optimization suggestions
    optimal_time_used = Column(Boolean, default=False)
    
    # Status tracking
    status = Column(String(50), default="scheduled")
    posted_at = Column(DateTime(timezone=True))
    post_id = Column(String(255))  # Platform-specific post ID after posting
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    client = relationship("Client", back_populates="scheduled_posts")
    campaign = relationship("Campaign", back_populates="scheduled_posts")
    post = relationship("Post", uselist=False, back_populates="scheduled_post")


class Post(Base):
    """Posted content model for tracking published posts."""
    
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    scheduled_post_id = Column(Integer)  # Foreign key to scheduled_posts table
    content_item_id = Column(Integer)  # Foreign key to content_items table
    social_account_id = Column(Integer, nullable=False)  # Foreign key to social_accounts table
    
    # Post details
    platform_post_id = Column(String(255), nullable=False)  # Platform-specific post ID
    platform = Column(String(50), nullable=False)
    caption = Column(Text)
    media_urls = Column(JSON)
    
    # Engagement metrics (updated periodically)
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    views_count = Column(Integer, default=0)
    clicks_count = Column(Integer, default=0)
    saves_count = Column(Integer, default=0)
    
    # Calculated metrics
    engagement_rate = Column(Float, default=0.0)
    reach = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    
    # Performance tracking
    performance_score = Column(Float)
    performance_trend = Column(String(50))  # improving, declining, stable
    
    # Metadata
    posted_at = Column(DateTime(timezone=True), nullable=False)
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    scheduled_post = relationship("ScheduledPost", back_populates="post")
    content_item = relationship("ContentItem", back_populates="posts")
    social_account = relationship("SocialAccount", back_populates="posts")
    analytics = relationship("PostAnalytics", back_populates="post")


class PostAnalytics(Base):
    """Detailed analytics for posts."""
    
    __tablename__ = "post_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, nullable=False)  # Foreign key to posts table
    
    # Time-based metrics
    recorded_at = Column(DateTime(timezone=True), nullable=False)
    
    # Engagement metrics snapshot
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    views = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    saves = Column(Integer, default=0)
    
    # Audience metrics
    reach = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    unique_viewers = Column(Integer, default=0)
    
    # Demographic data
    audience_demographics = Column(JSON)  # Age, gender, location breakdown
    
    # Platform-specific metrics
    platform_metrics = Column(JSON)  # Additional platform-specific data
    
    # Relationships
    post = relationship("Post", back_populates="analytics")
