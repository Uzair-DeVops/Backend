"""
RBAC routes for role-scope assignments and user role management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from uuid import UUID
from ..controllers.rbac_controller import (
    assign_scope_to_role,
    remove_scope_from_role,
    get_role_scopes,
    get_user_roles,
    get_user_scopes
)
from ..controllers.user_controller import assign_role_to_user
from ..models.role_model import RoleResponse
from ..models.scope_model import ScopeResponse
from ..models.user_model import UserCreate
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger
from ..controllers.user_controller import get_current_user

logger = get_logger("RBAC_ROUTES")

router = APIRouter(tags=["RBAC"])

# Role-Scope Management
@router.post("/roles/{role_id}/scopes/{scope_id}")
async def assign_scope_to_role_endpoint(
    role_id: str,
    scope_id: str,
    db: Session = Depends(get_database_session)
):
    """Assign a scope to a role"""
    try:
        role_uuid = UUID(role_id)
        scope_uuid = UUID(scope_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format"
        )
    
    success = assign_scope_to_role(role_uuid, scope_uuid, db)
    if success:
        return {"message": "Scope assigned to role successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to assign scope to role"
        )

@router.delete("/roles/{role_id}/scopes/{scope_id}")
async def remove_scope_from_role_endpoint(
    role_id: str,
    scope_id: str,
    db: Session = Depends(get_database_session)
):
    """Remove a scope from a role"""
    try:
        role_uuid = UUID(role_id)
        scope_uuid = UUID(scope_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format"
        )
    
    success = remove_scope_from_role(role_uuid, scope_uuid, db)
    if success:
        return {"message": "Scope removed from role successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove scope from role"
        )

@router.get("/roles/{role_id}/scopes", response_model=List[ScopeResponse])
async def get_role_scopes_endpoint(
    role_id: str,
    db: Session = Depends(get_database_session)
):
    """Get all scopes assigned to a role"""
    try:
        role_uuid = UUID(role_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format"
        )
    
    return get_role_scopes(role_uuid, db)

# User-Role Management
@router.post("/users/{user_id}/roles/{role_id}")
async def assign_role_to_user_endpoint(
    user_id: str,
    role_id: str,
    current_user: UserCreate = Depends(get_current_user),
    db: Session = Depends(get_database_session)
):
    """Assign a role to a user"""
    try:
        user_uuid = UUID(user_id)
        role_uuid = UUID(role_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format"
        )
    
    success = assign_role_to_user(user_uuid, role_uuid, current_user.id, db)
    if success:
        return {"message": "Role assigned to user successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to assign role to user"
        )

@router.get("/users/{user_id}/roles", response_model=List[RoleResponse])
async def get_user_roles_endpoint(
    user_id: str,
    db: Session = Depends(get_database_session)
):
    """Get all roles assigned to a user"""
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format"
        )
    
    return get_user_roles(user_uuid, db)

@router.get("/users/{user_id}/scopes", response_model=List[ScopeResponse])
async def get_user_scopes_endpoint(
    user_id: str,
    db: Session = Depends(get_database_session)
):
    """Get all scopes available to a user through their roles"""
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format"
        )
    
    return get_user_scopes(user_uuid, db)
