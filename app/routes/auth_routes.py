"""
Authentication routes for login functionality
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from ..controllers.auth_controller import (
    login_user,
    get_current_user
)
from ..models.auth_model import (
    LoginRequest,
    LoginResponse
)
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger

logger = get_logger("AUTH_ROUTES")

# Create router
auth_router = APIRouter()

@auth_router.post("/login", response_model=LoginResponse, tags=["Authentication"])
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_database_session)
):
    """Universal login endpoint for all user types"""
    return login_user(login_data, db)

@auth_router.get("/me", response_model=dict, tags=["Authentication"])
async def get_current_user_info(
    current_user = Depends(get_current_user)
):
    """Get current authenticated user information"""
    try:
        # Return user info based on user type
        if hasattr(current_user, 'username'):  # Admin user
            return {
                "user_id": str(current_user.id),
                "email": current_user.email,
                "username": current_user.username,
                "full_name": current_user.full_name,
                "user_type": "admin",
                "is_active": current_user.is_active
            }
        else:  # Enterprise client
            return {
                "user_id": str(current_user.id),
                "email": current_user.email,
                "name": current_user.name,
                "contact_person": current_user.contact_person,
                "user_type": "enterprise_client",
                "is_active": current_user.is_active
            }
    except Exception as e:
        logger.error(f"Error getting current user info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user information"
        )
