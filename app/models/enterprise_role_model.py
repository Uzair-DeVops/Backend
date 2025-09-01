from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
import json

class EnterpriseRoleBase(SQLModel):
    """Base enterprise role model with common fields"""
    name: str = Field(max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class EnterpriseRole(EnterpriseRoleBase, table=True):
    """Enterprise role model for database"""
    __tablename__ = "enterprise_roles"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    permissions: str = Field(default="[]")  # JSON string of permission IDs
    enterprise_client_id: UUID = Field(foreign_key="enterprise_clients.id")

class EnterpriseRoleCreate(SQLModel):
    """Enterprise role creation model"""
    name: str = Field(max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    permissions: List[str] = []  # List of permission IDs
    enterprise_client_id: UUID

class EnterpriseRoleUpdate(SQLModel):
    """Enterprise role update model"""
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None
    permissions: Optional[List[str]] = None

class EnterpriseRoleResponse(EnterpriseRoleBase):
    """Enterprise role response model"""
    id: UUID
    permissions: List[str] = []  # Converted from JSON string
    enterprise_client_id: UUID
