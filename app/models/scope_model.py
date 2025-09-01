from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4

class ScopeBase(SQLModel):
    """Base scope model with common fields"""
    name: str = Field(unique=True, index=True, max_length=100)
    description: Optional[str] = Field(default=None)
    resource: str = Field(max_length=100, index=True)
    action: str = Field(max_length=50, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Scope(ScopeBase, table=True):
    """Scope model for RBAC permissions"""
    __tablename__ = "scopes"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)

class ScopeCreate(SQLModel):
    """Scope creation model"""
    name: str = Field(max_length=100)
    description: Optional[str] = None
    resource: str = Field(max_length=100)
    action: str = Field(max_length=50)

class ScopeUpdate(SQLModel):
    """Scope update model"""
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    resource: Optional[str] = Field(None, max_length=100)
    action: Optional[str] = Field(None, max_length=50)

class ScopeResponse(ScopeBase):
    """Scope response model"""
    id: UUID 