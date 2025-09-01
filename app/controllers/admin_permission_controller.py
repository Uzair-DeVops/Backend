"""
Admin Permission controller with functional approach - Using services
from datetime import datetime
from typing import Optional, List
from sqlmodel import Session
from fastapi import HTTPException, status
"""
from typing import Optional, List
from sqlmodel import Session
from fastapi import HTTPException, status
from datetime import datetime # noqa: F401

from ..models.admin_permission_model import (
    AdminPermissionCreate, AdminPermissionUpdate, AdminPermissionResponse, AdminPermission
)
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger
from ..services.admin_permission_service import (
    create_admin_permission_service,
    get_admin_permission_by_name_service,
    get_admin_permission_by_id_service,
    get_all_admin_permissions_service,
    get_permissions_by_resource_service,
    update_admin_permission_service,
    delete_admin_permission_service,
    activate_permission_service,
    deactivate_permission_service
)

logger = get_logger("ADMIN_PERMISSION_CONTROLLER")


def create_admin_permission(permission_data: AdminPermissionCreate, db: Session) -> AdminPermissionResponse:
    """Create a new admin permission"""
    try:
        return create_admin_permission_service(permission_data, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in create_admin_permission: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def get_admin_permission_by_name(permission_name: str, db: Session) -> Optional[AdminPermissionResponse]:
    """Get admin permission by name"""
    try:
        return get_admin_permission_by_name_service(permission_name, db)
    except Exception as e:
        logger.error(f"Controller error in get_admin_permission_by_name: {e}")
        return None


def get_admin_permission_by_id(permission_id: str, db: Session) -> Optional[AdminPermissionResponse]:
    """Get admin permission by ID"""
    try:
        return get_admin_permission_by_id_service(permission_id, db)
    except Exception as e:
        logger.error(f"Controller error in get_admin_permission_by_id: {e}")
        return None


def get_all_admin_permissions(db: Session) -> List[AdminPermissionResponse]:
    """Get all admin permissions"""
    try:
        return get_all_admin_permissions_service(db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in get_all_admin_permissions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def get_permissions_by_resource(resource: str, db: Session) -> List[AdminPermissionResponse]:
    """Get permissions by resource"""
    try:
        return get_permissions_by_resource_service(resource, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in get_permissions_by_resource: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def update_admin_permission(permission_id: str, permission_data: AdminPermissionUpdate, db: Session) -> AdminPermissionResponse:
    """Update admin permission"""
    try:
        return update_admin_permission_service(permission_id, permission_data, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in update_admin_permission: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def delete_admin_permission(permission_id: str, db: Session) -> bool:
    """Delete admin permission"""
    try:
        return delete_admin_permission_service(permission_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in delete_admin_permission: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def activate_permission(permission_id: str, db: Session) -> AdminPermissionResponse:
    """Activate a permission"""
    try:
        return activate_permission_service(permission_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in activate_permission: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def deactivate_permission(permission_id: str, db: Session) -> AdminPermissionResponse:
    """Deactivate a permission"""
    try:
        return deactivate_permission_service(permission_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in deactivate_permission: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
