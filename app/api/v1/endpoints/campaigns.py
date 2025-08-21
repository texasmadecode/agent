"""Campaigns API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from app.core.database import get_db
from app.core.security import get_current_user

router = APIRouter()

@router.get("/")
async def get_campaigns(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    """Get list of campaigns."""
    return [{"id": 1, "name": "Summer Campaign", "status": "active", "start_date": "2025-08-15", "end_date": "2025-09-15"}]

@router.post("/")
async def create_campaign(campaign_data: Dict[str, Any], current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Create a new campaign."""
    return {"message": "Campaign created successfully", "campaign_id": 123}
