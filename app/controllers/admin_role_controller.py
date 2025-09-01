"""
Admin Role controller with functional approach - Using services
"""
from typing import Optional, List
from sqlmodel import Session
from fastapi import HTTPException, status

from ..models.admin_role_model import (
    AdminRoleCreate, AdminRoleUpdate, AdminRoleResponse, AdminRole  
)
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger
from ..services.admin_role_service import (
    create_admin_role_service,
    get_admin_role_by_name_service,
    get_admin_role_by_id_service,
    get_all_admin_roles_service,
    update_admin_role_service,
    delete_admin_role_service,
    activate_role_service,
    deactivate_role_service
)

logger = get_logger("ADMIN_ROLE_CONTROLLER")


def create_admin_role(role_data: AdminRoleCreate, db: Session) -> AdminRoleResponse:
    """Create a new admin role"""
    try:
        return create_admin_role_service(role_data, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in create_admin_role: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def get_admin_role_by_name(role_name: str, db: Session) -> Optional[AdminRoleResponse]:
    """Get admin role by name"""
    try:
        return get_admin_role_by_name_service(role_name, db)
    except Exception as e:
        logger.error(f"Controller error in get_admin_role_by_name: {e}")
        return None


def get_admin_role_by_id(role_id: str, db: Session) -> Optional[AdminRoleResponse]:
    """Get admin role by ID"""
    try:
        return get_admin_role_by_id_service(role_id, db)
    except Exception as e:
        logger.error(f"Controller error in get_admin_role_by_id: {e}")
        return None


def get_all_admin_roles(db: Session) -> List[AdminRoleResponse]:
    """Get all admin roles"""
    try:
        return get_all_admin_roles_service(db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in get_all_admin_roles: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def update_admin_role(role_id: str, role_data: AdminRoleUpdate, db: Session) -> AdminRoleResponse:
    """Update admin role"""
    try:
        return update_admin_role_service(role_id, role_data, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in update_admin_role: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def delete_admin_role(role_id: str, db: Session) -> bool:
    """Delete admin role"""
    try:
        return delete_admin_role_service(role_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in delete_admin_role: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def activate_role(role_id: str, db: Session) -> AdminRoleResponse:
    """Activate a role"""
    try:
        return activate_role_service(role_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in activate_role: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def deactivate_role(role_id: str, db: Session) -> AdminRoleResponse:
    """Deactivate a role"""
    try:
        return deactivate_role_service(role_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in deactivate_role: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
