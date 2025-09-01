"""
Enterprise Permission Service - Business logic layer for enterprise permission operations (Functional approach)
"""
from typing import Optional, List
from uuid import UUID
from sqlmodel import Session, select
from fastapi import HTTPException, status
import json
from datetime import datetime

from ..models.enterprise_permission_model import (
    EnterprisePermission, EnterprisePermissionCreate, EnterprisePermissionUpdate, EnterprisePermissionResponse
)
from ..utils.my_logger import get_logger

logger = get_logger("ENTERPRISE_PERMISSION_SERVICE")


def create_enterprise_permission_service(permission_data: EnterprisePermissionCreate, db: Session) -> EnterprisePermissionResponse:
    """Create a new enterprise permission"""
    try:
        # Check if permission name already exists for this enterprise client
        existing_permission = get_enterprise_permission_by_name_service(permission_data.name, permission_data.enterprise_client_id, db)
        if existing_permission:
            logger.warning(f"Enterprise permission creation failed: name {permission_data.name} already exists for enterprise client {permission_data.enterprise_client_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Permission name already exists for this enterprise client"
            )
        
        # Create permission object
        permission = EnterprisePermission(
            name=permission_data.name,
            description=permission_data.description,
            resource=permission_data.resource,
            action=permission_data.action,
            enterprise_client_id=permission_data.enterprise_client_id
        )
        
        # Save to database
        db.add(permission)
        db.commit()
        db.refresh(permission)
        
        logger.info(f"Enterprise permission created successfully: {permission.name}")
        
        return EnterprisePermissionResponse(
            id=permission.id,
            name=permission.name,
            description=permission.description,
            resource=permission.resource,
            action=permission.action,
            is_active=permission.is_active,
            created_at=permission.created_at,
            updated_at=permission.updated_at,
            enterprise_client_id=permission.enterprise_client_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enterprise permission creation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating enterprise permission"
        )


def get_enterprise_permission_by_name_service(name: str, enterprise_client_id: str, db: Session) -> Optional[EnterprisePermission]:
    """Get enterprise permission by name for a specific enterprise client"""
    try:
        client_uuid = UUID(enterprise_client_id)
        statement = select(EnterprisePermission).where(
            EnterprisePermission.name == name,
            EnterprisePermission.enterprise_client_id == client_uuid
        )
        return db.exec(statement).first()
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        return None
    except Exception as e:
        logger.error(f"Error getting enterprise permission by name: {e}")
        return None


def get_enterprise_permission_by_id_service(permission_id: str, db: Session) -> Optional[EnterprisePermissionResponse]:
    """Get enterprise permission by ID"""
    try:
        # Convert string to UUID
        permission_uuid = UUID(permission_id)
        statement = select(EnterprisePermission).where(EnterprisePermission.id == permission_uuid)
        permission = db.exec(statement).first()
        
        if not permission:
            return None
        
        return EnterprisePermissionResponse(
            id=permission.id,
            name=permission.name,
            description=permission.description,
            resource=permission.resource,
            action=permission.action,
            is_active=permission.is_active,
            created_at=permission.created_at,
            updated_at=permission.updated_at,
            enterprise_client_id=permission.enterprise_client_id
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        return None
    except Exception as e:
        logger.error(f"Error getting enterprise permission by ID: {e}")
        return None


def get_all_enterprise_permissions_service(db: Session) -> List[EnterprisePermissionResponse]:
    """Get all enterprise permissions"""
    try:
        statement = select(EnterprisePermission)
        permissions = db.exec(statement).all()
        
        return [
            EnterprisePermissionResponse(
                id=permission.id,
                name=permission.name,
                description=permission.description,
                resource=permission.resource,
                action=permission.action,
                is_active=permission.is_active,
                created_at=permission.created_at,
                updated_at=permission.updated_at,
                enterprise_client_id=permission.enterprise_client_id
            )
            for permission in permissions
        ]
        
    except Exception as e:
        logger.error(f"Error getting all enterprise permissions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving enterprise permissions"
        )


def get_enterprise_permissions_by_client_service(enterprise_client_id: str, db: Session) -> List[EnterprisePermissionResponse]:
    """Get enterprise permissions by enterprise client ID"""
    try:
        client_uuid = UUID(enterprise_client_id)
        statement = select(EnterprisePermission).where(EnterprisePermission.enterprise_client_id == client_uuid)
        permissions = db.exec(statement).all()
        
        return [
            EnterprisePermissionResponse(
                id=permission.id,
                name=permission.name,
                description=permission.description,
                resource=permission.resource,
                action=permission.action,
                is_active=permission.is_active,
                created_at=permission.created_at,
                updated_at=permission.updated_at,
                enterprise_client_id=permission.enterprise_client_id
            )
            for permission in permissions
        ]
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enterprise client ID format"
        )
    except Exception as e:
        logger.error(f"Error getting enterprise permissions by client: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving enterprise permissions"
        )


