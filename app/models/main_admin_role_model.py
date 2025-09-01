from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4

class MainAdminRoleBase(SQLModel):
    """Base main admin role model with common fields"""
    name: str = Field(unique=True, index=True, max_length=100)
    description: Optional[str] = Field(default=None)
    is_system_role: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class MainAdminRole(MainAdminRoleBase, table=True):
    """Main admin role model for database"""
    __tablename__ = "main_admin_roles"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)

class MainAdminRoleCreate(SQLModel):
    """Main admin role creation model"""
    name: str = Field(max_length=100)
    description: Optional[str] = None
    is_system_role: bool = False

class MainAdminRoleUpdate(SQLModel):
    """Main admin role update model"""
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    is_system_role: Optional[bool] = None

class MainAdminRoleResponse(MainAdminRoleBase):
    """Main admin role response model"""
    id: UUID
