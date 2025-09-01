"""
Admin User routes for user management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from ..controllers.admin_user_controller import (
    create_admin_user,
    get_admin_user_by_id,
    get_all_admin_users,
    update_admin_user,
    delete_admin_user,
    activate_user,
    deactivate_user
)
from ..models.admin_user_model import (
    AdminUserCreate, AdminUserUpdate, AdminUserResponse
)
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger

logger = get_logger("ADMIN_USER_ROUTES")

router = APIRouter(prefix="/users", tags=["Admin Users"])

@router.post("/", response_model=AdminUserResponse)
async def create_admin_user_endpoint(
    user_data: AdminUserCreate,
    db: Session = Depends(get_database_session)
):
    """Create a new admin user"""
    return create_admin_user(user_data, db)

@router.get("/", response_model=List[AdminUserResponse])
async def get_admin_users_endpoint(
    db: Session = Depends(get_database_session)
):
    """Get all admin users"""
    return get_all_admin_users(db)

@router.get("/{user_id}", response_model=AdminUserResponse)
async def get_admin_user_endpoint(
    user_id: str,
    db: Session = Depends(get_database_session)
):
    """Get admin user by ID"""
    user = get_admin_user_by_id(user_id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.put("/{user_id}", response_model=AdminUserResponse)
async def update_admin_user_endpoint(
    user_id: str,
    user_data: AdminUserUpdate,
    db: Session = Depends(get_database_session)
):
    """Update admin user"""
    return update_admin_user(user_id, user_data, db)

@router.patch("/{user_id}/activate", response_model=AdminUserResponse)
async def activate_admin_user_endpoint(
    user_id: str,
    db: Session = Depends(get_database_session)
):
    """Activate an admin user"""
    return activate_user(user_id, db)

@router.patch("/{user_id}/deactivate", response_model=AdminUserResponse)
async def deactivate_admin_user_endpoint(
    user_id: str,
    db: Session = Depends(get_database_session)
):
    """Deactivate an admin user"""
    return deactivate_user(user_id, db)

@router.delete("/{user_id}")
async def delete_admin_user_endpoint(
    user_id: str,
    db: Session = Depends(get_database_session)
):
    """Delete admin user"""
    success = delete_admin_user(user_id, db)
    if success:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        )
