"""
Authentication controller with login functionality - Using services
"""
from typing import Optional
from sqlmodel import Session
from fastapi import HTTPException, status, Depends, Request

from ..models.auth_model import LoginRequest, LoginResponse
from ..models.admin_user_model import AdminUser
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger
from ..services.auth_service import (
    authenticate_user_service,
    login_user_service,
    get_current_user_service,
    refresh_token_service,
    logout_user_service,
    change_password_service
)

logger = get_logger("AUTH_CONTROLLER")


def authenticate_admin_user(email: str, password: str, db: Session) -> Optional[AdminUser]:
    """Authenticate admin user with email and password"""
    try:
        return authenticate_user_service(email, password, db)
    except Exception as e:
        logger.error(f"Controller error in authenticate_admin_user: {e}")
        return None


def login_user(login_data: LoginRequest, db: Session) -> LoginResponse:
    """Universal login endpoint for all user types"""
    try:
        # Use the service for login
        token = login_user_service(login_data.email, login_data.password, db)
        
        # Get user details for response
        user = authenticate_user_service(login_data.email, login_data.password, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Convert role_ids and permissions from JSON
        import json
        role_ids = json.loads(user.role_ids) if user.role_ids else []
        permissions = json.loads(user.permissions) if user.permissions else []
        
        return LoginResponse(
            access_token=token.access_token,
            token_type=token.token_type,
            user_id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            role_ids=role_ids,
            permissions=permissions,
            user_type="admin"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in login_user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def get_current_user(request: Request, db: Session = Depends(get_database_session)):
    """Get current authenticated user from JWT token"""
    try:
        return get_current_user_service(request, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in get_current_user: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def refresh_token(current_user: AdminUser):
    """Refresh access token for current user"""
    try:
        return refresh_token_service(current_user)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in refresh_token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def logout_user(current_user: AdminUser):
    """Logout user"""
    try:
        return logout_user_service(current_user)
    except Exception as e:
        logger.error(f"Controller error in logout_user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def change_password(
    current_user: AdminUser, 
    current_password: str, 
    new_password: str, 
    db: Session
):
    """Change user password"""
    try:
        return change_password_service(current_user, current_password, new_password, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Controller error in change_password: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
