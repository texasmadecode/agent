"""
User and client management models.

This module defines the database models for users, clients,
and their associated authentication and settings.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from app.core.database import Base


class User(Base):
    """User model for system administrators and operators."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    clients = relationship("Client", back_populates="user")


class Client(Base):
    """Client model for marketing campaign management."""
    
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    company = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    website = Column(String(255))
    description = Column(Text)
    
    # Brand settings
    brand_voice = Column(Text)  # JSON string for brand voice guidelines
    brand_colors = Column(JSON)  # Brand color palette
    brand_fonts = Column(JSON)  # Brand typography settings
    brand_guidelines = Column(Text)  # Additional brand guidelines
    
    # User association
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Status and metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="clients")
    social_accounts = relationship("SocialAccount", back_populates="client")
    content_items = relationship("ContentItem", back_populates="client")
    campaigns = relationship("Campaign", back_populates="client")
    scheduled_posts = relationship("ScheduledPost", back_populates="client")


class SocialAccount(Base):
    """Social media account credentials and settings."""
    
    __tablename__ = "social_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    platform = Column(String(50), nullable=False)  # twitter, facebook, instagram, etc.
    account_name = Column(String(255))
    account_id = Column(String(255))  # Platform-specific account ID
    
    # Encrypted credentials
    access_token = Column(Text)  # Encrypted access token
    refresh_token = Column(Text)  # Encrypted refresh token
    api_credentials = Column(Text)  # Encrypted JSON of additional credentials
    
    # Settings
    is_active = Column(Boolean, default=True)
    auto_post = Column(Boolean, default=True)
    optimal_times = Column(JSON)  # Optimal posting times for this account
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_sync = Column(DateTime(timezone=True))
    
    # Relationships
    client = relationship("Client", back_populates="social_accounts")
    posts = relationship("Post", back_populates="social_account")


class Campaign(Base):
    """Marketing campaign model."""
    
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Campaign settings
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    budget = Column(String(50))  # Budget information
    target_audience = Column(JSON)  # Target audience settings
    goals = Column(JSON)  # Campaign goals and KPIs
    
    # Content strategy
    content_themes = Column(JSON)  # Content themes and topics
    posting_frequency = Column(JSON)  # Posting frequency per platform
    hashtag_strategy = Column(JSON)  # Hashtag strategy
    
    # Status
    status = Column(String(50), default="draft")  # draft, active, paused, completed
    is_active = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    client = relationship("Client", back_populates="campaigns")
    scheduled_posts = relationship("ScheduledPost", back_populates="campaign")
