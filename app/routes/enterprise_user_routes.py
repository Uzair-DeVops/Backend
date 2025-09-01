"""
Enterprise User routes for enterprise user management by enterprise admins
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Dict
from ..controllers.enterprise_user_controller import (
    create_enterprise_user,
    get_enterprise_user_by_id,
    get_all_enterprise_users,
    get_enterprise_users_by_client,
    get_enterprise_users_by_type,
    get_enterprise_users_by_creator,
    update_enterprise_user,
    delete_enterprise_user,
    activate_enterprise_user,
    deactivate_enterprise_user,
    update_enterprise_user_settings
)
from ..models.enterprise_user_model import (
    EnterpriseUserCreate, EnterpriseUserUpdate, EnterpriseUserResponse
)
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger

logger = get_logger("ENTERPRISE_USER_ROUTES")

router = APIRouter(prefix="/enterprise-users", tags=["Enterprise Users"])

@router.post("/", response_model=EnterpriseUserResponse)
async def create_enterprise_user_endpoint(
    user_data: EnterpriseUserCreate,
    db: Session = Depends(get_database_session)
):
    """Create a new enterprise user"""
    return create_enterprise_user(user_data, db)

@router.get("/", response_model=List[EnterpriseUserResponse])
async def get_enterprise_users_endpoint(
    db: Session = Depends(get_database_session)
):
    """Get all enterprise users"""
    return get_all_enterprise_users(db)

@router.get("/{user_id}", response_model=EnterpriseUserResponse)
async def get_enterprise_user_endpoint(
    user_id: str,
    db: Session = Depends(get_database_session)
):
    """Get enterprise user by ID"""
    user = get_enterprise_user_by_id(user_id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enterprise user not found"
        )
    return user

@router.get("/by-client/{enterprise_client_id}", response_model=List[EnterpriseUserResponse])
async def get_enterprise_users_by_client_endpoint(
    enterprise_client_id: str,
    db: Session = Depends(get_database_session)
):
    """Get enterprise users by enterprise client ID"""
    return get_enterprise_users_by_client(enterprise_client_id, db)

@router.get("/by-type/{user_type}/{enterprise_client_id}", response_model=List[EnterpriseUserResponse])
async def get_enterprise_users_by_type_endpoint(
    user_type: str,
    enterprise_client_id: str,
    db: Session = Depends(get_database_session)
):
    """Get enterprise users by user type for a specific enterprise client"""
    return get_enterprise_users_by_type(user_type, enterprise_client_id, db)

@router.get("/by-creator/{created_by}", response_model=List[EnterpriseUserResponse])
async def get_enterprise_users_by_creator_endpoint(
    created_by: str,
    db: Session = Depends(get_database_session)
):
    """Get enterprise users created by a specific enterprise admin"""
    return get_enterprise_users_by_creator(created_by, db)

@router.put("/{user_id}", response_model=EnterpriseUserResponse)
async def update_enterprise_user_endpoint(
    user_id: str,
    user_data: EnterpriseUserUpdate,
    db: Session = Depends(get_database_session)
):
    """Update enterprise user"""
    return update_enterprise_user(user_id, user_data, db)

@router.delete("/{user_id}")
async def delete_enterprise_user_endpoint(
    user_id: str,
    db: Session = Depends(get_database_session)
):
    """Delete enterprise user"""
    success = delete_enterprise_user(user_id, db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enterprise user not found"
        )
    return {"message": "Enterprise user deleted successfully"}

@router.patch("/{user_id}/activate", response_model=EnterpriseUserResponse)
async def activate_enterprise_user_endpoint(
    user_id: str,
    db: Session = Depends(get_database_session)
):
    """Activate an enterprise user"""
    return activate_enterprise_user(user_id, db)

@router.patch("/{user_id}/deactivate", response_model=EnterpriseUserResponse)
async def deactivate_enterprise_user_endpoint(
    user_id: str,
    db: Session = Depends(get_database_session)
):
    """Deactivate an enterprise user"""
    return deactivate_enterprise_user(user_id, db)

@router.patch("/{user_id}/settings", response_model=EnterpriseUserResponse)
async def update_enterprise_user_settings_endpoint(
    user_id: str,
    settings: Dict,
    db: Session = Depends(get_database_session)
):
    """Update enterprise user settings"""
    return update_enterprise_user_settings(user_id, settings, db)
