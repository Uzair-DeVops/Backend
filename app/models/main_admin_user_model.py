from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
import json

class MainAdminUserBase(SQLModel):
    """Base main admin user model with common fields"""
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    full_name: str = Field(max_length=100)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class MainAdminUser(MainAdminUserBase, table=True):
    """Main admin user model for database"""
    __tablename__ = "main_admin_users"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    password: str
    role_id: Optional[UUID] = Field(default=None, foreign_key="main_admin_roles.id")
    permissions: str = Field(default="[]")  # JSON string of permission IDs

class MainAdminUserCreate(SQLModel):
    """Main admin user creation model"""
    email: str
    username: str
    full_name: str
    password: str
    role_id: Optional[UUID] = None
    permissions: List[str] = []  # List of permission IDs

class MainAdminUserUpdate(SQLModel):
    """Main admin user update model"""
    email: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    role_id: Optional[UUID] = None
    permissions: Optional[List[str]] = None
    is_active: Optional[bool] = None

class MainAdminUserResponse(MainAdminUserBase):
    """Main admin user response model"""
    id: UUID
    role_id: Optional[UUID] = None
    permissions: List[str] = []  # Converted from JSON string

class MainAdminUserLogin(SQLModel):
    """Main admin user login model"""
    email: str
    password: str
