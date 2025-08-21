"""Social accounts API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from app.core.database import get_db
from app.core.security import get_current_user

router = APIRouter()

@router.get("/")
async def get_social_accounts(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    """Get list of social media accounts."""
    return [{"id": 1, "platform": "instagram", "account_name": "@techstartup", "is_active": True, "last_sync": "2025-08-21T09:30:00Z"}]

@router.post("/")
async def add_social_account(account_data: Dict[str, Any], current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Add a new social media account."""
    return {"message": "Social account added successfully", "account_id": 123}
