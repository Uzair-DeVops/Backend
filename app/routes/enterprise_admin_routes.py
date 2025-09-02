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
from ..models.admin_user_model import AdminUser
from ..utils.database_dependency import get_database_session
from ..services.auth_service import require_admin_user_service as require_admin_user
from ..utils.my_logger import get_logger

logger = get_logger("ENTERPRISE_ADMIN_ROUTES")

router = APIRouter(prefix="/enterprise-admins", tags=["Enterprise Admins"])

@router.post("/", response_model=EnterpriseAdminResponse)
async def create_enterprise_admin_endpoint(
    admin_data: EnterpriseAdminCreate,
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Create a new enterprise admin - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} creating new enterprise admin")
    return create_enterprise_admin(admin_data, db)

@router.get("/", response_model=List[EnterpriseAdminResponse])
async def get_enterprise_admins_endpoint(
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Get all enterprise admins - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} fetching all enterprise admins")
    return get_all_enterprise_admins(db)

@router.get("/{admin_id}", response_model=EnterpriseAdminResponse)
async def get_enterprise_admin_endpoint(
    admin_id: str,
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Get enterprise admin by ID - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} fetching enterprise admin {admin_id}")
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
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Get enterprise admins by enterprise client ID - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} fetching enterprise admins for client {enterprise_client_id}")
    return get_enterprise_admins_by_client(enterprise_client_id, db)

@router.put("/{admin_id}", response_model=EnterpriseAdminResponse)
async def update_enterprise_admin_endpoint(
    admin_id: str,
    admin_data: EnterpriseAdminUpdate,
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Update enterprise admin - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} updating enterprise admin {admin_id}")
    return update_enterprise_admin(admin_id, admin_data, db)

@router.delete("/{admin_id}")
async def delete_enterprise_admin_endpoint(
    admin_id: str,
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Delete enterprise admin - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} deleting enterprise admin {admin_id}")
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
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Activate an enterprise admin - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} activating enterprise admin {admin_id}")
    return activate_enterprise_admin(admin_id, db)

@router.patch("/{admin_id}/deactivate", response_model=EnterpriseAdminResponse)
async def deactivate_enterprise_admin_endpoint(
    admin_id: str,
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Deactivate an enterprise admin - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} deactivating enterprise admin {admin_id}")
    return deactivate_enterprise_admin(admin_id, db)
