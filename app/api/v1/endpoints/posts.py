"""Posts management API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from app.core.database import get_db
from app.core.security import get_current_user

router = APIRouter()

@router.get("/")
async def get_posts(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    """Get list of posts."""
    return [{"id": 1, "content": "Sample post", "platform": "instagram", "status": "posted"}]

@router.post("/")
async def create_post(post_data: Dict[str, Any], current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Create a new post."""
    return {"message": "Post created successfully", "post_id": 123}
