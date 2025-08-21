"""
Authentication API endpoints.

This module handles user authentication, registration,
and token management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Dict, Any

from app.core.database import get_db
from app.core.security import SecurityManager, get_current_user

router = APIRouter()


@router.post("/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Authenticate user and return access token.
    
    Args:
        form_data: Username and password form data
        db: Database session
        
    Returns:
        Access token and token type
    """
    try:
        # In a real implementation, you would validate credentials against the database
        # For demo purposes, accept any username/password
        if not form_data.username or not form_data.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=30)
        access_token = SecurityManager.create_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 1800,  # 30 minutes
            "user": {
                "username": form_data.username,
                "email": f"{form_data.username}@example.com"
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication error: {str(e)}"
        )


@router.post("/register")
async def register_user(
    user_data: Dict[str, Any],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Register a new user.
    
    Args:
        user_data: User registration data
        db: Database session
        
    Returns:
        Success message and user info
    """
    try:
        # In a real implementation, you would:
        # 1. Validate the user data
        # 2. Check if user already exists
        # 3. Hash the password
        # 4. Save to database
        
        return {
            "message": "User registered successfully",
            "user": {
                "username": user_data.get("username"),
                "email": user_data.get("email"),
                "created_at": "2025-08-21T10:00:00Z"
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration error: {str(e)}"
        )


@router.get("/me")
async def get_current_user_info(
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get current user information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User information
    """
    return {
        "user": current_user,
        "permissions": ["read", "write", "admin"],
        "last_login": "2025-08-21T09:30:00Z"
    }


@router.post("/logout")
async def logout(
    current_user: dict = Depends(get_current_user)
) -> Dict[str, str]:
    """
    Logout current user.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Success message
    """
    # In a real implementation, you might:
    # 1. Blacklist the token
    # 2. Update last logout time in database
    
    return {"message": "Successfully logged out"}
