"""
API v1 router configuration.

This module sets up all the API routes for version 1 of the
automated marketing agent API.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    clients,
    content,
    posts,
    analytics,
    campaigns,
    social_accounts,
    dashboard
)

# Create main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(clients.router, prefix="/clients", tags=["clients"])
api_router.include_router(content.router, prefix="/content", tags=["content"])
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])
api_router.include_router(social_accounts.router, prefix="/social-accounts", tags=["social-accounts"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