def get_enterprise_permissions_by_resource_service(resource: str, enterprise_client_id: str, db: Session) -> List[EnterprisePermissionResponse]:
    """Get enterprise permissions by resource for a specific enterprise client"""
    try:
        client_uuid = UUID(enterprise_client_id)
        statement = select(EnterprisePermission).where(
            EnterprisePermission.resource == resource,
            EnterprisePermission.enterprise_client_id == client_uuid
        )
        permissions = db.exec(statement).all()
        
        return [
            EnterprisePermissionResponse(
                id=permission.id,
                name=permission.name,
                description=permission.description,
                resource=permission.resource,
                action=permission.action,
                is_active=permission.is_active,
                created_at=permission.created_at,
                updated_at=permission.updated_at,
                enterprise_client_id=permission.enterprise_client_id
            )
            for permission in permissions
        ]
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enterprise client ID format"
        )
    except Exception as e:
        logger.error(f"Error getting enterprise permissions by resource: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving enterprise permissions"
        )


def update_enterprise_permission_service(permission_id: str, permission_data: EnterprisePermissionUpdate, db: Session) -> EnterprisePermissionResponse:
    """Update enterprise permission"""
    try:
        # Convert string to UUID
        permission_uuid = UUID(permission_id)
        statement = select(EnterprisePermission).where(EnterprisePermission.id == permission_uuid)
        permission = db.exec(statement).first()
        
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enterprise permission not found"
            )
        
        # Check if new name already exists for this enterprise client (if name is being updated)
        if permission_data.name and permission_data.name != permission.name:
            existing_permission = get_enterprise_permission_by_name_service(permission_data.name, str(permission.enterprise_client_id), db)
            if existing_permission:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Permission name already exists for this enterprise client"
                )
        
        # Update fields
        for field, value in permission_data.dict(exclude_unset=True).items():
            if hasattr(permission, field) and field != "id":
                setattr(permission, field, value)
        
        # Update timestamp
        permission.updated_at = datetime.now()
        
        db.add(permission)
        db.commit()
        db.refresh(permission)
        
        logger.info(f"Enterprise permission updated successfully: {permission.name}")
        
        return EnterprisePermissionResponse(
            id=permission.id,
            name=permission.name,
            description=permission.description,
            resource=permission.resource,
            action=permission.action,
            is_active=permission.is_active,
            created_at=permission.created_at,
            updated_at=permission.updated_at,
            enterprise_client_id=permission.enterprise_client_id
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enterprise permission ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enterprise permission update error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating enterprise permission"
        )


def delete_enterprise_permission_service(permission_id: str, db: Session) -> bool:
    """Delete enterprise permission"""
    try:
        # Convert string to UUID
        permission_uuid = UUID(permission_id)
        statement = select(EnterprisePermission).where(EnterprisePermission.id == permission_uuid)
        permission = db.exec(statement).first()
        
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enterprise permission not found"
            )
        
        db.delete(permission)
        db.commit()
        
        logger.info(f"Enterprise permission deleted successfully: {permission.name}")
        return True
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enterprise permission ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enterprise permission deletion error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting enterprise permission"
        )


def activate_enterprise_permission_service(permission_id: str, db: Session) -> EnterprisePermissionResponse:
    """Activate an enterprise permission"""
    try:
        permission_uuid = UUID(permission_id)
        statement = select(EnterprisePermission).where(EnterprisePermission.id == permission_uuid)
        permission = db.exec(statement).first()
        
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enterprise permission not found"
            )
        
        permission.is_active = True
        permission.updated_at = datetime.now()
        
        db.add(permission)
        db.commit()
        db.refresh(permission)
        
        logger.info(f"Enterprise permission activated: {permission.name}")
        
        return EnterprisePermissionResponse(
            id=permission.id,
            name=permission.name,
            description=permission.description,
            resource=permission.resource,
            action=permission.action,
            is_active=permission.is_active,
            created_at=permission.created_at,
            updated_at=permission.updated_at,
            enterprise_client_id=permission.enterprise_client_id
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enterprise permission ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enterprise permission activation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error activating enterprise permission"
        )


def deactivate_enterprise_permission_service(permission_id: str, db: Session) -> EnterprisePermissionResponse:
    """Deactivate an enterprise permission"""
    try:
        permission_uuid = UUID(permission_id)
        statement = select(EnterprisePermission).where(EnterprisePermission.id == permission_uuid)
        permission = db.exec(statement).first()
        
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enterprise permission not found"
            )
        
        permission.is_active = False
        permission.updated_at = datetime.now()
        
        db.add(permission)
        db.commit()
        db.refresh(permission)
        
        logger.info(f"Enterprise permission deactivated: {permission.name}")
        
        return EnterprisePermissionResponse(
            id=permission.id,
            name=permission.name,
            description=permission.description,
            resource=permission.resource,
            action=permission.action,
            is_active=permission.is_active,
            created_at=permission.created_at,
            updated_at=permission.updated_at,
            enterprise_client_id=permission.enterprise_client_id
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enterprise permission ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enterprise permission deactivation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deactivating enterprise permission"
        )
