"""
Main Admin Permission routes for permission management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from ..controllers.admin_permission_controller import (
    create_admin_permission,
    get_all_admin_permissions
)
from ..models.admin_permission_model import (
    AdminPermissionCreate, AdminPermissionResponse
)
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger

logger = get_logger("ADMIN_PERMISSION_ROUTES")

router = APIRouter(prefix="/permissions", tags=["Admin Permissions"])

@router.post("/", response_model=AdminPermissionResponse)
async def create_admin_permission_endpoint(
    permission_data: AdminPermissionCreate, 
    db: Session = Depends(get_database_session)
):
    """Create a new admin permission"""
    return create_admin_permission(permission_data, db)

@router.get("/", response_model=List[AdminPermissionResponse])
async def get_admin_permissions_endpoint(
    db: Session = Depends(get_database_session)
):
    """Get all admin permissions"""
    return get_all_admin_permissions(db)
