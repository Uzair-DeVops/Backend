"""
Enterprise Permission routes for enterprise permission management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from ..controllers.enterprise_permission_controller import (
    create_enterprise_permission,
    get_enterprise_permission_by_id,
    get_all_enterprise_permissions,
    get_enterprise_permissions_by_client,
    get_enterprise_permissions_by_resource,
    update_enterprise_permission,
    delete_enterprise_permission,
    activate_enterprise_permission,
    deactivate_enterprise_permission
)
from ..models.enterprise_permission_model import (
    EnterprisePermissionCreate, EnterprisePermissionUpdate, EnterprisePermissionResponse
)
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger

logger = get_logger("ENTERPRISE_PERMISSION_ROUTES")

router = APIRouter(prefix="/enterprise-permissions", tags=["Enterprise Permissions"])

@router.post("/", response_model=EnterprisePermissionResponse)
async def create_enterprise_permission_endpoint(
    permission_data: EnterprisePermissionCreate,
    db: Session = Depends(get_database_session)
):
    """Create a new enterprise permission"""
    return create_enterprise_permission(permission_data, db)

@router.get("/", response_model=List[EnterprisePermissionResponse])
async def get_enterprise_permissions_endpoint(
    db: Session = Depends(get_database_session)
):
    """Get all enterprise permissions"""
    return get_all_enterprise_permissions(db)

@router.get("/{permission_id}", response_model=EnterprisePermissionResponse)
async def get_enterprise_permission_endpoint(
    permission_id: str,
    db: Session = Depends(get_database_session)
):
    """Get enterprise permission by ID"""
    permission = get_enterprise_permission_by_id(permission_id, db)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enterprise permission not found"
        )
    return permission

@router.get("/by-client/{enterprise_client_id}", response_model=List[EnterprisePermissionResponse])
async def get_enterprise_permissions_by_client_endpoint(
    enterprise_client_id: str,
    db: Session = Depends(get_database_session)
):
    """Get enterprise permissions by enterprise client ID"""
    return get_enterprise_permissions_by_client(enterprise_client_id, db)

@router.get("/by-resource/{resource}/{enterprise_client_id}", response_model=List[EnterprisePermissionResponse])
async def get_enterprise_permissions_by_resource_endpoint(
    resource: str,
    enterprise_client_id: str,
    db: Session = Depends(get_database_session)
):
    """Get enterprise permissions by resource for a specific enterprise client"""
    return get_enterprise_permissions_by_resource(resource, enterprise_client_id, db)

@router.put("/{permission_id}", response_model=EnterprisePermissionResponse)
async def update_enterprise_permission_endpoint(
    permission_id: str,
    permission_data: EnterprisePermissionUpdate,
    db: Session = Depends(get_database_session)
):
    """Update enterprise permission"""
    return update_enterprise_permission(permission_id, permission_data, db)

@router.delete("/{permission_id}")
async def delete_enterprise_permission_endpoint(
    permission_id: str,
    db: Session = Depends(get_database_session)
):
    """Delete enterprise permission"""
    success = delete_enterprise_permission(permission_id, db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enterprise permission not found"
        )
    return {"message": "Enterprise permission deleted successfully"}

@router.patch("/{permission_id}/activate", response_model=EnterprisePermissionResponse)
async def activate_enterprise_permission_endpoint(
    permission_id: str,
    db: Session = Depends(get_database_session)
):
    """Activate an enterprise permission"""
    return activate_enterprise_permission(permission_id, db)

@router.patch("/{permission_id}/deactivate", response_model=EnterprisePermissionResponse)
async def deactivate_enterprise_permission_endpoint(
    permission_id: str,
    db: Session = Depends(get_database_session)
):
    """Deactivate an enterprise permission"""
    return deactivate_enterprise_permission(permission_id, db)
