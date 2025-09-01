"""
Enterprise Admin Service - Business logic layer for enterprise admin operations (Functional approach)
"""
from typing import Optional, List
from uuid import UUID
from sqlmodel import Session, select
from fastapi import HTTPException, status
import json
from datetime import datetime

from ..models.enterprise_admin_model import (
    EnterpriseAdmin, EnterpriseAdminCreate, EnterpriseAdminUpdate, EnterpriseAdminResponse
)
from ..utils.my_logger import get_logger
from ..utils.auth_utils import get_password_hash, verify_password

logger = get_logger("ENTERPRISE_ADMIN_SERVICE")


def create_enterprise_admin_service(admin_data: EnterpriseAdminCreate, db: Session) -> EnterpriseAdminResponse:
    """Create a new enterprise admin"""
    try:
        # Check if email already exists
        existing_admin = get_enterprise_admin_by_email_service(admin_data.email, db)
        if existing_admin:
            logger.warning(f"Enterprise admin creation failed: email {admin_data.email} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        
        # Check if username already exists
        existing_username = get_enterprise_admin_by_username_service(admin_data.username, db)
        if existing_username:
            logger.warning(f"Enterprise admin creation failed: username {admin_data.username} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        
        # Hash password
        hashed_password = get_password_hash(admin_data.password)
        
        # Convert role_ids and permissions lists to JSON strings
        role_ids_json = json.dumps(admin_data.role_ids)
        permissions_json = json.dumps(admin_data.permissions)
        
        # Create admin object
        admin = EnterpriseAdmin(
            email=admin_data.email,
            username=admin_data.username,
            full_name=admin_data.full_name,
            password=hashed_password,
            role_ids=role_ids_json,
            permissions=permissions_json,
            enterprise_client_id=admin_data.enterprise_client_id
        )
        
        # Save to database
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        logger.info(f"Enterprise admin created successfully: {admin.email}")
        
        return EnterpriseAdminResponse(
            id=admin.id,
            email=admin.email,
            username=admin.username,
            full_name=admin.full_name,
            is_active=admin.is_active,
            created_at=admin.created_at,
            updated_at=admin.updated_at,
            role_ids=admin_data.role_ids,
            permissions=admin_data.permissions,
            enterprise_client_id=admin.enterprise_client_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enterprise admin creation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating enterprise admin"
        )


def get_enterprise_admin_by_email_service(email: str, db: Session) -> Optional[EnterpriseAdmin]:
    """Get enterprise admin by email"""
    try:
        statement = select(EnterpriseAdmin).where(EnterpriseAdmin.email == email)
        return db.exec(statement).first()
    except Exception as e:
        logger.error(f"Error getting enterprise admin by email: {e}")
        return None


def get_enterprise_admin_by_username_service(username: str, db: Session) -> Optional[EnterpriseAdmin]:
    """Get enterprise admin by username"""
    try:
        statement = select(EnterpriseAdmin).where(EnterpriseAdmin.username == username)
        return db.exec(statement).first()
    except Exception as e:
        logger.error(f"Error getting enterprise admin by username: {e}")
        return None


def get_enterprise_admin_by_id_service(admin_id: str, db: Session) -> Optional[EnterpriseAdminResponse]:
    """Get enterprise admin by ID"""
    try:
        # Convert string to UUID
        admin_uuid = UUID(admin_id)
        statement = select(EnterpriseAdmin).where(EnterpriseAdmin.id == admin_uuid)
        admin = db.exec(statement).first()
        
        if not admin:
            return None
        
        # Convert JSON role_ids and permissions back to lists
        role_ids = json.loads(admin.role_ids) if admin.role_ids else []
        permissions = json.loads(admin.permissions) if admin.permissions else []
        
        return EnterpriseAdminResponse(
            id=admin.id,
            email=admin.email,
            username=admin.username,
            full_name=admin.full_name,
            is_active=admin.is_active,
            created_at=admin.created_at,
            updated_at=admin.updated_at,
            role_ids=role_ids,
            permissions=permissions,
            enterprise_client_id=admin.enterprise_client_id
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        return None
    except Exception as e:
        logger.error(f"Error getting enterprise admin by ID: {e}")
        return None


def get_all_enterprise_admins_service(db: Session) -> List[EnterpriseAdminResponse]:
    """Get all enterprise admins"""
    try:
        statement = select(EnterpriseAdmin)
        admins = db.exec(statement).all()
        
        return [
            EnterpriseAdminResponse(
                id=admin.id,
                email=admin.email,
                username=admin.username,
                full_name=admin.full_name,
                is_active=admin.is_active,
                created_at=admin.created_at,
                updated_at=admin.updated_at,
                role_ids=json.loads(admin.role_ids) if admin.role_ids else [],
                permissions=json.loads(admin.permissions) if admin.permissions else [],
                enterprise_client_id=admin.enterprise_client_id
            )
            for admin in admins
        ]
        
    except Exception as e:
        logger.error(f"Error getting all enterprise admins: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving enterprise admins"
        )


def get_enterprise_admins_by_client_service(enterprise_client_id: str, db: Session) -> List[EnterpriseAdminResponse]:
    """Get enterprise admins by enterprise client ID"""
    try:
        client_uuid = UUID(enterprise_client_id)
        statement = select(EnterpriseAdmin).where(EnterpriseAdmin.enterprise_client_id == client_uuid)
        admins = db.exec(statement).all()
        
        return [
            EnterpriseAdminResponse(
                id=admin.id,
                email=admin.email,
                username=admin.username,
                full_name=admin.full_name,
                is_active=admin.is_active,
                created_at=admin.created_at,
                updated_at=admin.updated_at,
                role_ids=json.loads(admin.role_ids) if admin.role_ids else [],
                permissions=json.loads(admin.permissions) if admin.permissions else [],
                enterprise_client_id=admin.enterprise_client_id
            )
            for admin in admins
        ]
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enterprise client ID format"
        )
    except Exception as e:
        logger.error(f"Error getting enterprise admins by client: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving enterprise admins"
        )


def update_enterprise_admin_service(admin_id: str, admin_data: EnterpriseAdminUpdate, db: Session) -> EnterpriseAdminResponse:
    """Update enterprise admin"""
    try:
        # Convert string to UUID
        admin_uuid = UUID(admin_id)
        statement = select(EnterpriseAdmin).where(EnterpriseAdmin.id == admin_uuid)
        admin = db.exec(statement).first()
        
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enterprise admin not found"
            )
        
        # Check if new email already exists (if email is being updated)
        if admin_data.email and admin_data.email != admin.email:
            existing_admin = get_enterprise_admin_by_email_service(admin_data.email, db)
            if existing_admin:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )
        
        # Check if new username already exists (if username is being updated)
        if admin_data.username and admin_data.username != admin.username:
            existing_username = get_enterprise_admin_by_username_service(admin_data.username, db)
            if existing_username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists"
                )
        
        # Update fields
        for field, value in admin_data.dict(exclude_unset=True).items():
            if hasattr(admin, field) and field != "id":
                if field == "password" and value:
                    value = get_password_hash(value)
                elif field in ["role_ids", "permissions"] and value is not None:
                    value = json.dumps(value)
                setattr(admin, field, value)
        
        # Update timestamp
        admin.updated_at = datetime.now()
        
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        logger.info(f"Enterprise admin updated successfully: {admin.email}")
        
        return EnterpriseAdminResponse(
            id=admin.id,
            email=admin.email,
            username=admin.username,
            full_name=admin.full_name,
            is_active=admin.is_active,
            created_at=admin.created_at,
            updated_at=admin.updated_at,
            role_ids=json.loads(admin.role_ids) if admin.role_ids else [],
            permissions=json.loads(admin.permissions) if admin.permissions else [],
            enterprise_client_id=admin.enterprise_client_id
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enterprise admin ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enterprise admin update error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating enterprise admin"
        )


