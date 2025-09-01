"""
Main Admin Role routes for role management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from ..controllers.admin_role_controller import (
    create_admin_role,
    get_admin_role_by_id,
    get_all_admin_roles
)
from ..models.admin_role_model import (
    AdminRoleCreate, AdminRoleResponse
)
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger

logger = get_logger("ADMIN_ROLE_ROUTES")

router = APIRouter(prefix="/roles", tags=["Admin Roles"])

@router.post("/", response_model=AdminRoleResponse)
async def create_admin_role_endpoint(
    role_data: AdminRoleCreate,
    db: Session = Depends(get_database_session)
):
    """Create a new admin role"""
    return create_admin_role(role_data, db)

@router.get("/", response_model=List[AdminRoleResponse])
async def get_admin_roles_endpoint(
    db: Session = Depends(get_database_session)
):
    """Get all admin roles"""
    return get_all_admin_roles(db)

@router.get("/{role_id}", response_model=AdminRoleResponse)
async def get_admin_role_endpoint(
    role_id: str,
    db: Session = Depends(get_database_session)
):
    """Get admin role by ID"""
    role = get_admin_role_by_id(role_id, db)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    return role
