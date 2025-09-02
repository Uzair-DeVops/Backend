"""
Admin Role Service - Business logic layer for admin role operations (Functional approach)
"""
from typing import Optional, List
from uuid import UUID
from sqlmodel import Session, select
from fastapi import HTTPException, status
import json
from datetime import datetime

from ..models.admin_role_model import (
    AdminRole, AdminRoleCreate, AdminRoleUpdate, AdminRoleResponse
)
from ..utils.my_logger import get_logger

logger = get_logger("ADMIN_ROLE_SERVICE")


def create_admin_role_service(role_data: AdminRoleCreate, db: Session) -> AdminRoleResponse:
    """Create a new admin role"""
    try:
        # Check if role name already exists
        existing_role = get_admin_role_by_name_service(role_data.name, db)
        if existing_role:
            logger.warning(f"Role creation failed: name {role_data.name} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role name already exists"
            )
        
        # Convert permissions list to JSON string
        permissions_json = json.dumps(role_data.permissions)
        
        # Create role object
        role = AdminRole(
            name=role_data.name,
            description=role_data.description,
            permissions=permissions_json,
            is_active=role_data.is_active
        )
        
        # Save to database
        db.add(role)
        db.commit()
        db.refresh(role)
        
        logger.info(f"Admin role created successfully: {role.name}")
        
        return AdminRoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            permissions=role_data.permissions,
            is_active=role.is_active,
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


def get_admin_role_by_name_service(name: str, db: Session) -> Optional[AdminRole]:
    """Get admin role by name"""
    try:
        statement = select(AdminRole).where(AdminRole.name == name)
        return db.exec(statement).first()
    except Exception as e:
        logger.error(f"Error getting role by name: {e}")
        return None


def get_admin_role_by_id_service(role_id: str, db: Session) -> Optional[AdminRoleResponse]:
    """Get admin role by ID - Supports both hex strings and simple integers"""
    try:
        # Try to find by the exact ID string first (for hex IDs)
        statement = select(AdminRole).where(AdminRole.id == role_id)
        role = db.exec(statement).first()
        
        if not role:
            # If not found, try to find by position/index (for integer IDs)
            try:
                int_id = int(role_id)
                if int_id > 0:
                    # Get all roles and find by position (1-based index)
                    all_roles = db.exec(select(AdminRole)).all()
                    if 0 < int_id <= len(all_roles):
                        role = all_roles[int_id - 1]  # Convert to 0-based index
                        logger.info(f"Found role by position {int_id}: {role.name}")
                    else:
                        logger.warning(f"Position {int_id} out of range. Total roles: {len(all_roles)}")
                        return None
                else:
                    logger.warning(f"Invalid position: {int_id}")
                    return None
            except ValueError:
                logger.warning(f"Invalid ID format: {role_id}")
                return None
        
        if not role:
            return None
        
        # Convert JSON permissions back to list
        permissions = json.loads(role.permissions) if role.permissions else []
        
        return AdminRoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            permissions=permissions,
            is_active=role.is_active,
            created_at=role.created_at,
            updated_at=role.updated_at
        )
        
    except Exception as e:
        logger.error(f"Error getting role by ID: {e}")
        return None


def get_all_admin_roles_service(db: Session) -> List[AdminRoleResponse]:
    """Get all admin roles"""
    try:
        statement = select(AdminRole)
        roles = db.exec(statement).all()
        
        return [
            AdminRoleResponse(
                id=role.id,
                name=role.name,
                description=role.description,
                permissions=json.loads(role.permissions) if role.permissions else [],
                is_active=role.is_active,
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


def update_admin_role_service(role_id: str, role_data: AdminRoleUpdate, db: Session) -> AdminRoleResponse:
    """Update admin role"""
    try:
        # Convert string to UUID
        role_uuid = UUID(role_id)
        statement = select(AdminRole).where(AdminRole.id == role_uuid)
        role = db.exec(statement).first()
        
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        # Check if new name already exists (if name is being updated)
        if role_data.name and role_data.name != role.name:
            existing_role = get_admin_role_by_name_service(role_data.name, db)
            if existing_role:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Role name already exists"
                )
        
        # Update fields
        for field, value in role_data.dict(exclude_unset=True).items():
            if hasattr(role, field) and field != "id":
                if field == "permissions" and value is not None:
                    value = json.dumps(value)
                setattr(role, field, value)
        
        # Update timestamp
        role.updated_at = datetime.utcnow()
        
        db.add(role)
        db.commit()
        db.refresh(role)
        
        logger.info(f"Admin role updated successfully: {role.name}")
        
        return AdminRoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            permissions=json.loads(role.permissions) if role.permissions else [],
            is_active=role.is_active,
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


def delete_admin_role_service(role_id: str, db: Session) -> bool:
    """Delete admin role"""
    try:
        # Convert string to UUID
        role_uuid = UUID(role_id)
        statement = select(AdminRole).where(AdminRole.id == role_uuid)
        role = db.exec(statement).first()
        
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        db.delete(role)
        db.commit()
        
        logger.info(f"Admin role deleted successfully: {role.name}")
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


def activate_role_service(role_id: str, db: Session) -> AdminRoleResponse:
    """Activate a role"""
    try:
        role_uuid = UUID(role_id)
        statement = select(AdminRole).where(AdminRole.id == role_uuid)
        role = db.exec(statement).first()
        
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        role.is_active = True
        role.updated_at = datetime.utcnow()
        
        db.add(role)
        db.commit()
        db.refresh(role)
        
        logger.info(f"Admin role activated: {role.name}")
        
        return AdminRoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            permissions=json.loads(role.permissions) if role.permissions else [],
            is_active=role.is_active,
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
        logger.error(f"Role activation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error activating role"
        )


def deactivate_role_service(role_id: str, db: Session) -> AdminRoleResponse:
    """Deactivate a role"""
    try:
        role_uuid = UUID(role_id)
        statement = select(AdminRole).where(AdminRole.id == role_uuid)
        role = db.exec(statement).first()
        
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        role.is_active = False
        role.updated_at = datetime.utcnow()
        
        db.add(role)
        db.commit()
        db.refresh(role)
        
        logger.info(f"Admin role deactivated: {role.name}")
        
        return AdminRoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            permissions=json.loads(role.permissions) if role.permissions else [],
            is_active=role.is_active,
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
        logger.error(f"Role deactivation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deactivating role"
        )
