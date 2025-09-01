"""
Enterprise Role routes for enterprise role management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from ..controllers.enterprise_role_controller import (
    create_enterprise_role,
    get_enterprise_role_by_id,
    get_all_enterprise_roles,
    get_enterprise_roles_by_client,
    update_enterprise_role,
    delete_enterprise_role,
    activate_enterprise_role,
    deactivate_enterprise_role
)
from ..models.enterprise_role_model import (
    EnterpriseRoleCreate, EnterpriseRoleUpdate, EnterpriseRoleResponse
)
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger

logger = get_logger("ENTERPRISE_ROLE_ROUTES")

router = APIRouter(prefix="/enterprise-roles", tags=["Enterprise Roles"])

@router.post("/", response_model=EnterpriseRoleResponse)
async def create_enterprise_role_endpoint(
    role_data: EnterpriseRoleCreate,
    db: Session = Depends(get_database_session)
):
    """Create a new enterprise role"""
    return create_enterprise_role(role_data, db)

@router.get("/", response_model=List[EnterpriseRoleResponse])
async def get_enterprise_roles_endpoint(
    db: Session = Depends(get_database_session)
):
    """Get all enterprise roles"""
    return get_all_enterprise_roles(db)

@router.get("/{role_id}", response_model=EnterpriseRoleResponse)
async def get_enterprise_role_endpoint(
    role_id: str,
    db: Session = Depends(get_database_session)
):
    """Get enterprise role by ID"""
    role = get_enterprise_role_by_id(role_id, db)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enterprise role not found"
        )
    return role

@router.get("/by-client/{enterprise_client_id}", response_model=List[EnterpriseRoleResponse])
async def get_enterprise_roles_by_client_endpoint(
    enterprise_client_id: str,
    db: Session = Depends(get_database_session)
):
    """Get enterprise roles by enterprise client ID"""
    return get_enterprise_roles_by_client(enterprise_client_id, db)

@router.put("/{role_id}", response_model=EnterpriseRoleResponse)
async def update_enterprise_role_endpoint(
    role_id: str,
    role_data: EnterpriseRoleUpdate,
    db: Session = Depends(get_database_session)
):
    """Update enterprise role"""
    return update_enterprise_role(role_id, role_data, db)

@router.delete("/{role_id}")
async def delete_enterprise_role_endpoint(
    role_id: str,
    db: Session = Depends(get_database_session)
):
    """Delete enterprise role"""
    success = delete_enterprise_role(role_id, db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enterprise role not found"
        )
    return {"message": "Enterprise role deleted successfully"}

@router.patch("/{role_id}/activate", response_model=EnterpriseRoleResponse)
async def activate_enterprise_role_endpoint(
    role_id: str,
    db: Session = Depends(get_database_session)
):
    """Activate an enterprise role"""
    return activate_enterprise_role(role_id, db)

@router.patch("/{role_id}/deactivate", response_model=EnterpriseRoleResponse)
async def deactivate_enterprise_role_endpoint(
    role_id: str,
    db: Session = Depends(get_database_session)
):
    """Deactivate an enterprise role"""
    return deactivate_enterprise_role(role_id, db)
