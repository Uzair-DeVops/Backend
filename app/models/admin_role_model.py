from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
import json

class AdminRoleBase(SQLModel):
    """Base admin role model with common fields"""
    name: str = Field(unique=True, index=True, max_length=100)
    description: Optional[str] = Field(default=None)
    is_system_role: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class AdminRole(AdminRoleBase, table=True):
    """Admin role model for database"""
    __tablename__ = "admin_roles"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    permissions: str = Field(default="[]")  # JSON string of permission IDs

class AdminRoleCreate(SQLModel):
    """Admin role creation model"""
    name: str = Field(max_length=100)
    description: Optional[str] = None
    is_system_role: bool = False
    permissions: List[str] = []  # List of permission IDs

class AdminRoleUpdate(SQLModel):
    """Admin role update model"""
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    is_system_role: Optional[bool] = None
    permissions: Optional[List[str]] = None

class AdminRoleResponse(AdminRoleBase):
    """Admin role response model"""
    id: UUID
    permissions: List[str] = []  # Converted from JSON string