def delete_enterprise_admin_service(admin_id: str, db: Session) -> bool:
    """Delete enterprise admin"""
    try:
        # Convert string to UUID
        admin_uuid = UUID(admin_id)
        statement = select(EnterpriseAdmin).where(EnterpriseAdmin.id == admin_uuid)
        admin = db.exec(statement).first()
        
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enterprise admin not found"
            )
        
        db.delete(admin)
        db.commit()
        
        logger.info(f"Enterprise admin deleted successfully: {admin.email}")
        return True
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enterprise admin ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enterprise admin deletion error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting enterprise admin"
        )


def verify_enterprise_admin_password_service(admin: EnterpriseAdmin, password: str) -> bool:
    """Verify enterprise admin password"""
    return verify_password(password, admin.password)


def activate_enterprise_admin_service(admin_id: str, db: Session) -> EnterpriseAdminResponse:
    """Activate an enterprise admin"""
    try:
        admin_uuid = UUID(admin_id)
        statement = select(EnterpriseAdmin).where(EnterpriseAdmin.id == admin_uuid)
        admin = db.exec(statement).first()
        
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enterprise admin not found"
            )
        
        admin.is_active = True
        admin.updated_at = datetime.now()
        
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        logger.info(f"Enterprise admin activated: {admin.email}")
        
        return EnterpriseAdminResponse(
            id=admin.id,
            email=admin.email,
            username=admin.username,
            full_name=admin.full_name,
            is_active=admin.is_active,
            created_at=admin.created_at,
            updated_at=admin.updated_at,
            role_ids=json.loads(admin.role_ids) if admin.role_ids else [],
            permissions=json.loads(admin.permissions) if admin.permissions else [],
            enterprise_client_id=admin.enterprise_client_id
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enterprise admin ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enterprise admin activation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error activating enterprise admin"
        )


def deactivate_enterprise_admin_service(admin_id: str, db: Session) -> EnterpriseAdminResponse:
    """Deactivate an enterprise admin"""
    try:
        admin_uuid = UUID(admin_id)
        statement = select(EnterpriseAdmin).where(EnterpriseAdmin.id == admin_uuid)
        admin = db.exec(statement).first()
        
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enterprise admin not found"
            )
        
        admin.is_active = False
        admin.updated_at = datetime.now()
        
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        logger.info(f"Enterprise admin deactivated: {admin.email}")
        
        return EnterpriseAdminResponse(
            id=admin.id,
            email=admin.email,
            username=admin.username,
            full_name=admin.full_name,
            is_active=admin.is_active,
            created_at=admin.created_at,
            updated_at=admin.updated_at,
            role_ids=json.loads(admin.role_ids) if admin.role_ids else [],
            permissions=json.loads(admin.permissions) if admin.permissions else [],
            enterprise_client_id=admin.enterprise_client_id
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enterprise admin ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enterprise admin deactivation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deactivating enterprise admin"
        )
