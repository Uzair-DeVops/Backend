"""
Enterprise User Service - Business logic layer for enterprise user operations (Functional approach)
"""
from typing import Optional, List
from uuid import UUID
from sqlmodel import Session, select
from fastapi import HTTPException, status
import json
from datetime import datetime

from ..models.enterprise_user_model import (
    EnterpriseUser, EnterpriseUserCreate, EnterpriseUserUpdate, EnterpriseUserResponse
)
from ..utils.my_logger import get_logger
from ..utils.auth_utils import get_password_hash, verify_password

logger = get_logger("ENTERPRISE_USER_SERVICE")


def create_enterprise_user_service(user_data: EnterpriseUserCreate, db: Session) -> EnterpriseUserResponse:
    """Create a new enterprise user"""
    try:
        # Check if email already exists
        existing_user = get_enterprise_user_by_email_service(user_data.email, db)
        if existing_user:
            logger.warning(f"Enterprise user creation failed: email {user_data.email} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        
        # Check if username already exists
        existing_username = get_enterprise_user_by_username_service(user_data.username, db)
        if existing_username:
            logger.warning(f"Enterprise user creation failed: username {user_data.username} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Convert role_ids, permissions, and settings to JSON strings
        role_ids_json = json.dumps(user_data.role_ids)
        permissions_json = json.dumps(user_data.permissions)
        settings_json = json.dumps(user_data.settings) if user_data.settings else "{}"
        
        # Create user object
        user = EnterpriseUser(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            user_type=user_data.user_type,
            department=user_data.department,
            position=user_data.position,
            phone=user_data.phone,
            password=hashed_password,
            role_ids=role_ids_json,
            permissions=permissions_json,
            settings=settings_json,
            enterprise_client_id=user_data.enterprise_client_id,
            created_by=user_data.created_by
        )
        
        # Save to database
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"Enterprise user created successfully: {user.email} (Type: {user.user_type})")
        
        return EnterpriseUserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            user_type=user.user_type,
            department=user.department,
            position=user.position,
            phone=user.phone,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            role_ids=user_data.role_ids,
            permissions=user_data.permissions,
            settings=user_data.settings,
            enterprise_client_id=user.enterprise_client_id,
            created_by=user.created_by
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enterprise user creation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating enterprise user"
        )


def get_enterprise_user_by_email_service(email: str, db: Session) -> Optional[EnterpriseUser]:
    """Get enterprise user by email"""
    try:
        statement = select(EnterpriseUser).where(EnterpriseUser.email == email)
        return db.exec(statement).first()
    except Exception as e:
        logger.error(f"Error getting enterprise user by email: {e}")
        return None


def get_enterprise_user_by_username_service(username: str, db: Session) -> Optional[EnterpriseUser]:
    """Get enterprise user by username"""
    try:
        statement = select(EnterpriseUser).where(EnterpriseUser.username == username)
        return db.exec(statement).first()
    except Exception as e:
        logger.error(f"Error getting enterprise user by username: {e}")
        return None


def get_enterprise_user_by_id_service(user_id: str, db: Session) -> Optional[EnterpriseUserResponse]:
    """Get enterprise user by ID"""
    try:
        # Convert string to UUID
        user_uuid = UUID(user_id)
        statement = select(EnterpriseUser).where(EnterpriseUser.id == user_uuid)
        user = db.exec(statement).first()
        
        if not user:
            return None
        
        # Convert JSON role_ids, permissions, and settings back to lists/dict
        role_ids = json.loads(user.role_ids) if user.role_ids else []
        permissions = json.loads(user.permissions) if user.permissions else []
        settings = json.loads(user.settings) if user.settings else {}
        
        return EnterpriseUserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            user_type=user.user_type,
            department=user.department,
            position=user.position,
            phone=user.phone,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            role_ids=role_ids,
            permissions=permissions,
            settings=settings,
            enterprise_client_id=user.enterprise_client_id,
            created_by=user.created_by
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        return None
    except Exception as e:
        logger.error(f"Error getting enterprise user by ID: {e}")
        return None


