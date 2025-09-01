"""
Admin User Service - Business logic layer for admin user operations (Functional approach)
"""
from typing import Optional, List
from uuid import UUID
from sqlmodel import Session, select
from fastapi import HTTPException, status
import json
from datetime import datetime

from ..models.admin_user_model import (
    AdminUser, AdminUserCreate, AdminUserUpdate, AdminUserResponse
)
from ..utils.my_logger import get_logger
from ..utils.auth_utils import get_password_hash, verify_password

logger = get_logger("ADMIN_USER_SERVICE")


def create_admin_user_service(user_data: AdminUserCreate, db: Session) -> AdminUserResponse:
    """Create a new admin user"""
    try:
        # Check if email already exists
        existing_user = get_admin_user_by_email_service(user_data.email, db)
        if existing_user:
            logger.warning(f"User creation failed: email {user_data.email} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        
        # Check if username already exists
        existing_username = get_admin_user_by_username_service(user_data.username, db)
        if existing_username:
            logger.warning(f"User creation failed: username {user_data.username} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Convert role_ids and permissions lists to JSON strings
        role_ids_json = json.dumps(user_data.role_ids)
        permissions_json = json.dumps(user_data.permissions)
        
        # Create user object
        user = AdminUser(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            password=hashed_password,
            role_ids=role_ids_json,
            permissions=permissions_json
        )
        
        # Save to database
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"Admin user created successfully: {user.email}")
        
        return AdminUserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            role_ids=user_data.role_ids,
            permissions=user_data.permissions
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"User creation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )


def get_admin_user_by_email_service(email: str, db: Session) -> Optional[AdminUser]:
    """Get admin user by email"""
    try:
        statement = select(AdminUser).where(AdminUser.email == email)
        return db.exec(statement).first()
    except Exception as e:
        logger.error(f"Error getting user by email: {e}")
        return None


def get_admin_user_by_username_service(username: str, db: Session) -> Optional[AdminUser]:
    """Get admin user by username"""
    try:
        statement = select(AdminUser).where(AdminUser.username == username)
        return db.exec(statement).first()
    except Exception as e:
        logger.error(f"Error getting user by username: {e}")
        return None


def get_admin_user_by_id_service(user_id: str, db: Session) -> Optional[AdminUserResponse]:
    """Get admin user by ID"""
    try:
        # Convert string to UUID
        user_uuid = UUID(user_id)
        statement = select(AdminUser).where(AdminUser.id == user_uuid)
        user = db.exec(statement).first()
        
        if not user:
            return None
        
        # Convert JSON role_ids and permissions back to lists
        role_ids = json.loads(user.role_ids) if user.role_ids else []
        permissions = json.loads(user.permissions) if user.permissions else []
        
        return AdminUserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            role_ids=role_ids,
            permissions=permissions
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        return None
    except Exception as e:
        logger.error(f"Error getting user by ID: {e}")
        return None


def get_all_admin_users_service(db: Session) -> List[AdminUserResponse]:
    """Get all admin users"""
    try:
        statement = select(AdminUser)
        users = db.exec(statement).all()
        
        return [
            AdminUserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                full_name=user.full_name,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
                role_ids=json.loads(user.role_ids) if user.role_ids else [],
                permissions=json.loads(user.permissions) if user.permissions else []
            )
            for user in users
        ]
        
    except Exception as e:
        logger.error(f"Error getting all users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving users"
        )


def update_admin_user_service(user_id: str, user_data: AdminUserUpdate, db: Session) -> AdminUserResponse:
    """Update admin user"""
    try:
        # Convert string to UUID
        user_uuid = UUID(user_id)
        statement = select(AdminUser).where(AdminUser.id == user_uuid)
        user = db.exec(statement).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check if new email already exists (if email is being updated)
        if user_data.email and user_data.email != user.email:
            existing_user = get_admin_user_by_email_service(user_data.email, db)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )
        
        # Check if new username already exists (if username is being updated)
        if user_data.username and user_data.username != user.username:
            existing_username = get_admin_user_by_username_service(user_data.username, db)
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
                setattr(user, field, value)
        
        # Update timestamp
        user.updated_at = datetime.now()
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"Admin user updated successfully: {user.email}")
        
        return AdminUserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            role_ids=json.loads(user.role_ids) if user.role_ids else [],
            permissions=json.loads(user.permissions) if user.permissions else []
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"User update error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user"
        )


def delete_admin_user_service(user_id: str, db: Session) -> bool:
    """Delete admin user"""
    try:
        # Convert string to UUID
        user_uuid = UUID(user_id)
        statement = select(AdminUser).where(AdminUser.id == user_uuid)
        user = db.exec(statement).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        db.delete(user)
        db.commit()
        
        logger.info(f"Admin user deleted successfully: {user.email}")
        return True
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"User deletion error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting user"
        )


def verify_user_password_service(user: AdminUser, password: str) -> bool:
    """Verify user password"""
    return verify_password(password, user.password)


def activate_user_service(user_id: str, db: Session) -> AdminUserResponse:
    """Activate a user account"""
    try:
        user_uuid = UUID(user_id)
        statement = select(AdminUser).where(AdminUser.id == user_uuid)
        user = db.exec(statement).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user.is_active = True
        user.updated_at = datetime.now()
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"Admin user activated: {user.email}")
        
        return AdminUserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            role_ids=json.loads(user.role_ids) if user.role_ids else [],
            permissions=json.loads(user.permissions) if user.permissions else []
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"User activation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error activating user"
        )


def deactivate_user_service(user_id: str, db: Session) -> AdminUserResponse:
    """Deactivate a user account"""
    try:
        user_uuid = UUID(user_id)
        statement = select(AdminUser).where(AdminUser.id == user_uuid)
        user = db.exec(statement).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user.is_active = False
        user.updated_at = datetime.now()
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"Admin user deactivated: {user.email}")
        
        return AdminUserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            role_ids=json.loads(user.role_ids) if user.role_ids else [],
            permissions=json.loads(user.permissions) if user.permissions else []
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"User deactivation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deactivating user"
        )

