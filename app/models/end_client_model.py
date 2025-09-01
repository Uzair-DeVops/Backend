from datetime import datetime
from typing import Optional, List, Dict
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
import json

class EndClientBase(SQLModel):
    """Base end client model with common fields"""
    name: str = Field(max_length=200)
    email: str = Field(unique=True, index=True)
    contact_person: str = Field(max_length=100)
    phone: Optional[str] = Field(default=None, max_length=20)
    address: Optional[str] = Field(default=None)
    company_size: Optional[str] = Field(default=None, max_length=50)
    industry: Optional[str] = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class EndClient(EndClientBase, table=True):
    """End client model for database"""
    __tablename__ = "end_clients"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    settings: str = Field(default="{}")  # JSON string of client settings
    enterprise_client_id: UUID = Field(foreign_key="enterprise_clients.id")
    created_by: UUID = Field(foreign_key="enterprise_admins.id")

class EndClientCreate(SQLModel):
    """End client creation model"""
    name: str = Field(max_length=200)
    email: str
    contact_person: str = Field(max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    company_size: Optional[str] = Field(None, max_length=50)
    industry: Optional[str] = Field(None, max_length=100)
    settings: Dict = {}  # Client-specific settings
    enterprise_client_id: UUID
    created_by: UUID

class EndClientUpdate(SQLModel):
    """End client update model"""
    name: Optional[str] = Field(None, max_length=200)
    email: Optional[str] = None
    contact_person: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    company_size: Optional[str] = Field(None, max_length=50)
    industry: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None
    settings: Optional[Dict] = None

class EndClientResponse(EndClientBase):
    """End client response model"""
    id: UUID
    settings: Dict = {}  # Converted from JSON string
    enterprise_client_id: UUID
    created_by: UUID
