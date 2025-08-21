"""
Security and authentication utilities.

This module provides basic authentication functionality for development.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import hashlib
import secrets
import base64
import json

from app.core.config import settings

# JWT security
security = HTTPBearer()


class SecurityManager:
    """Security and authentication manager."""
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against its hash.
        
        Args:
            plain_password: The plain text password
            hashed_password: The hashed password
            
        Returns:
            bool: True if password matches, False otherwise
        """
        # Simple hash verification for development
        return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Hash a password.
        
        Args:
            password: The plain text password
            
        Returns:
            str: The hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a simple access token.
        
        Args:
            data: The data to encode in the token
            expires_delta: Token expiration time
            
        Returns:
            str: The encoded token
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire.isoformat()})
        
        # Simple base64 encoding for development
        token_str = json.dumps(to_encode)
        encoded_token = base64.b64encode(token_str.encode()).decode()
        
        return encoded_token
    
    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        """
        Verify and decode a token.
        
        Args:
            token: The token to verify
            
        Returns:
            dict: The decoded token payload, or None if invalid
        """
        try:
            # Simple base64 decoding for development
            decoded_str = base64.b64decode(token.encode()).decode()
            payload = json.loads(decoded_str)
            
            # Check expiration
            exp_str = payload.get("exp")
            if exp_str:
                exp_time = datetime.fromisoformat(exp_str)
                if datetime.utcnow() > exp_time:
                    return None
            
            return payload
        except Exception:
            return None


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get the current authenticated user from token.
    
    Args:
        credentials: HTTP authorization credentials
        
    Returns:
        dict: User information from token
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = SecurityManager.verify_token(credentials.credentials)
        if payload is None:
            raise credentials_exception
        
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
        # Return user information
        return {"user_id": user_id, **payload}
        
    except Exception:
        raise credentials_exception


def create_api_key(length: int = 32) -> str:
    """
    Generate a secure API key.
    
    Args:
        length: Length of the API key
        
    Returns:
        str: Generated API key
    """
    import string
    
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


class EncryptionManager:
    """Simple encryption utilities for development."""
    
    @staticmethod
    def encrypt_credentials(data: str) -> str:
        """
        Simple encryption for development.
        
        Args:
            data: The data to encrypt
            
        Returns:
            str: Encrypted data
        """
        # Simple base64 encoding for development
        return base64.b64encode(data.encode()).decode()
    
    @staticmethod
    def decrypt_credentials(encrypted_data: str) -> str:
        """
        Simple decryption for development.
        
        Args:
            encrypted_data: The encrypted data
            
        Returns:
            str: Decrypted data
        """
        try:
            return base64.b64decode(encrypted_data.encode()).decode()
        except Exception:
            return encrypted_data  # Return original if decryption fails


# Create global security manager instance
security_manager = SecurityManager()
encryption_manager = EncryptionManager()
