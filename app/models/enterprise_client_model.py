from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
import json

class EnterpriseClientBase(SQLModel):
    """Base enterprise client model with common fields"""
    name: str = Field(max_length=200)
    email: str = Field(unique=True, index=True)
    contact_person: str = Field(max_length=100)
    phone: Optional[str] = Field(default=None, max_length=20)
    address: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class EnterpriseClient(EnterpriseClientBase, table=True):
    """Enterprise client model for database"""
    __tablename__ = "enterprise_clients"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    role_ids: str = Field(default="[]")  # JSON string of role IDs
    permissions: str = Field(default="[]")  # JSON string of permission IDs

class EnterpriseClientCreate(SQLModel):
    """Enterprise client creation model"""
    name: str = Field(max_length=200)
    email: str
    contact_person: str = Field(max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    role_ids: List[str] = []  # List of role IDs
    permissions: List[str] = []  # List of permission IDs

class EnterpriseClientUpdate(SQLModel):
    """Enterprise client update model"""
    name: Optional[str] = Field(None, max_length=200)
    email: Optional[str] = None
    contact_person: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    is_active: Optional[bool] = None
    role_ids: Optional[List[str]] = None
    permissions: Optional[List[str]] = None

class EnterpriseClientResponse(EnterpriseClientBase):
    """Enterprise client response model"""
    id: UUID
    role_ids: List[str] = []  # Converted from JSON string
    permissions: List[str] = []  # Converted from JSON string