def get_all_enterprise_users_service(db: Session) -> List[EnterpriseUserResponse]:
    """Get all enterprise users"""
    try:
        statement = select(EnterpriseUser)
        users = db.exec(statement).all()
        
        return [
            EnterpriseUserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                full_name=user.full_name,
                user_type=user.user_type,
                department=user.department,
                position=user.position,
                phone=user.phone,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
                role_ids=json.loads(user.role_ids) if user.role_ids else [],
                permissions=json.loads(user.permissions) if user.permissions else [],
                settings=json.loads(user.settings) if user.settings else {},
                enterprise_client_id=user.enterprise_client_id,
                created_by=user.created_by
            )
            for user in users
        ]
        
    except Exception as e:
        logger.error(f"Error getting all enterprise users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving enterprise users"
        )


def get_enterprise_users_by_client_service(enterprise_client_id: str, db: Session) -> List[EnterpriseUserResponse]:
    """Get enterprise users by enterprise client ID"""
    try:
        client_uuid = UUID(enterprise_client_id)
        statement = select(EnterpriseUser).where(EnterpriseUser.enterprise_client_id == client_uuid)
        users = db.exec(statement).all()
        
        return [
            EnterpriseUserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                full_name=user.full_name,
                user_type=user.user_type,
                department=user.department,
                position=user.position,
                phone=user.phone,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
                role_ids=json.loads(user.role_ids) if user.role_ids else [],
                permissions=json.loads(user.permissions) if user.permissions else [],
                settings=json.loads(user.settings) if user.settings else {},
                enterprise_client_id=user.enterprise_client_id,
                created_by=user.created_by
            )
            for user in users
        ]
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enterprise client ID format"
        )
    except Exception as e:
        logger.error(f"Error getting enterprise users by client: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving enterprise users"
        )


def get_enterprise_users_by_type_service(user_type: str, enterprise_client_id: str, db: Session) -> List[EnterpriseUserResponse]:
    """Get enterprise users by user type for a specific enterprise client"""
    try:
        client_uuid = UUID(enterprise_client_id)
        statement = select(EnterpriseUser).where(
            EnterpriseUser.user_type == user_type,
            EnterpriseUser.enterprise_client_id == client_uuid
        )
        users = db.exec(statement).all()
        
        return [
            EnterpriseUserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                full_name=user.full_name,
                user_type=user.user_type,
                department=user.department,
                position=user.position,
                phone=user.phone,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
                role_ids=json.loads(user.role_ids) if user.role_ids else [],
                permissions=json.loads(user.permissions) if user.permissions else [],
                settings=json.loads(user.settings) if user.settings else {},
                enterprise_client_id=user.enterprise_client_id,
                created_by=user.created_by
            )
            for user in users
        ]
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enterprise client ID format"
        )
    except Exception as e:
        logger.error(f"Error getting enterprise users by type: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving enterprise users"
        )


def get_enterprise_users_by_creator_service(created_by: str, db: Session) -> List[EnterpriseUserResponse]:
    """Get enterprise users created by a specific enterprise admin"""
    try:
        creator_uuid = UUID(created_by)
        statement = select(EnterpriseUser).where(EnterpriseUser.created_by == creator_uuid)
        users = db.exec(statement).all()
        
        return [
            EnterpriseUserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                full_name=user.full_name,
                user_type=user.user_type,
                department=user.department,
                position=user.position,
                phone=user.phone,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
                role_ids=json.loads(user.role_ids) if user.role_ids else [],
                permissions=json.loads(user.permissions) if user.permissions else [],
                settings=json.loads(user.settings) if user.settings else {},
                enterprise_client_id=user.enterprise_client_id,
                created_by=user.created_by
            )
            for user in users
        ]
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid creator ID format"
        )
    except Exception as e:
        logger.error(f"Error getting enterprise users by creator: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving enterprise users"
        )


def update_enterprise_user_service(user_id: str, user_data: EnterpriseUserUpdate, db: Session) -> EnterpriseUserResponse:
    """Update enterprise user"""
    try:
        # Convert string to UUID
        user_uuid = UUID(user_id)
        statement = select(EnterpriseUser).where(EnterpriseUser.id == user_uuid)
        user = db.exec(statement).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enterprise user not found"
            )
        
        # Check if new email already exists (if email is being updated)
        if user_data.email and user_data.email != user.email:
            existing_user = get_enterprise_user_by_email_service(user_data.email, db)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )
        
        # Check if new username already exists (if username is being updated)
        if user_data.username and user_data.username != user.username:
            existing_username = get_enterprise_user_by_username_service(user_data.username, db)
            if existing_username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists"
                )
        
        # Update fields
        for field, value in user_data.dict(exclude_unset=True).items():
            if hasattr(user, field) and field != "id":
                if field == "password" and value:
                    value = get_password_hash(value)
                elif field in ["role_ids", "permissions"] and value is not None:
                    value = json.dumps(value)
                elif field == "settings" and value is not None:
                    value = json.dumps(value)
                setattr(user, field, value)
        
        # Update timestamp
        user.updated_at = datetime.now()
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"Enterprise user updated successfully: {user.email}")
        
        return EnterpriseUserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            user_type=user.user_type,
            department=user.department,
            position=user.position,
            phone=user.phone,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            role_ids=json.loads(user.role_ids) if user.role_ids else [],
            permissions=json.loads(user.permissions) if user.permissions else [],
            settings=json.loads(user.settings) if user.settings else {},
            enterprise_client_id=user.enterprise_client_id,
            created_by=user.created_by
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enterprise user ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enterprise user update error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating enterprise user"
        )


