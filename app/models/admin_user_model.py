from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
import json

class AdminUserBase(SQLModel):
    """Base admin user model with common fields"""
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    full_name: str = Field(max_length=100)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class AdminUser(AdminUserBase, table=True):
    """Admin user model for database"""
    __tablename__ = "admin_users"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    password: str
    role_ids: str = Field(default="[]")  # JSON string of role IDs
    permissions: str = Field(default="[]")  # JSON string of permission IDs

class AdminUserCreate(SQLModel):
    """Admin user creation model"""
    email: str
    username: str
    full_name: str
    password: str
    role_ids: List[str] = []  # List of role IDs
    permissions: List[str] = []  # List of permission IDs

class AdminUserUpdate(SQLModel):
    """Admin user update model"""
    email: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    role_ids: Optional[List[str]] = None
    permissions: Optional[List[str]] = None
    is_active: Optional[bool] = None

class AdminUserResponse(AdminUserBase):
    """Admin user response model"""
    id: UUID
    role_ids: List[str] = []  # Converted from JSON string
    permissions: List[str] = []  # Converted from JSON string

class AdminUserLogin(SQLModel):
    """Admin user login model"""
    email: str
    password: str
