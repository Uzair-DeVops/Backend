"""
Admin Permission Service - Business logic layer for admin permission operations (Functional approach)
"""
from typing import Optional, List
from sqlmodel import Session, select
from fastapi import HTTPException, status
from datetime import datetime

from ..models.admin_permission_model import (
    AdminPermission, AdminPermissionCreate, AdminPermissionUpdate, AdminPermissionResponse
)
from ..utils.my_logger import get_logger

logger = get_logger("ADMIN_PERMISSION_SERVICE")


def _convert_id_to_permission(permission_id: str, db: Session) -> Optional[AdminPermission]:
    """Helper function to convert ID (hex string or integer position) to permission object"""
    try:
        # Try to find by the exact ID string first (for hex IDs)
        statement = select(AdminPermission).where(AdminPermission.id == permission_id)
        permission = db.exec(statement).first()
        
        if not permission:
            # If not found, try to find by position/index (for integer IDs)
            try:
                int_id = int(permission_id)
                if int_id > 0:
                    # Get all permissions and find by position (1-based index)
                    all_permissions = db.exec(select(AdminPermission)).all()
                    if 0 < int_id <= len(all_permissions):
                        permission = all_permissions[int_id - 1]  # Convert to 0-based index
                        logger.info(f"Found permission by position {int_id}: {permission.name}")
                    else:
                        logger.warning(f"Position {int_id} out of range. Total permissions: {len(all_permissions)}")
                        return None
                else:
                    logger.warning(f"Invalid position: {int_id}")
                    return None
            except ValueError:
                logger.warning(f"Invalid ID format: {permission_id}")
                return None
        
        return permission
        
    except Exception as e:
        logger.error(f"Error converting ID to permission: {e}")
        return None


def create_admin_permission_service(permission_data: AdminPermissionCreate, db: Session) -> AdminPermissionResponse:
    """Create a new admin permission"""
    try:
        # Check if permission name already exists
        existing_permission = get_admin_permission_by_name_service(permission_data.name, db)
        if existing_permission:
            logger.warning(f"Permission creation failed: name {permission_data.name} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Permission name already exists"
            )
        
        # Create permission object
        permission = AdminPermission(
            name=permission_data.name,
            description=permission_data.description,
            resource=permission_data.resource,
            action=permission_data.action,
            is_active=permission_data.is_active
        )
        
        # Save to database
        db.add(permission)
        db.commit()
        db.refresh(permission)
        
        logger.info(f"Admin permission created successfully: {permission.name}")
        
        return AdminPermissionResponse(
            id=permission.id,
            name=permission.name,
            description=permission.description,
            resource=permission.resource,
            action=permission.action,
            is_active=permission.is_active,
            created_at=permission.created_at,
            updated_at=permission.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Permission creation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating permission"
        )


def get_admin_permission_by_name_service(name: str, db: Session) -> Optional[AdminPermission]:
    """Get admin permission by name"""
    try:
        statement = select(AdminPermission).where(AdminPermission.name == name)
        return db.exec(statement).first()
    except Exception as e:
        logger.error(f"Error getting permission by name: {e}")
        return None


def get_admin_permission_by_id_service(permission_id: str, db: Session) -> Optional[AdminPermissionResponse]:
    """Get admin permission by ID - Supports both hex strings and simple integers"""
    try:
        permission = _convert_id_to_permission(permission_id, db)
        
        if not permission:
            return None
        
        return AdminPermissionResponse(
            id=permission.id,
            name=permission.name,
            description=permission.description,
            resource=permission.resource,
            action=permission.action,
            is_active=permission.is_active,
            created_at=permission.created_at,
            updated_at=permission.updated_at
        )
        
    except Exception as e:
        logger.error(f"Error getting permission by ID: {e}")
        return None


def get_all_admin_permissions_service(db: Session) -> List[AdminPermissionResponse]:
    """Get all admin permissions"""
    try:
        statement = select(AdminPermission)
        permissions = db.exec(statement).all()
        
        return [
            AdminPermissionResponse(
                id=permission.id,
                name=permission.name,
                description=permission.description,
                resource=permission.resource,
                action=permission.action,
                is_active=permission.is_active,
                created_at=permission.created_at,
                updated_at=permission.updated_at
            )
            for permission in permissions
        ]
        
    except Exception as e:
        logger.error(f"Error getting all permissions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving permissions"
        )


