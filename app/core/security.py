"""
Security and authentication utilities.

This module provides JWT token handling, password hashing,
and user authentication functionality.
"""

from datetime import datetime, timedelta
from typing import Optional, Union, Any
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Hash a password.
        
        Args:
            password: The plain text password
            
        Returns:
            str: The hashed password
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token.
        
        Args:
            data: The data to encode in the token
            expires_delta: Token expiration time
            
        Returns:
            str: The encoded JWT token
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        """
        Verify and decode a JWT token.
        
        Args:
            token: The JWT token to verify
            
        Returns:
            dict: The decoded token payload, or None if invalid
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except JWTError:
            return None


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get the current authenticated user from JWT token.
    
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
            
        # Here you would typically fetch user from database
        # For now, return the payload
        return {"user_id": user_id, **payload}
        
    except JWTError:
        raise credentials_exception


def create_api_key(length: int = 32) -> str:
    """
    Generate a secure API key.
    
    Args:
        length: Length of the API key
        
    Returns:
        str: Generated API key
    """
    import secrets
    import string
    
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


class EncryptionManager:
    """Encryption utilities for sensitive data."""
    
    @staticmethod
    def encrypt_credentials(data: str) -> str:
        """
        Encrypt sensitive credential data.
        
        Args:
            data: The data to encrypt
            
        Returns:
            str: Encrypted data
        """
        from cryptography.fernet import Fernet
        
        # Generate key from settings
        key = settings.SECRET_KEY.encode()[:32]  # Fernet needs 32 bytes
        key = key.ljust(32, b'0')  # Pad if necessary
        
        # Create Fernet cipher
        cipher = Fernet(Fernet.generate_key())
        
        # Encrypt data
        encrypted = cipher.encrypt(data.encode())
        return encrypted.decode()
    
    @staticmethod
    def decrypt_credentials(encrypted_data: str) -> str:
        """
        Decrypt sensitive credential data.
        
        Args:
            encrypted_data: The encrypted data
            
        Returns:
            str: Decrypted data
        """
        from cryptography.fernet import Fernet
        
        # Generate key from settings
        key = settings.SECRET_KEY.encode()[:32]
        key = key.ljust(32, b'0')
        
        # Create Fernet cipher
        cipher = Fernet(key)
        
        # Decrypt data
        decrypted = cipher.decrypt(encrypted_data.encode())
        return decrypted.decode()


# Create global security manager instance
security_manager = SecurityManager()
encryption_manager = EncryptionManager()
