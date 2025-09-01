"""
Scope routes for RBAC system
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from ..controllers.scope_controller import (
    create_scope,
    get_scope_by_id,
    get_all_scopes,
    update_scope,
    delete_scope
)
from ..models.scope_model import ScopeCreate, ScopeUpdate, ScopeResponse
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger

logger = get_logger("SCOPE_ROUTES")

router = APIRouter( tags=["Scopes"])

@router.post("/", response_model=ScopeResponse)
async def create_scope_endpoint(
    scope_data: ScopeCreate,
    db: Session = Depends(get_database_session)
):
    """Create a new scope"""
    return create_scope(scope_data, db)

@router.get("/", response_model=List[ScopeResponse])
async def get_scopes_endpoint(
    db: Session = Depends(get_database_session)
):
    """Get all scopes"""
    return get_all_scopes(db)

@router.get("/{scope_id}", response_model=ScopeResponse)
async def get_scope_endpoint(
    scope_id: str,
    db: Session = Depends(get_database_session)
):
    """Get scope by ID"""
    scope = get_scope_by_id(scope_id, db)
    if not scope:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scope not found"
        )
    return scope

@router.put("/{scope_id}", response_model=ScopeResponse)
async def update_scope_endpoint(
    scope_id: str,
    scope_data: ScopeUpdate,
    db: Session = Depends(get_database_session)
):
    """Update scope"""
    return update_scope(scope_id, scope_data, db)

@router.delete("/{scope_id}")
async def delete_scope_endpoint(
    scope_id: str,
    db: Session = Depends(get_database_session)
):
    """Delete scope"""
    success = delete_scope(scope_id, db)
    if success:
        return {"message": "Scope deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete scope"
        )
