"""
Role controller with functional approach for RBAC role management
"""
from typing import Optional, List
from uuid import UUID
from sqlmodel import Session, select
from fastapi import HTTPException, status
from ..models.role_model import Role, RoleCreate, RoleUpdate, RoleResponse, RoleCreateWithScopes
from ..models.role_scope_model import RoleScope
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger

logger = get_logger("ROLE_CONTROLLER")

def create_role_with_scopes(role_data: RoleCreateWithScopes, db: Session) -> RoleResponse:
    """Create a new role with scope assignments"""
    try:
        # Check if role name already exists
        existing_role = get_role_by_name(role_data.name, db)
        if existing_role:
            logger.warning(f"Role creation failed: name {role_data.name} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role name already exists"
            )
        
        # Create role object
        role = Role(
            name=role_data.name,
            description=role_data.description,
            is_system_role=role_data.is_system_role
        )
        
        # Save to database
        db.add(role)
        db.commit()
        db.refresh(role)
        
        # Assign scopes to role
        for scope_id in role_data.scope_ids:
            try:
                role_scope = RoleScope(
                    role_id=role.id,
                    scope_id=scope_id
                )
                db.add(role_scope)
            except Exception as e:
                logger.warning(f"Failed to assign scope {scope_id} to role {role.name}: {e}")
        
        db.commit()
        
        logger.info(f"Role created successfully with scopes: {role.name}")
        
        return RoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            is_system_role=role.is_system_role,
            created_at=role.created_at,
            updated_at=role.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Role creation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating role"
        )

def create_role(role_data: RoleCreate, db: Session) -> RoleResponse:
    """Create a new role"""
    try:
        # Check if role name already exists
        existing_role = get_role_by_name(role_data.name, db)
        if existing_role:
            logger.warning(f"Role creation failed: name {role_data.name} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role name already exists"
            )
        
        # Create role object
        role = Role(
            name=role_data.name,
            description=role_data.description,
            is_system_role=role_data.is_system_role
        )
        
        # Save to database
        db.add(role)
        db.commit()
        db.refresh(role)
        
        logger.info(f"Role created successfully: {role.name}")
        
        return RoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            is_system_role=role.is_system_role,
            created_at=role.created_at,
            updated_at=role.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Role creation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating role"
        )

def get_role_by_id(role_id: str, db: Session) -> Optional[RoleResponse]:
    """Get role by ID"""
    try:
        # Convert string to UUID
        role_uuid = UUID(role_id)
        statement = select(Role).where(Role.id == role_uuid)
        role = db.exec(statement).first()
        
        if not role:
            return None
        
        return RoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            is_system_role=role.is_system_role,
            created_at=role.created_at,
            updated_at=role.updated_at
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        return None
    except Exception as e:
        logger.error(f"Error getting role by ID: {e}")
        return None

def get_role_by_name(role_name: str, db: Session) -> Optional[Role]:
    """Get role by name"""
    try:
        statement = select(Role).where(Role.name == role_name)
        return db.exec(statement).first()
    except Exception as e:
        logger.error(f"Error getting role by name: {e}")
        return None

def get_all_roles(db: Session) -> List[RoleResponse]:
    """Get all roles"""
    try:
        statement = select(Role)
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
        logger.error(f"Error getting all roles: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving roles"
        )

def update_role(role_id: str, role_data: RoleUpdate, db: Session) -> RoleResponse:
    """Update role information"""
    try:
        # Convert string to UUID
        role_uuid = UUID(role_id)
        statement = select(Role).where(Role.id == role_uuid)
        role = db.exec(statement).first()
        
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        # Prevent updating system roles
        if role.is_system_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot update system roles"
            )
        
        # Check if new name already exists (if name is being updated)
        if role_data.name and role_data.name != role.name:
            existing_role = get_role_by_name(role_data.name, db)
            if existing_role:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Role name already exists"
                )
        
        # Update fields
        for field, value in role_data.dict(exclude_unset=True).items():
            if hasattr(role, field) and field != "id":
                setattr(role, field, value)
        
        # Update timestamp
        from datetime import datetime
        role.updated_at = datetime.utcnow()
        
        db.add(role)
        db.commit()
        db.refresh(role)
        
        logger.info(f"Role updated successfully: {role.name}")
        
        return RoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            is_system_role=role.is_system_role,
            created_at=role.created_at,
            updated_at=role.updated_at
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Role update error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating role"
        )

def delete_role(role_id: str, db: Session) -> bool:
    """Delete role"""
    try:
        # Convert string to UUID
        role_uuid = UUID(role_id)
        statement = select(Role).where(Role.id == role_uuid)
        role = db.exec(statement).first()
        
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        # Prevent deleting system roles
        if role.is_system_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete system roles"
            )
        
        db.delete(role)
        db.commit()
        
        logger.info(f"Role deleted successfully: {role.name}")
        return True
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Role deletion error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting role"
        )
