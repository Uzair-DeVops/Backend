from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4

class AdminPermissionBase(SQLModel):
    """Base admin permission model with common fields"""
    name: str = Field(unique=True, index=True, max_length=100)
    description: Optional[str] = Field(default=None)
    action: str = Field(max_length=100, index=True)
    resource: str = Field(max_length=100, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class AdminPermission(AdminPermissionBase, table=True):
    """Admin permission model for database"""
    __tablename__ = "admin_permissions"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)

class AdminPermissionCreate(SQLModel):
    """Admin permission creation model"""
    name: str = Field(max_length=100)
    description: Optional[str] = None
    action: str = Field(max_length=100)
    resource: str = Field(max_length=100)

class AdminPermissionUpdate(SQLModel):
    """Admin permission update model"""
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    action: Optional[str] = Field(None, max_length=100)
    resource: Optional[str] = Field(None, max_length=100)

class AdminPermissionResponse(AdminPermissionBase):
    """Admin permission response model"""
    id: UUID
