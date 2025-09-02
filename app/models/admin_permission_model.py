from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from uuid import uuid4

class AdminPermissionBase(SQLModel):
    """Base admin permission model with common fields"""
    name: str = Field(unique=True, index=True, max_length=100)
    description: Optional[str] = Field(default=None)
    action: str = Field(max_length=100, index=True)
    resource: str = Field(max_length=100, index=True)
    is_active: bool = Field(default=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class AdminPermission(AdminPermissionBase, table=True):
    """Admin permission model for database"""
    __tablename__ = "admin_permissions"
    
    id: str = Field(default_factory=lambda: str(uuid4()).replace('-', ''), primary_key=True)

class AdminPermissionCreate(SQLModel):
    """Admin permission creation model"""
    name: str = Field(max_length=100)
    description: Optional[str] = None
    action: str = Field(max_length=100)
    resource: str = Field(max_length=100)
    is_active: bool = True

class AdminPermissionUpdate(SQLModel):
    """Admin permission update model"""
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    action: Optional[str] = Field(None, max_length=100)
    resource: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None

class AdminPermissionResponse(AdminPermissionBase):
    """Admin permission response model"""
    id: str
