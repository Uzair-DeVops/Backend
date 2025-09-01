from datetime import datetime
from typing import Optional, List, Dict
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
import json

class EnterpriseUserBase(SQLModel):
    """Base enterprise user model with common fields"""
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True, max_length=50)
    full_name: str = Field(max_length=100)
    user_type: str = Field(max_length=50)  # e.g., "finance_team", "account_team", "support_team"
    department: Optional[str] = Field(default=None, max_length=100)
    position: Optional[str] = Field(default=None, max_length=100)
    phone: Optional[str] = Field(default=None, max_length=20)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class EnterpriseUser(EnterpriseUserBase, table=True):
    """Enterprise user model for database"""
    __tablename__ = "enterprise_users"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    password: str = Field(max_length=255)
    role_ids: str = Field(default="[]")  # JSON string of enterprise role IDs
    permissions: str = Field(default="[]")  # JSON string of enterprise permission IDs
    settings: str = Field(default="{}")  # JSON string of user-specific settings
    enterprise_client_id: UUID = Field(foreign_key="enterprise_clients.id")
    created_by: UUID = Field(foreign_key="enterprise_admins.id")

class EnterpriseUserCreate(SQLModel):
    """Enterprise user creation model"""
    email: str
    username: str = Field(max_length=50)
    full_name: str = Field(max_length=100)
    user_type: str = Field(max_length=50)
    department: Optional[str] = Field(None, max_length=100)
    position: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    password: str = Field(min_length=8)
    role_ids: List[str] = []  # List of enterprise role IDs
    permissions: List[str] = []  # List of enterprise permission IDs
    settings: Dict = {}  # User-specific settings
    enterprise_client_id: UUID
    created_by: UUID

class EnterpriseUserUpdate(SQLModel):
    """Enterprise user update model"""
    email: Optional[str] = None
    username: Optional[str] = Field(None, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)
    user_type: Optional[str] = Field(None, max_length=50)
    department: Optional[str] = Field(None, max_length=100)
    position: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None
    role_ids: Optional[List[str]] = None
    permissions: Optional[List[str]] = None
    settings: Optional[Dict] = None

class EnterpriseUserResponse(EnterpriseUserBase):
    """Enterprise user response model"""
    id: UUID
    role_ids: List[str] = []  # Converted from JSON string
    permissions: List[str] = []  # Converted from JSON string
    settings: Dict = {}  # Converted from JSON string
    enterprise_client_id: UUID
    created_by: UUID 
