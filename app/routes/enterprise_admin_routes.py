"""
Enterprise Admin routes for enterprise admin management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from ..controllers.enterprise_admin_controller import (
    create_enterprise_admin,
    get_enterprise_admin_by_id,
    get_all_enterprise_admins,
    get_enterprise_admins_by_client,
    update_enterprise_admin,
    delete_enterprise_admin,
    activate_enterprise_admin,
    deactivate_enterprise_admin
)
from ..models.enterprise_admin_model import (
    EnterpriseAdminCreate, EnterpriseAdminUpdate, EnterpriseAdminResponse
)
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger

logger = get_logger("ENTERPRISE_ADMIN_ROUTES")

router = APIRouter(prefix="/enterprise-admins", tags=["Enterprise Admins"])

@router.post("/", response_model=EnterpriseAdminResponse)
async def create_enterprise_admin_endpoint(
    admin_data: EnterpriseAdminCreate,
    db: Session = Depends(get_database_session)
):
    """Create a new enterprise admin"""
    return create_enterprise_admin(admin_data, db)

@router.get("/", response_model=List[EnterpriseAdminResponse])
async def get_enterprise_admins_endpoint(
    db: Session = Depends(get_database_session)
):
    """Get all enterprise admins"""
    return get_all_enterprise_admins(db)

@router.get("/{admin_id}", response_model=EnterpriseAdminResponse)
async def get_enterprise_admin_endpoint(
    admin_id: str,
    db: Session = Depends(get_database_session)
):
    """Get enterprise admin by ID"""
    admin = get_enterprise_admin_by_id(admin_id, db)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enterprise admin not found"
        )
    return admin

@router.get("/by-client/{enterprise_client_id}", response_model=List[EnterpriseAdminResponse])
async def get_enterprise_admins_by_client_endpoint(
    enterprise_client_id: str,
    db: Session = Depends(get_database_session)
):
    """Get enterprise admins by enterprise client ID"""
    return get_enterprise_admins_by_client(enterprise_client_id, db)

@router.put("/{admin_id}", response_model=EnterpriseAdminResponse)
async def update_enterprise_admin_endpoint(
    admin_id: str,
    admin_data: EnterpriseAdminUpdate,
    db: Session = Depends(get_database_session)
):
    """Update enterprise admin"""
    return update_enterprise_admin(admin_id, admin_data, db)

@router.delete("/{admin_id}")
async def delete_enterprise_admin_endpoint(
    admin_id: str,
    db: Session = Depends(get_database_session)
):
    """Delete enterprise admin"""
    success = delete_enterprise_admin(admin_id, db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enterprise admin not found"
        )
    return {"message": "Enterprise admin deleted successfully"}

@router.patch("/{admin_id}/activate", response_model=EnterpriseAdminResponse)
async def activate_enterprise_admin_endpoint(
    admin_id: str,
    db: Session = Depends(get_database_session)
):
    """Activate an enterprise admin"""
    return activate_enterprise_admin(admin_id, db)

@router.patch("/{admin_id}/deactivate", response_model=EnterpriseAdminResponse)
async def deactivate_enterprise_admin_endpoint(
    admin_id: str,
    db: Session = Depends(get_database_session)
):
    """Deactivate an enterprise admin"""
    return deactivate_enterprise_admin(admin_id, db)
