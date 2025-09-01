"""
Enterprise User controller with functional approach - Using services
"""
from typing import Optional, List
from sqlmodel import Session
from fastapi import HTTPException, status

from ..models.enterprise_user_model import (
    EnterpriseUserCreate, EnterpriseUserUpdate, EnterpriseUserResponse, EnterpriseUser
)
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger
from ..services.enterprise_user_service import (
    create_enterprise_user_service,
    get_enterprise_user_by_email_service,
    get_enterprise_user_by_username_service,
    get_enterprise_user_by_id_service,
    get_all_enterprise_users_service,
    get_enterprise_users_by_client_service,
    get_enterprise_users_by_type_service,
    get_enterprise_users_by_creator_service,
    update_enterprise_user_service,
    delete_enterprise_user_service,
    verify_enterprise_user_password_service,
    activate_enterprise_user_service,
    deactivate_enterprise_user_service,
    update_enterprise_user_settings_service
)

logger = get_logger("ENTERPRISE_USER_CONTROLLER")


def create_enterprise_user(user_data: EnterpriseUserCreate, db: Session) -> EnterpriseUserResponse:
    """Create a new enterprise user"""
    try:
        return create_enterprise_user_service(user_data, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in create_enterprise_user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def get_enterprise_user_by_email(email: str, db: Session) -> Optional[EnterpriseUserResponse]:
    """Get enterprise user by email"""
    try:
        return get_enterprise_user_by_email_service(email, db)
    except Exception as e:
        logger.error(f"Controller error in get_enterprise_user_by_email: {e}")
        return None


def get_enterprise_user_by_username(username: str, db: Session) -> Optional[EnterpriseUserResponse]:
    """Get enterprise user by username"""
    try:
        return get_enterprise_user_by_username_service(username, db)
    except Exception as e:
        logger.error(f"Controller error in get_enterprise_user_by_username: {e}")
        return None


def get_enterprise_user_by_id(user_id: str, db: Session) -> Optional[EnterpriseUserResponse]:
    """Get enterprise user by ID"""
    try:
        return get_enterprise_user_by_id_service(user_id, db)
    except Exception as e:
        logger.error(f"Controller error in get_enterprise_user_by_id: {e}")
        return None


def get_all_enterprise_users(db: Session) -> List[EnterpriseUserResponse]:
    """Get all enterprise users"""
    try:
        return get_all_enterprise_users_service(db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in get_all_enterprise_users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def get_enterprise_users_by_client(enterprise_client_id: str, db: Session) -> List[EnterpriseUserResponse]:
    """Get enterprise users by enterprise client ID"""
    try:
        return get_enterprise_users_by_client_service(enterprise_client_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in get_enterprise_users_by_client: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def get_enterprise_users_by_type(user_type: str, enterprise_client_id: str, db: Session) -> List[EnterpriseUserResponse]:
    """Get enterprise users by user type for a specific enterprise client"""
    try:
        return get_enterprise_users_by_type_service(user_type, enterprise_client_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in get_enterprise_users_by_type: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def get_enterprise_users_by_creator(created_by: str, db: Session) -> List[EnterpriseUserResponse]:
    """Get enterprise users created by a specific enterprise admin"""
    try:
        return get_enterprise_users_by_creator_service(created_by, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in get_enterprise_users_by_creator: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def update_enterprise_user(user_id: str, user_data: EnterpriseUserUpdate, db: Session) -> EnterpriseUserResponse:
    """Update enterprise user"""
    try:
        return update_enterprise_user_service(user_id, user_data, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in update_enterprise_user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def delete_enterprise_user(user_id: str, db: Session) -> bool:
    """Delete enterprise user"""
    try:
        return delete_enterprise_user_service(user_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in delete_enterprise_user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def activate_enterprise_user(user_id: str, db: Session) -> EnterpriseUserResponse:
    """Activate an enterprise user"""
    try:
        return activate_enterprise_user_service(user_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in activate_enterprise_user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def deactivate_enterprise_user(user_id: str, db: Session) -> EnterpriseUserResponse:
    """Deactivate an enterprise user"""
    try:
        return deactivate_enterprise_user_service(user_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in deactivate_enterprise_user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def update_enterprise_user_settings(user_id: str, settings: dict, db: Session) -> EnterpriseUserResponse:
    """Update enterprise user settings"""
    try:
        return update_enterprise_user_settings_service(user_id, settings, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in update_enterprise_user_settings: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
