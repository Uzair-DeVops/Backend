from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
import json

class EnterprisePermissionBase(SQLModel):
    """Base enterprise permission model with common fields"""
    name: str = Field(max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    resource: str = Field(max_length=100)  # e.g., "end_client", "enterprise_admin"
    action: str = Field(max_length=50)     # e.g., "create", "read", "update", "delete"
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class EnterprisePermission(EnterprisePermissionBase, table=True):
    """Enterprise permission model for database"""
    __tablename__ = "enterprise_permissions"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    enterprise_client_id: UUID = Field(foreign_key="enterprise_clients.id")

class EnterprisePermissionCreate(SQLModel):
    """Enterprise permission creation model"""
    name: str = Field(max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    resource: str = Field(max_length=100)
    action: str = Field(max_length=50)
    enterprise_client_id: UUID

class EnterprisePermissionUpdate(SQLModel):
    """Enterprise permission update model"""
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    resource: Optional[str] = Field(None, max_length=100)
    action: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None

class EnterprisePermissionResponse(EnterprisePermissionBase):
    """Enterprise permission response model"""
    id: UUID
    enterprise_client_id: UUID
