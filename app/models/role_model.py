from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4

class RoleBase(SQLModel):
    """Base role model with common fields"""
    name: str = Field(unique=True, index=True, max_length=100)
    description: Optional[str] = Field(default=None)
    is_system_role: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Role(RoleBase, table=True):
    """Role model for RBAC"""
    __tablename__ = "roles"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)

class RoleCreate(SQLModel):
    """Role creation model"""
    name: str = Field(max_length=100)
    description: Optional[str] = None
    is_system_role: bool = False

class RoleCreateWithScopes(SQLModel):
    """Role creation model with scope assignments"""
    name: str = Field(max_length=100)
    description: Optional[str] = None
    is_system_role: bool = False
    scope_ids: List[UUID] = Field(default=[], description="List of scope IDs to assign to this role")

class RoleUpdate(SQLModel):
    """Role update model"""
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    is_system_role: Optional[bool] = None

class RoleResponse(RoleBase):
    """Role response model"""
    id: UUID