def get_permissions_by_resource_service(resource: str, db: Session) -> List[AdminPermissionResponse]:
    """Get permissions by resource"""
    try:
        statement = select(AdminPermission).where(AdminPermission.resource == resource)
        permissions = db.exec(statement).all()
        
        return [
            AdminPermissionResponse(
                id=permission.id,
                name=permission.name,
                description=permission.description,
                resource=permission.resource,
                action=permission.action,
                is_active=permission.is_active,
                created_at=permission.created_at,
                updated_at=permission.updated_at
            )
            for permission in permissions
        ]
        
    except Exception as e:
        logger.error(f"Error getting permissions by resource: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving permissions by resource"
        )


def update_admin_permission_service(permission_id: str, permission_data: AdminPermissionUpdate, db: Session) -> AdminPermissionResponse:
    """Update admin permission - Supports both hex strings and simple integers"""
    try:
        permission = _convert_id_to_permission(permission_id, db)
        
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Permission not found"
            )
        
        # Check if new name already exists (if name is being updated)
        if permission_data.name and permission_data.name != permission.name:
            existing_permission = get_admin_permission_by_name_service(permission_data.name, db)
            if existing_permission:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Permission name already exists"
                )
        
        # Update fields
        for field, value in permission_data.dict(exclude_unset=True).items():
            if hasattr(permission, field) and field != "id":
                setattr(permission, field, value)
        
        # Update timestamp
        permission.updated_at = datetime.utcnow()
        
        db.add(permission)
        db.commit()
        db.refresh(permission)
        
        logger.info(f"Admin permission updated successfully: {permission.name}")
        
        return AdminPermissionResponse(
            id=permission.id,
            name=permission.name,
            description=permission.description,
            resource=permission.resource,
            action=permission.action,
            is_active=permission.is_active,
            created_at=permission.created_at,
            updated_at=permission.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Permission update error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating permission"
        )


def delete_admin_permission_service(permission_id: str, db: Session) -> bool:
    """Delete admin permission - Supports both hex strings and simple integers"""
    try:
        permission = _convert_id_to_permission(permission_id, db)
        
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Permission not found"
            )
        
        db.delete(permission)
        db.commit()
        
        logger.info(f"Admin permission deleted successfully: {permission.name}")
        return True
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Permission deletion error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting permission"
        )


def activate_permission_service(permission_id: str, db: Session) -> AdminPermissionResponse:
    """Activate a permission - Supports both hex strings and simple integers"""
    try:
        permission = _convert_id_to_permission(permission_id, db)
        
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Permission not found"
            )
        
        permission.is_active = True
        permission.updated_at = datetime.utcnow()
        
        db.add(permission)
        db.commit()
        db.refresh(permission)
        
        logger.info(f"Admin permission activated: {permission.name}")
        
        return AdminPermissionResponse(
            id=permission.id,
            name=permission.name,
            description=permission.description,
            resource=permission.resource,
            action=permission.action,
            is_active=permission.is_active,
            created_at=permission.created_at,
            updated_at=permission.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Permission activation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error activating permission"
        )


def deactivate_permission_service(permission_id: str, db: Session) -> AdminPermissionResponse:
    """Deactivate a permission - Supports both hex strings and simple integers"""
    try:
        permission = _convert_id_to_permission(permission_id, db)
        
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Permission not found"
            )
        
        permission.is_active = False
        permission.updated_at = datetime.utcnow()
        
        db.add(permission)
        db.commit()
        db.refresh(permission)
        
        logger.info(f"Admin permission deactivated: {permission.name}")
        
        return AdminPermissionResponse(
            id=permission.id,
            name=permission.name,
            description=permission.description,
            resource=permission.resource,
            action=permission.action,
            is_active=permission.is_active,
            created_at=permission.created_at,
            updated_at=permission.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Permission deactivation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deactivating permission"
        )
