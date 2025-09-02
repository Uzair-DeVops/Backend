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
from ..models.admin_user_model import AdminUser
from ..utils.database_dependency import get_database_session
from ..services.auth_service import require_admin_user_service as require_admin_user
from ..utils.my_logger import get_logger

logger = get_logger("ADMIN_ROLE_ROUTES")

router = APIRouter(prefix="/roles", tags=["Admin Roles"])

@router.post("/", response_model=AdminRoleResponse)
async def create_admin_role_endpoint(
    role_data: AdminRoleCreate,
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Create a new admin role - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} creating new admin role")
    return create_admin_role(role_data, db)

@router.get("/", response_model=List[AdminRoleResponse])
async def get_admin_roles_endpoint(
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Get all admin roles - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} fetching all admin roles")
    return get_all_admin_roles(db)

@router.get("/{role_id}", response_model=AdminRoleResponse)
async def get_admin_role_endpoint(
    role_id: str,
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Get admin role by ID - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} fetching admin role {role_id}")
    role = get_admin_role_by_id(role_id, db)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    return role
