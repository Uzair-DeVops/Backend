"""
RBAC controller for role-scope assignments and role management
"""
from typing import Optional, List
from uuid import UUID
from sqlmodel import Session, select
from fastapi import HTTPException, status
from ..models.role_model import Role, RoleResponse
from ..models.scope_model import Scope, ScopeResponse
from ..models.role_scope_model import RoleScope, RoleScopeCreate, RoleScopeResponse
from ..models.user_role_model import UserRole, UserRoleResponse
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger

logger = get_logger("RBAC_CONTROLLER")

def assign_scope_to_role(role_id: UUID, scope_id: UUID, db: Session) -> bool:
    """Assign a scope to a role"""
    try:
        # Check if role exists
        role = get_role_by_id_internal(role_id, db)
        if not role:
            logger.warning(f"Scope assignment failed: role {role_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        # Check if scope exists
        scope = get_scope_by_id_internal(scope_id, db)
        if not scope:
            logger.warning(f"Scope assignment failed: scope {scope_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scope not found"
            )
        
        # Check if scope is already assigned
        existing_assignment = get_role_scope(role_id, scope_id, db)
        if existing_assignment:
            logger.warning(f"Scope assignment failed: scope {scope_id} already assigned to role {role_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Scope already assigned to role"
            )
        
        # Create scope assignment
        role_scope = RoleScope(
            role_id=role_id,
            scope_id=scope_id
        )
        
        db.add(role_scope)
        db.commit()
        
        logger.info(f"Scope {scope.name} assigned to role {role.name}")
        return True
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Scope assignment error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error assigning scope to role"
        )

def remove_scope_from_role(role_id: UUID, scope_id: UUID, db: Session) -> bool:
    """Remove a scope from a role"""
    try:
        # Check if assignment exists
        role_scope = get_role_scope(role_id, scope_id, db)
        if not role_scope:
            logger.warning(f"Scope removal failed: scope {scope_id} not assigned to role {role_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scope not assigned to role"
            )
        
        db.delete(role_scope)
        db.commit()
        
        logger.info(f"Scope removed from role {role_id}")
        return True
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Scope removal error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error removing scope from role"
        )

def get_role_scopes(role_id: UUID, db: Session) -> List[ScopeResponse]:
    """Get all scopes assigned to a role"""
    try:
        statement = select(Scope).join(RoleScope).where(RoleScope.role_id == role_id)
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
        logger.error(f"Error getting role scopes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving role scopes"
        )

def get_user_roles(user_id: UUID, db: Session) -> List[RoleResponse]:
    """Get all roles assigned to a user"""
    try:
        statement = select(Role).join(UserRole).where(UserRole.user_id == user_id)
        roles = db.exec(statement).all()
        
        return [
            RoleResponse(
                id=role.id,
                name=role.name,
                description=role.description,
                is_system_role=role.is_system_role,
                created_at=role.created_at,
                updated_at=role.updated_at
            )
            for role in roles
        ]
        
    except Exception as e:
        logger.error(f"Error getting user roles: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user roles"
        )

def get_user_scopes(user_id: UUID, db: Session) -> List[ScopeResponse]:
    """Get all scopes available to a user through their roles"""
    try:
        # Get all scopes from all roles assigned to the user
        statement = select(Scope).join(RoleScope).join(UserRole).where(UserRole.user_id == user_id)
        scopes = db.exec(statement).all()
        
        # Remove duplicates
        unique_scopes = {}
        for scope in scopes:
            if scope.id not in unique_scopes:
                unique_scopes[scope.id] = scope
        
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
            for scope in unique_scopes.values()
        ]
        
    except Exception as e:
        logger.error(f"Error getting user scopes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user scopes"
        )

def get_role_scope(role_id: UUID, scope_id: UUID, db: Session) -> Optional[RoleScope]:
    """Get role-scope assignment"""
    try:
        statement = select(RoleScope).where(
            RoleScope.role_id == role_id,
            RoleScope.scope_id == scope_id
        )
        return db.exec(statement).first()
    except Exception as e:
        logger.error(f"Error getting role scope: {e}")
        return None

def get_role_by_id_internal(role_id: UUID, db: Session) -> Optional[Role]:
    """Get role by ID (internal use)"""
    try:
        statement = select(Role).where(Role.id == role_id)
        return db.exec(statement).first()
    except Exception as e:
        logger.error(f"Error getting role by ID: {e}")
        return None

def get_scope_by_id_internal(scope_id: UUID, db: Session) -> Optional[Scope]:
    """Get scope by ID (internal use)"""
    try:
        statement = select(Scope).where(Scope.id == scope_id)
        return db.exec(statement).first()
    except Exception as e:
        logger.error(f"Error getting scope by ID: {e}")
        return None
