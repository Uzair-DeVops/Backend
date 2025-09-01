from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4

class MainAdminPermissionBase(SQLModel):
    """Base main admin permission model with common fields"""
    name: str = Field(unique=True, index=True, max_length=100)
    description: Optional[str] = Field(default=None)
    action: str = Field(max_length=100, index=True)
    resource: str = Field(max_length=100, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class MainAdminPermission(MainAdminPermissionBase, table=True):
    """Main admin permission model for database"""
    __tablename__ = "main_admin_permissions"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)

class MainAdminPermissionCreate(SQLModel):
    """Main admin permission creation model"""
    name: str = Field(max_length=100)
    description: Optional[str] = None
    action: str = Field(max_length=100)
    resource: str = Field(max_length=100)

class MainAdminPermissionUpdate(SQLModel):
    """Main admin permission update model"""
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    action: Optional[str] = Field(None, max_length=100)
    resource: Optional[str] = Field(None, max_length=100)

class MainAdminPermissionResponse(MainAdminPermissionBase):
    """Main admin permission response model"""
    id: UUID
