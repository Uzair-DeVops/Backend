from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4

class RoleScopeBase(SQLModel):
    """Base role-scope relationship model"""
    role_id: UUID = Field(foreign_key="roles.id", index=True)
    scope_id: UUID = Field(foreign_key="scopes.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class RoleScope(RoleScopeBase, table=True):
    """Role-Scope relationship model for RBAC"""
    __tablename__ = "role_scopes"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)

class RoleScopeCreate(SQLModel):
    """Role-scope assignment creation model"""
    role_id: UUID
    scope_id: UUID

class RoleScopeResponse(RoleScopeBase):
    """Role-scope response model"""
    id: UUID
