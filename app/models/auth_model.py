"""
Authentication models for login functionality
"""
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field
from uuid import UUID

class LoginRequest(SQLModel):
    """Login request model"""
    email: str
    password: str

class LoginResponse(SQLModel):
    """Login response model"""
    access_token: str
    token_type: str = "bearer"
    user_id: UUID
    email: str
    username: str
    full_name: str
    role_ids: List[str] = []
    permissions: List[str] = []
    user_type: str  # "admin" or "enterprise_client"



class TokenData(SQLModel):
    """Token data model for JWT payload"""
    user_id: Optional[str] = None
    email: Optional[str] = None
    user_type: Optional[str] = None

class TokenResponse(SQLModel):
    """Token response model"""
    access_token: str
    token_type: str = "bearer"