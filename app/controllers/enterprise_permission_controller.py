"""
Enterprise Permission controller with functional approach - Using services
"""
from typing import Optional, List
from sqlmodel import Session
from fastapi import HTTPException, status

from ..models.enterprise_permission_model import (
    EnterprisePermissionCreate, EnterprisePermissionUpdate, EnterprisePermissionResponse, EnterprisePermission
)
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger
from ..services.enterprise_permission_service import (
    create_enterprise_permission_service,
    get_enterprise_permission_by_name_service,
    get_enterprise_permission_by_id_service,
    get_all_enterprise_permissions_service,
    get_enterprise_permissions_by_client_service,
    get_enterprise_permissions_by_resource_service,
    update_enterprise_permission_service,
    delete_enterprise_permission_service,
    activate_enterprise_permission_service,
    deactivate_enterprise_permission_service
)

logger = get_logger("ENTERPRISE_PERMISSION_CONTROLLER")


def create_enterprise_permission(permission_data: EnterprisePermissionCreate, db: Session) -> EnterprisePermissionResponse:
    """Create a new enterprise permission"""
    try:
        return create_enterprise_permission_service(permission_data, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in create_enterprise_permission: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def get_enterprise_permission_by_name(name: str, enterprise_client_id: str, db: Session) -> Optional[EnterprisePermissionResponse]:
    """Get enterprise permission by name for a specific enterprise client"""
    try:
        return get_enterprise_permission_by_name_service(name, enterprise_client_id, db)
    except Exception as e:
        logger.error(f"Controller error in get_enterprise_permission_by_name: {e}")
        return None


def get_enterprise_permission_by_id(permission_id: str, db: Session) -> Optional[EnterprisePermissionResponse]:
    """Get enterprise permission by ID"""
    try:
        return get_enterprise_permission_by_id_service(permission_id, db)
    except Exception as e:
        logger.error(f"Controller error in get_enterprise_permission_by_id: {e}")
        return None


def get_all_enterprise_permissions(db: Session) -> List[EnterprisePermissionResponse]:
    """Get all enterprise permissions"""
    try:
        return get_all_enterprise_permissions_service(db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in get_all_enterprise_permissions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def get_enterprise_permissions_by_client(enterprise_client_id: str, db: Session) -> List[EnterprisePermissionResponse]:
    """Get enterprise permissions by enterprise client ID"""
    try:
        return get_enterprise_permissions_by_client_service(enterprise_client_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in get_enterprise_permissions_by_client: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def get_enterprise_permissions_by_resource(resource: str, enterprise_client_id: str, db: Session) -> List[EnterprisePermissionResponse]:
    """Get enterprise permissions by resource for a specific enterprise client"""
    try:
        return get_enterprise_permissions_by_resource_service(resource, enterprise_client_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in get_enterprise_permissions_by_resource: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def update_enterprise_permission(permission_id: str, permission_data: EnterprisePermissionUpdate, db: Session) -> EnterprisePermissionResponse:
    """Update enterprise permission"""
    try:
        return update_enterprise_permission_service(permission_id, permission_data, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in update_enterprise_permission: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def delete_enterprise_permission(permission_id: str, db: Session) -> bool:
    """Delete enterprise permission"""
    try:
        return delete_enterprise_permission_service(permission_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in delete_enterprise_permission: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def activate_enterprise_permission(permission_id: str, db: Session) -> EnterprisePermissionResponse:
    """Activate an enterprise permission"""
    try:
        return activate_enterprise_permission_service(permission_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in activate_enterprise_permission: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def deactivate_enterprise_permission(permission_id: str, db: Session) -> EnterprisePermissionResponse:
    """Deactivate an enterprise permission"""
    try:
        return deactivate_enterprise_permission_service(permission_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in deactivate_enterprise_permission: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
