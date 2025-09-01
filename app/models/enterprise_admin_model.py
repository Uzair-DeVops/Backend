from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
import json

class EnterpriseAdminBase(SQLModel):
    """Base enterprise admin model with common fields"""
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True, max_length=50)
    full_name: str = Field(max_length=100)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class EnterpriseAdmin(EnterpriseAdminBase, table=True):
    """Enterprise admin model for database"""
    __tablename__ = "enterprise_admins"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    password: str = Field(max_length=255)
    role_ids: str = Field(default="[]")  # JSON string of role IDs
    permissions: str = Field(default="[]")  # JSON string of permission IDs
    enterprise_client_id: Optional[UUID] = Field(default=None, foreign_key="enterprise_clients.id")

class EnterpriseAdminCreate(SQLModel):
    """Enterprise admin creation model"""
    email: str
    username: str = Field(max_length=50)
    full_name: str = Field(max_length=100)
    password: str = Field(min_length=8)
    role_ids: List[str] = []  # List of role IDs
    permissions: List[str] = []  # List of permission IDs
    enterprise_client_id: Optional[UUID] = None

class EnterpriseAdminUpdate(SQLModel):
    """Enterprise admin update model"""
    email: Optional[str] = None
    username: Optional[str] = Field(None, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None
    role_ids: Optional[List[str]] = None
    permissions: Optional[List[str]] = None
    enterprise_client_id: Optional[UUID] = None

class EnterpriseAdminResponse(EnterpriseAdminBase):
    """Enterprise admin response model"""
    id: UUID
    role_ids: List[str] = []  # Converted from JSON string
    permissions: List[str] = []  # Converted from JSON string
    enterprise_client_id: Optional[UUID] = None
