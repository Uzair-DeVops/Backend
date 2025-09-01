"""
Scope controller with functional approach for RBAC permission management
"""
from typing import Optional, List
from uuid import UUID
from sqlmodel import Session, select
from fastapi import HTTPException, status
from ..models.scope_model import Scope, ScopeCreate, ScopeUpdate, ScopeResponse
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger

logger = get_logger("SCOPE_CONTROLLER")

def create_scope(scope_data: ScopeCreate, db: Session) -> ScopeResponse:
    """Create a new scope"""
    try:
        # Check if scope name already exists
        existing_scope = get_scope_by_name(scope_data.name, db)
        if existing_scope:
            logger.warning(f"Scope creation failed: name {scope_data.name} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Scope name already exists"
            )
        
        # Create scope object
        scope = Scope(
            name=scope_data.name,
            description=scope_data.description,
            resource=scope_data.resource,
            action=scope_data.action
        )
        
        # Save to database
        db.add(scope)
        db.commit()
        db.refresh(scope)
        
        logger.info(f"Scope created successfully: {scope.name}")
        
        return ScopeResponse(
            id=scope.id,
            name=scope.name,
            description=scope.description,
            resource=scope.resource,
            action=scope.action,
            created_at=scope.created_at,
            updated_at=scope.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Scope creation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating scope"
        )

def get_scope_by_id(scope_id: str, db: Session) -> Optional[ScopeResponse]:
    """Get scope by ID"""
    try:
        # Convert string to UUID
        scope_uuid = UUID(scope_id)
        statement = select(Scope).where(Scope.id == scope_uuid)
        scope = db.exec(statement).first()
        
        if not scope:
            return None
        
        return ScopeResponse(
            id=scope.id,
            name=scope.name,
            description=scope.description,
            resource=scope.resource,
            action=scope.action,
            created_at=scope.created_at,
            updated_at=scope.updated_at
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        return None
    except Exception as e:
        logger.error(f"Error getting scope by ID: {e}")
        return None

def get_scope_by_name(scope_name: str, db: Session) -> Optional[Scope]:
    """Get scope by name"""
    try:
        statement = select(Scope).where(Scope.name == scope_name)
        return db.exec(statement).first()
    except Exception as e:
        logger.error(f"Error getting scope by name: {e}")
        return None

def get_all_scopes(db: Session) -> List[ScopeResponse]:
    """Get all scopes"""
    try:
        statement = select(Scope)
        scopes = db.exec(statement).all()
        
        return [
            ScopeResponse(
                id=scope.id,
                name=scope.name,
                description=scope.description,
                resource=scope.resource,
                action=scope.action,
                created_at=scope.created_at,
                updated_at=scope.updated_at
            )
            for scope in scopes
        ]
        
    except Exception as e:
        logger.error(f"Error getting all scopes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving scopes"
        )

def update_scope(scope_id: str, scope_data: ScopeUpdate, db: Session) -> ScopeResponse:
    """Update scope information"""
    try:
        # Convert string to UUID
        scope_uuid = UUID(scope_id)
        statement = select(Scope).where(Scope.id == scope_uuid)
        scope = db.exec(statement).first()
        
        if not scope:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scope not found"
            )
        
        # Check if new name already exists (if name is being updated)
        if scope_data.name and scope_data.name != scope.name:
            existing_scope = get_scope_by_name(scope_data.name, db)
            if existing_scope:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Scope name already exists"
                )
        
        # Update fields
        for field, value in scope_data.dict(exclude_unset=True).items():
            if hasattr(scope, field) and field != "id":
                setattr(scope, field, value)
        
        # Update timestamp
        from datetime import datetime
        scope.updated_at = datetime.utcnow()
        
        db.add(scope)
        db.commit()
        db.refresh(scope)
        
        logger.info(f"Scope updated successfully: {scope.name}")
        
        return ScopeResponse(
            id=scope.id,
            name=scope.name,
            description=scope.description,
            resource=scope.resource,
            action=scope.action,
            created_at=scope.created_at,
            updated_at=scope.updated_at
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid scope ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Scope update error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating scope"
        )

def delete_scope(scope_id: str, db: Session) -> bool:
    """Delete scope"""
    try:
        # Convert string to UUID
        scope_uuid = UUID(scope_id)
        statement = select(Scope).where(Scope.id == scope_uuid)
        scope = db.exec(statement).first()
        
        if not scope:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scope not found"
            )
        
        db.delete(scope)
        db.commit()
        
        logger.info(f"Scope deleted successfully: {scope.name}")
        return True
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid scope ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Scope deletion error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting scope"
        ) 