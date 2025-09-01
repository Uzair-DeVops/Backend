"""
Enterprise Role Service - Business logic layer for enterprise role operations (Functional approach)
"""
from typing import Optional, List
from uuid import UUID
from sqlmodel import Session, select
from fastapi import HTTPException, status
import json
from datetime import datetime

from ..models.enterprise_role_model import (
    EnterpriseRole, EnterpriseRoleCreate, EnterpriseRoleUpdate, EnterpriseRoleResponse
)
from ..utils.my_logger import get_logger

logger = get_logger("ENTERPRISE_ROLE_SERVICE")


def create_enterprise_role_service(role_data: EnterpriseRoleCreate, db: Session) -> EnterpriseRoleResponse:
    """Create a new enterprise role"""
    try:
        # Check if role name already exists for this enterprise client
        existing_role = get_enterprise_role_by_name_service(role_data.name, role_data.enterprise_client_id, db)
        if existing_role:
            logger.warning(f"Enterprise role creation failed: name {role_data.name} already exists for enterprise client {role_data.enterprise_client_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role name already exists for this enterprise client"
            )
        
        # Convert permissions list to JSON string
        permissions_json = json.dumps(role_data.permissions)
        
        # Create role object
        role = EnterpriseRole(
            name=role_data.name,
            description=role_data.description,
            permissions=permissions_json,
            enterprise_client_id=role_data.enterprise_client_id
        )
        
        # Save to database
        db.add(role)
        db.commit()
        db.refresh(role)
        
        logger.info(f"Enterprise role created successfully: {role.name}")
        
        return EnterpriseRoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            is_active=role.is_active,
            created_at=role.created_at,
            updated_at=role.updated_at,
            permissions=role_data.permissions,
            enterprise_client_id=role.enterprise_client_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enterprise role creation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating enterprise role"
        )


def get_enterprise_role_by_name_service(name: str, enterprise_client_id: str, db: Session) -> Optional[EnterpriseRole]:
    """Get enterprise role by name for a specific enterprise client"""
    try:
        client_uuid = UUID(enterprise_client_id)
        statement = select(EnterpriseRole).where(
            EnterpriseRole.name == name,
            EnterpriseRole.enterprise_client_id == client_uuid
        )
        return db.exec(statement).first()
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        return None
    except Exception as e:
        logger.error(f"Error getting enterprise role by name: {e}")
        return None


def get_enterprise_role_by_id_service(role_id: str, db: Session) -> Optional[EnterpriseRoleResponse]:
    """Get enterprise role by ID"""
    try:
        # Convert string to UUID
        role_uuid = UUID(role_id)
        statement = select(EnterpriseRole).where(EnterpriseRole.id == role_uuid)
        role = db.exec(statement).first()
        
        if not role:
            return None
        
        # Convert JSON permissions back to list
        permissions = json.loads(role.permissions) if role.permissions else []
        
        return EnterpriseRoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            is_active=role.is_active,
            created_at=role.created_at,
            updated_at=role.updated_at,
            permissions=permissions,
            enterprise_client_id=role.enterprise_client_id
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        return None
    except Exception as e:
        logger.error(f"Error getting enterprise role by ID: {e}")
        return None


def get_all_enterprise_roles_service(db: Session) -> List[EnterpriseRoleResponse]:
    """Get all enterprise roles"""
    try:
        statement = select(EnterpriseRole)
        roles = db.exec(statement).all()
        
        return [
            EnterpriseRoleResponse(
                id=role.id,
                name=role.name,
                description=role.description,
                is_active=role.is_active,
                created_at=role.created_at,
                updated_at=role.updated_at,
                permissions=json.loads(role.permissions) if role.permissions else [],
                enterprise_client_id=role.enterprise_client_id
            )
            for role in roles
        ]
        
    except Exception as e:
        logger.error(f"Error getting all enterprise roles: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving enterprise roles"
        )


