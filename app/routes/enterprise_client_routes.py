"""
Enterprise Client routes for enterprise management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Dict
from ..controllers.enterprise_client_controller import (
    create_enterprise_client,
    get_enterprise_client_by_id,
    get_all_enterprise_clients,
    update_enterprise_client,
    delete_enterprise_client,
    activate_enterprise_client,
    deactivate_enterprise_client,
    update_client_settings
)
from ..models.enterprise_client_model import (
    EnterpriseClientCreate, EnterpriseClientUpdate, EnterpriseClientResponse
)
from ..models.admin_user_model import AdminUser
from ..utils.database_dependency import get_database_session
from ..services.auth_service import require_admin_user_service as require_admin_user
from ..utils.my_logger import get_logger

logger = get_logger("ENTERPRISE_CLIENT_ROUTES")

router = APIRouter(prefix="/enterprise-clients", tags=["Enterprise Clients"])

@router.post("/", response_model=EnterpriseClientResponse)
async def create_enterprise_client_endpoint(
    client_data: EnterpriseClientCreate,
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Create a new enterprise client - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} creating new enterprise client")
    return create_enterprise_client(client_data, db)

@router.get("/", response_model=List[EnterpriseClientResponse])
async def get_enterprise_clients_endpoint(
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Get all enterprise clients - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} fetching all enterprise clients")
    return get_all_enterprise_clients(db)

@router.get("/{client_id}", response_model=EnterpriseClientResponse)
async def get_enterprise_client_endpoint(
    client_id: str,
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Get enterprise client by ID - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} fetching enterprise client {client_id}")
    client = get_enterprise_client_by_id(client_id, db)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enterprise client not found"
        )
    return client

@router.put("/{client_id}", response_model=EnterpriseClientResponse)
async def update_enterprise_client_endpoint(
    client_id: str,
    client_data: EnterpriseClientUpdate,
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Update enterprise client - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} updating enterprise client {client_id}")
    return update_enterprise_client(client_id, client_data, db)

@router.patch("/{client_id}/activate", response_model=EnterpriseClientResponse)
async def activate_enterprise_client_endpoint(
    client_id: str,
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Activate an enterprise client - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} activating enterprise client {client_id}")
    return activate_enterprise_client(client_id, db)

@router.patch("/{client_id}/deactivate", response_model=EnterpriseClientResponse)
async def deactivate_enterprise_client_endpoint(
    client_id: str,
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Deactivate an enterprise client - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} deactivating enterprise client {client_id}")
    return deactivate_enterprise_client(client_id, db)

@router.patch("/{client_id}/settings", response_model=EnterpriseClientResponse)
async def update_enterprise_client_settings_endpoint(
    client_id: str,
    settings: Dict,
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Update enterprise client settings - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} updating settings for enterprise client {client_id}")
    return update_client_settings(client_id, settings, db)

@router.delete("/{client_id}")
async def delete_enterprise_client_endpoint(
    client_id: str,
    db: Session = Depends(get_database_session),
    current_user: AdminUser = Depends(require_admin_user)
):
    """Delete enterprise client - Requires admin authentication"""
    logger.info(f"Admin user {current_user.email} deleting enterprise client {client_id}")
    success = delete_enterprise_client(client_id, db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enterprise client not found"
        )
    return {"message": "Enterprise client deleted successfully"}
