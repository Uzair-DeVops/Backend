"""
Main Admin Permission routes for permission management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from ..controllers.admin_permission_controller import (
    create_admin_permission,
    get_all_admin_permissions,
    get_admin_permission_by_id,
    update_admin_permission,
    delete_admin_permission,
    activate_permission,
    deactivate_permission,
    get_permissions_by_resource
)
from ..models.admin_permission_model import (
    AdminPermissionCreate, AdminPermissionUpdate, AdminPermissionResponse
)
from ..models.admin_user_model import AdminUser
from ..utils.database_dependency import get_database_session
from ..services.auth_service import require_admin_user_service as require_admin_user
from ..utils.my_logger import get_logger

logger = get_logger("ADMIN_PERMISSION_ROUTES")

router = APIRouter(prefix="/permissions", tags=["Admin Permissions"])

@router.post("/", response_model=AdminPermissionResponse)
async def create_admin_permission_endpoint(
    permission_data: AdminPermissionCreate, 
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Create a new admin permission - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} creating new admin permission")
    return create_admin_permission(permission_data, db)

@router.get("/", response_model=List[AdminPermissionResponse])
async def get_admin_permissions_endpoint(
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Get all admin permissions - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} fetching all admin permissions")
    return get_all_admin_permissions(db)

@router.get("/{permission_id}", response_model=AdminPermissionResponse)
async def get_admin_permission_by_id_endpoint(
    permission_id: str,
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Get admin permission by ID - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} fetching admin permission {permission_id}")
    permission = get_admin_permission_by_id(permission_id, db)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )
    return permission

@router.get("/resource/{resource}", response_model=List[AdminPermissionResponse])
async def get_permissions_by_resource_endpoint(
    resource: str,
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Get permissions by resource - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} fetching permissions for resource {resource}")
    return get_permissions_by_resource(resource, db)

@router.put("/{permission_id}", response_model=AdminPermissionResponse)
async def update_admin_permission_endpoint(
    permission_id: str,
    permission_data: AdminPermissionUpdate,
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Update admin permission - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} updating admin permission {permission_id}")
    return update_admin_permission(permission_id, permission_data, db)

@router.delete("/{permission_id}")
async def delete_admin_permission_endpoint(
    permission_id: str,
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Delete admin permission - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} deleting admin permission {permission_id}")
    success = delete_admin_permission(permission_id, db)
    if success:
        return {"message": "Permission deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete permission"
        )

@router.patch("/{permission_id}/activate", response_model=AdminPermissionResponse)
async def activate_admin_permission_endpoint(
    permission_id: str,
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Activate admin permission - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} activating admin permission {permission_id}")
    return activate_permission(permission_id, db)

@router.patch("/{permission_id}/deactivate", response_model=AdminPermissionResponse)
async def deactivate_admin_permission_endpoint(
    permission_id: str,
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Deactivate admin permission - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} deactivating admin permission {permission_id}")
    return deactivate_permission(permission_id, db)
