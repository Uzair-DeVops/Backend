from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4

class UserRoleBase(SQLModel):
    """Base user-role relationship model"""
    user_id: UUID = Field(foreign_key="users.id", index=True)
    role_id: UUID = Field(foreign_key="roles.id", index=True)
    assigned_by: UUID = Field(foreign_key="users.id")
    assigned_at: datetime = Field(default_factory=datetime.utcnow)

class UserRole(UserRoleBase, table=True):
    """User-Role relationship model for RBAC"""
    __tablename__ = "user_roles"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)

class UserRoleCreate(SQLModel):
    """User-role assignment creation model"""
    user_id: UUID
    role_id: UUID
    assigned_by: UUID

class UserRoleResponse(UserRoleBase):
    """User-role response model"""
    id: UUID
