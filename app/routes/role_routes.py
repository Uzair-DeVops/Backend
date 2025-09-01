"""
Role routes for RBAC system
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from ..controllers.role_controller import (
    get_role_by_id,
    get_all_roles,
    update_role,
    delete_role,
    create_role_with_scopes
)
from ..models.role_model import RoleUpdate, RoleResponse, RoleCreateWithScopes
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger

logger = get_logger("ROLE_ROUTES")

router = APIRouter(tags=["Roles"])

@router.post("/create-with-scopes", response_model=RoleResponse)
async def create_role_with_scopes_endpoint(
    role_data: RoleCreateWithScopes,
    db: Session = Depends(get_database_session)
):
    """Create a new role with scope assignments"""
    return create_role_with_scopes(role_data, db)

@router.get("/", response_model=List[RoleResponse])
async def get_roles_endpoint(
    db: Session = Depends(get_database_session)
):
    """Get all roles"""
    return get_all_roles(db)

@router.get("/{role_id}", response_model=RoleResponse)
async def get_role_endpoint(
    role_id: str,
    db: Session = Depends(get_database_session)
):
    """Get role by ID"""
    role = get_role_by_id(role_id, db)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    return role

@router.put("/{role_id}", response_model=RoleResponse)
async def update_role_endpoint(
    role_id: str,
    role_data: RoleUpdate,
    db: Session = Depends(get_database_session)
):
    """Update role"""
    return update_role(role_id, role_data, db)

@router.delete("/{role_id}")
async def delete_role_endpoint(
    role_id: str,
    db: Session = Depends(get_database_session)
):
    """Delete role"""
    success = delete_role(role_id, db)
    if success:
        return {"message": "Role deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete role"
        )
