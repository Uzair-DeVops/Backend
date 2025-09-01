"""
Enterprise Admin controller with functional approach - Using services
"""
from typing import Optional, List
from sqlmodel import Session
from fastapi import HTTPException, status

from ..models.enterprise_admin_model import (
    EnterpriseAdminCreate, EnterpriseAdminUpdate, EnterpriseAdminResponse, EnterpriseAdmin
)
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger
from ..services.enterprise_admin_service import (
    create_enterprise_admin_service,
    get_enterprise_admin_by_email_service,
    get_enterprise_admin_by_username_service,
    get_enterprise_admin_by_id_service,
    get_all_enterprise_admins_service,
    get_enterprise_admins_by_client_service,
    update_enterprise_admin_service,
    delete_enterprise_admin_service,
    activate_enterprise_admin_service,
    deactivate_enterprise_admin_service
)

logger = get_logger("ENTERPRISE_ADMIN_CONTROLLER")


def create_enterprise_admin(admin_data: EnterpriseAdminCreate, db: Session) -> EnterpriseAdminResponse:
    """Create a new enterprise admin"""
    try:
        return create_enterprise_admin_service(admin_data, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in create_enterprise_admin: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def get_enterprise_admin_by_email(email: str, db: Session) -> Optional[EnterpriseAdminResponse]:
    """Get enterprise admin by email"""
    try:
        return get_enterprise_admin_by_email_service(email, db)
    except Exception as e:
        logger.error(f"Controller error in get_enterprise_admin_by_email: {e}")
        return None


def get_enterprise_admin_by_username(username: str, db: Session) -> Optional[EnterpriseAdminResponse]:
    """Get enterprise admin by username"""
    try:
        return get_enterprise_admin_by_username_service(username, db)
    except Exception as e:
        logger.error(f"Controller error in get_enterprise_admin_by_username: {e}")
        return None


def get_enterprise_admin_by_id(admin_id: str, db: Session) -> Optional[EnterpriseAdminResponse]:
    """Get enterprise admin by ID"""
    try:
        return get_enterprise_admin_by_id_service(admin_id, db)
    except Exception as e:
        logger.error(f"Controller error in get_enterprise_admin_by_id: {e}")
        return None


def get_all_enterprise_admins(db: Session) -> List[EnterpriseAdminResponse]:
    """Get all enterprise admins"""
    try:
        return get_all_enterprise_admins_service(db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in get_all_enterprise_admins: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def get_enterprise_admins_by_client(enterprise_client_id: str, db: Session) -> List[EnterpriseAdminResponse]:
    """Get enterprise admins by enterprise client ID"""
    try:
        return get_enterprise_admins_by_client_service(enterprise_client_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in get_enterprise_admins_by_client: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def update_enterprise_admin(admin_id: str, admin_data: EnterpriseAdminUpdate, db: Session) -> EnterpriseAdminResponse:
    """Update enterprise admin"""
    try:
        return update_enterprise_admin_service(admin_id, admin_data, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in update_enterprise_admin: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def delete_enterprise_admin(admin_id: str, db: Session) -> bool:
    """Delete enterprise admin"""
    try:
        return delete_enterprise_admin_service(admin_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in delete_enterprise_admin: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def activate_enterprise_admin(admin_id: str, db: Session) -> EnterpriseAdminResponse:
    """Activate an enterprise admin"""
    try:
        return activate_enterprise_admin_service(admin_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in activate_enterprise_admin: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def deactivate_enterprise_admin(admin_id: str, db: Session) -> EnterpriseAdminResponse:
    """Deactivate an enterprise admin"""
    try:
        return deactivate_enterprise_admin_service(admin_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in deactivate_enterprise_admin: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