def delete_enterprise_user_service(user_id: str, db: Session) -> bool:
    """Delete enterprise user"""
    try:
        # Convert string to UUID
        user_uuid = UUID(user_id)
        statement = select(EnterpriseUser).where(EnterpriseUser.id == user_uuid)
        user = db.exec(statement).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enterprise user not found"
            )
        
        db.delete(user)
        db.commit()
        
        logger.info(f"Enterprise user deleted successfully: {user.email}")
        return True
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enterprise user ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enterprise user deletion error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting enterprise user"
        )


def verify_enterprise_user_password_service(user: EnterpriseUser, password: str) -> bool:
    """Verify enterprise user password"""
    return verify_password(password, user.password)


def activate_enterprise_user_service(user_id: str, db: Session) -> EnterpriseUserResponse:
    """Activate an enterprise user"""
    try:
        user_uuid = UUID(user_id)
        statement = select(EnterpriseUser).where(EnterpriseUser.id == user_uuid)
        user = db.exec(statement).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enterprise user not found"
            )
        
        user.is_active = True
        user.updated_at = datetime.now()
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"Enterprise user activated: {user.email}")
        
        return EnterpriseUserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            user_type=user.user_type,
            department=user.department,
            position=user.position,
            phone=user.phone,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            role_ids=json.loads(user.role_ids) if user.role_ids else [],
            permissions=json.loads(user.permissions) if user.permissions else [],
            settings=json.loads(user.settings) if user.settings else {},
            enterprise_client_id=user.enterprise_client_id,
            created_by=user.created_by
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enterprise user ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enterprise user activation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error activating enterprise user"
        )


def deactivate_enterprise_user_service(user_id: str, db: Session) -> EnterpriseUserResponse:
    """Deactivate an enterprise user"""
    try:
        user_uuid = UUID(user_id)
        statement = select(EnterpriseUser).where(EnterpriseUser.id == user_uuid)
        user = db.exec(statement).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enterprise user not found"
            )
        
        user.is_active = False
        user.updated_at = datetime.now()
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"Enterprise user deactivated: {user.email}")
        
        return EnterpriseUserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            user_type=user.user_type,
            department=user.department,
            position=user.position,
            phone=user.phone,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            role_ids=json.loads(user.role_ids) if user.role_ids else [],
            permissions=json.loads(user.permissions) if user.permissions else [],
            settings=json.loads(user.settings) if user.settings else {},
            enterprise_client_id=user.enterprise_client_id,
            created_by=user.created_by
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enterprise user ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enterprise user deactivation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deactivating enterprise user"
        )


def update_enterprise_user_settings_service(user_id: str, settings: dict, db: Session) -> EnterpriseUserResponse:
    """Update enterprise user settings"""
    try:
        user_uuid = UUID(user_id)
        statement = select(EnterpriseUser).where(EnterpriseUser.id == user_uuid)
        user = db.exec(statement).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enterprise user not found"
            )
        
        # Update settings
        user.settings = json.dumps(settings)
        user.updated_at = datetime.now()
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"Enterprise user settings updated for: {user.email}")
        
        return EnterpriseUserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            user_type=user.user_type,
            department=user.department,
            position=user.position,
            phone=user.phone,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            role_ids=json.loads(user.role_ids) if user.role_ids else [],
            permissions=json.loads(user.permissions) if user.permissions else [],
            settings=settings,
            enterprise_client_id=user.enterprise_client_id,
            created_by=user.created_by
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enterprise user ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enterprise user settings update error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating enterprise user settings"
        )