def get_enterprise_roles_by_client_service(enterprise_client_id: str, db: Session) -> List[EnterpriseRoleResponse]:
    """Get enterprise roles by enterprise client ID"""
    try:
        client_uuid = UUID(enterprise_client_id)
        statement = select(EnterpriseRole).where(EnterpriseRole.enterprise_client_id == client_uuid)
        roles = db.exec(statement).all()
        
        return [
            EnterpriseRoleResponse(
                id=role.id,
                name=role.name,
                description=role.description,
                is_active=role.is_active,
                created_at=role.created_at,
                updated_at=role.updated_at,
                permissions=json.loads(role.permissions) if role.permissions else [],
                enterprise_client_id=role.enterprise_client_id
            )
            for role in roles
        ]
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enterprise client ID format"
        )
    except Exception as e:
        logger.error(f"Error getting enterprise roles by client: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving enterprise roles"
        )


def update_enterprise_role_service(role_id: str, role_data: EnterpriseRoleUpdate, db: Session) -> EnterpriseRoleResponse:
    """Update enterprise role"""
    try:
        # Convert string to UUID
        role_uuid = UUID(role_id)
        statement = select(EnterpriseRole).where(EnterpriseRole.id == role_uuid)
        role = db.exec(statement).first()
        
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enterprise role not found"
            )
        
        # Check if new name already exists for this enterprise client (if name is being updated)
        if role_data.name and role_data.name != role.name:
            existing_role = get_enterprise_role_by_name_service(role_data.name, str(role.enterprise_client_id), db)
            if existing_role:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Role name already exists for this enterprise client"
                )
        
        # Update fields
        for field, value in role_data.dict(exclude_unset=True).items():
            if hasattr(role, field) and field != "id":
                if field == "permissions" and value is not None:
                    value = json.dumps(value)
                setattr(role, field, value)
        
        # Update timestamp
        role.updated_at = datetime.now()
        
        db.add(role)
        db.commit()
        db.refresh(role)
        
        logger.info(f"Enterprise role updated successfully: {role.name}")
        
        return EnterpriseRoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            is_active=role.is_active,
            created_at=role.created_at,
            updated_at=role.updated_at,
            permissions=json.loads(role.permissions) if role.permissions else [],
            enterprise_client_id=role.enterprise_client_id
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enterprise role ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enterprise role update error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating enterprise role"
        )


def delete_enterprise_role_service(role_id: str, db: Session) -> bool:
    """Delete enterprise role"""
    try:
        # Convert string to UUID
        role_uuid = UUID(role_id)
        statement = select(EnterpriseRole).where(EnterpriseRole.id == role_uuid)
        role = db.exec(statement).first()
        
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enterprise role not found"
            )
        
        db.delete(role)
        db.commit()
        
        logger.info(f"Enterprise role deleted successfully: {role.name}")
        return True
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enterprise role ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enterprise role deletion error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting enterprise role"
        )


def activate_enterprise_role_service(role_id: str, db: Session) -> EnterpriseRoleResponse:
    """Activate an enterprise role"""
    try:
        role_uuid = UUID(role_id)
        statement = select(EnterpriseRole).where(EnterpriseRole.id == role_uuid)
        role = db.exec(statement).first()
        
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enterprise role not found"
            )
        
        role.is_active = True
        role.updated_at = datetime.now()
        
        db.add(role)
        db.commit()
        db.refresh(role)
        
        logger.info(f"Enterprise role activated: {role.name}")
        
        return EnterpriseRoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            is_active=role.is_active,
            created_at=role.created_at,
            updated_at=role.updated_at,
            permissions=json.loads(role.permissions) if role.permissions else [],
            enterprise_client_id=role.enterprise_client_id
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enterprise role ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enterprise role activation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error activating enterprise role"
        )


def deactivate_enterprise_role_service(role_id: str, db: Session) -> EnterpriseRoleResponse:
    """Deactivate an enterprise role"""
    try:
        role_uuid = UUID(role_id)
        statement = select(EnterpriseRole).where(EnterpriseRole.id == role_uuid)
        role = db.exec(statement).first()
        
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enterprise role not found"
            )
        
        role.is_active = False
        role.updated_at = datetime.now()
        
        db.add(role)
        db.commit()
        db.refresh(role)
        
        logger.info(f"Enterprise role deactivated: {role.name}")
        
        return EnterpriseRoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            is_active=role.is_active,
            created_at=role.created_at,
            updated_at=role.updated_at,
            permissions=json.loads(role.permissions) if role.permissions else [],
            enterprise_client_id=role.enterprise_client_id
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enterprise role ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enterprise role deactivation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deactivating enterprise role"
        )
