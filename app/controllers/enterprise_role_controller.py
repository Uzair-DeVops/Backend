"""
Enterprise Role controller with functional approach - Using services
"""
from typing import Optional, List
from sqlmodel import Session
from fastapi import HTTPException, status

from ..models.enterprise_role_model import (
    EnterpriseRoleCreate, EnterpriseRoleUpdate, EnterpriseRoleResponse, EnterpriseRole
)
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger
from ..services.enterprise_role_service import (
    create_enterprise_role_service,
    get_enterprise_role_by_name_service,
    get_enterprise_role_by_id_service,
    get_all_enterprise_roles_service,
    get_enterprise_roles_by_client_service,
    update_enterprise_role_service,
    delete_enterprise_role_service,
    activate_enterprise_role_service,
    deactivate_enterprise_role_service
)

logger = get_logger("ENTERPRISE_ROLE_CONTROLLER")


def create_enterprise_role(role_data: EnterpriseRoleCreate, db: Session) -> EnterpriseRoleResponse:
    """Create a new enterprise role"""
    try:
        return create_enterprise_role_service(role_data, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in create_enterprise_role: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def get_enterprise_role_by_name(name: str, enterprise_client_id: str, db: Session) -> Optional[EnterpriseRoleResponse]:
    """Get enterprise role by name for a specific enterprise client"""
    try:
        return get_enterprise_role_by_name_service(name, enterprise_client_id, db)
    except Exception as e:
        logger.error(f"Controller error in get_enterprise_role_by_name: {e}")
        return None


def get_enterprise_role_by_id(role_id: str, db: Session) -> Optional[EnterpriseRoleResponse]:
    """Get enterprise role by ID"""
    try:
        return get_enterprise_role_by_id_service(role_id, db)
    except Exception as e:
        logger.error(f"Controller error in get_enterprise_role_by_id: {e}")
        return None


def get_all_enterprise_roles(db: Session) -> List[EnterpriseRoleResponse]:
    """Get all enterprise roles"""
    try:
        return get_all_enterprise_roles_service(db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in get_all_enterprise_roles: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def get_enterprise_roles_by_client(enterprise_client_id: str, db: Session) -> List[EnterpriseRoleResponse]:
    """Get enterprise roles by enterprise client ID"""
    try:
        return get_enterprise_roles_by_client_service(enterprise_client_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in get_enterprise_roles_by_client: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def update_enterprise_role(role_id: str, role_data: EnterpriseRoleUpdate, db: Session) -> EnterpriseRoleResponse:
    """Update enterprise role"""
    try:
        return update_enterprise_role_service(role_id, role_data, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in update_enterprise_role: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def delete_enterprise_role(role_id: str, db: Session) -> bool:
    """Delete enterprise role"""
    try:
        return delete_enterprise_role_service(role_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in delete_enterprise_role: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def activate_enterprise_role(role_id: str, db: Session) -> EnterpriseRoleResponse:
    """Activate an enterprise role"""
    try:
        return activate_enterprise_role_service(role_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in activate_enterprise_role: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def deactivate_enterprise_role(role_id: str, db: Session) -> EnterpriseRoleResponse:
    """Deactivate an enterprise role"""
    try:
        return deactivate_enterprise_role_service(role_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in deactivate_enterprise_role: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
