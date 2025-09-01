"""
Admin User controller with functional approach - Using services
"""
from typing import Optional, List
from sqlmodel import Session
from fastapi import HTTPException, status

from ..models.admin_user_model import (
    AdminUserCreate, AdminUserUpdate, AdminUserResponse, AdminUser
)
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger
from ..services.admin_user_service import (
    create_admin_user_service,
    get_admin_user_by_email_service,
    get_admin_user_by_username_service,
    get_admin_user_by_id_service,
    get_all_admin_users_service,
    update_admin_user_service,
    delete_admin_user_service,
    activate_user_service,
    deactivate_user_service
)

logger = get_logger("ADMIN_USER_CONTROLLER")


def create_admin_user(user_data: AdminUserCreate, db: Session) -> AdminUserResponse:
    """Create a new admin user"""
    try:
        return create_admin_user_service(user_data, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in create_admin_user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def get_admin_user_by_email(email: str, db: Session) -> Optional[AdminUserResponse]:
    """Get admin user by email"""
    try:
        return get_admin_user_by_email_service(email, db)
    except Exception as e:
        logger.error(f"Controller error in get_admin_user_by_email: {e}")
        return None


def get_admin_user_by_username(username: str, db: Session) -> Optional[AdminUserResponse]:
    """Get admin user by username"""
    try:
        return get_admin_user_by_username_service(username, db)
    except Exception as e:
        logger.error(f"Controller error in get_admin_user_by_username: {e}")
        return None


def get_admin_user_by_id(user_id: str, db: Session) -> Optional[AdminUserResponse]:
    """Get admin user by ID"""
    try:
        return get_admin_user_by_id_service(user_id, db)
    except Exception as e:
        logger.error(f"Controller error in get_admin_user_by_id: {e}")
        return None


def get_all_admin_users(db: Session) -> List[AdminUserResponse]:
    """Get all admin users"""
    try:
        return get_all_admin_users_service(db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in get_all_admin_users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def update_admin_user(user_id: str, user_data: AdminUserUpdate, db: Session) -> AdminUserResponse:
    """Update admin user"""
    try:
        return update_admin_user_service(user_id, user_data, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in update_admin_user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def delete_admin_user(user_id: str, db: Session) -> bool:
    """Delete admin user"""
    try:
        return delete_admin_user_service(user_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in delete_admin_user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def activate_user(user_id: str, db: Session) -> AdminUserResponse:
    """Activate a user account"""
    try:
        return activate_user_service(user_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in activate_user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def deactivate_user(user_id: str, db: Session) -> AdminUserResponse:
    """Deactivate a user account"""
    try:
        return deactivate_user_service(user_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in deactivate_user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
