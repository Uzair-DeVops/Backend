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


def _convert_id_to_user(user_id: str, db: Session) -> Optional[AdminUser]:
    """Helper function to convert ID (hex string or integer position) to user object"""
    try:
        # Try to find by the exact ID string first (for hex IDs)
        statement = select(AdminUser).where(AdminUser.id == user_id)
        user = db.exec(statement).first()
        
        if not user:
            # If not found, try to find by position/index (for integer IDs)
            try:
                int_id = int(user_id)
                if int_id > 0:
                    # Get all users and find by position (1-based index)
                    all_users = db.exec(select(AdminUser)).all()
                    if 0 < int_id <= len(all_users):
                        user = all_users[int_id - 1]  # Convert to 0-based index
                        logger.info(f"Found user by position {int_id}: {user.email}")
                    else:
                        logger.warning(f"Position {int_id} out of range. Total users: {len(all_users)}")
                        return None
                else:
                    logger.warning(f"Invalid position: {int_id}")
                    return None
            except ValueError:
                logger.warning(f"Invalid ID format: {user_id}")
                return None
        
        return user
        
    except Exception as e:
        logger.error(f"Error converting ID to user: {e}")
        return None


def _get_user_permissions_from_roles(user: AdminUser, db: Session) -> List[str]:
    """Helper function to get actual permissions from user's assigned roles"""
    try:
        role_permissions = []
        if user.role_ids:
            from ..models.admin_role_model import AdminRole
            role_ids = json.loads(user.role_ids)
            for role_id in role_ids:
                # Normalize UUID format (remove hyphens for database lookup)
                normalized_role_id = role_id.replace('-', '')
                role = db.exec(select(AdminRole).where(AdminRole.id == normalized_role_id)).first()
                if role and role.permissions:
                    try:
                        role_perms = json.loads(role.permissions)
                        role_permissions.extend(role_perms)
                    except json.JSONDecodeError:
                        logger.warning(f"Invalid permissions JSON for role {role_id}")
        
        # Also include any direct permissions assigned to the user
        user_permissions = []
        if user.permissions:
            try:
                user_perms = json.loads(user.permissions)
                user_permissions.extend(user_perms)
            except json.JSONDecodeError:
                logger.warning(f"Invalid permissions JSON for user {user.id}")
        
        # Combine and remove duplicates
        all_permissions = list(set(role_permissions + user_permissions))
        return all_permissions
        
    except Exception as e:
        logger.error(f"Error getting user permissions from roles: {e}")
        return []


def _get_permission_names_from_ids(permission_ids: List[str], db: Session) -> List[str]:
    """Helper function to convert permission IDs to permission names"""
    try:
        if not permission_ids:
            return []
        
        from ..models.admin_permission_model import AdminPermission
        permission_names = []
        
        for perm_id in permission_ids:
            # Normalize UUID format (remove hyphens for database lookup)
            normalized_perm_id = perm_id.replace('-', '')
            permission = db.exec(select(AdminPermission).where(AdminPermission.id == normalized_perm_id)).first()
            if permission:
                permission_names.append(permission.name)
            else:
                logger.warning(f"Permission with ID {perm_id} not found")
        
        return permission_names
        
    except Exception as e:
        logger.error(f"Error getting permission names from IDs: {e}")
        return []


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
        
        # Get permissions from assigned roles
        role_permissions = []
        if user_data.role_ids:
            from ..models.admin_role_model import AdminRole
            for role_id in user_data.role_ids:
                # Normalize UUID format (remove hyphens for database lookup)
                normalized_role_id = role_id.replace('-', '')
                logger.info(f"Looking up role: original_id={role_id}, normalized_id={normalized_role_id}")
                
                try:
                    role = db.exec(select(AdminRole).where(AdminRole.id == normalized_role_id)).first()
                    logger.info(f"Role lookup result: {role.name if role else 'Not found'}")
                    
                    if role and role.permissions:
                        try:
                            role_perms = json.loads(role.permissions)
                            role_permissions.extend(role_perms)
                            logger.info(f"Added {len(role_perms)} permissions from role {role.name}")
                        except json.JSONDecodeError:
                            logger.warning(f"Invalid permissions JSON for role {role_id}")
                except Exception as e:
                    logger.error(f"Error looking up role {role_id}: {e}")
                    continue
        
        # Combine role permissions with any additional permissions passed in request
        all_permissions = list(set(role_permissions + user_data.permissions))  # Remove duplicates
        
        # Convert role_ids and permissions lists to JSON strings
        role_ids_json = json.dumps(user_data.role_ids)
        permissions_json = json.dumps(all_permissions)
        
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
            permissions=all_permissions,  # Return the actual permissions from roles
            permission_names=_get_permission_names_from_ids(all_permissions, db)
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
    """Get admin user by ID - Supports both hex strings and simple integers"""
    try:
        user = _convert_id_to_user(user_id, db)
        
        if not user:
            return None
        
        # Get actual permissions from roles
        role_ids = json.loads(user.role_ids) if user.role_ids else []
        permissions = _get_user_permissions_from_roles(user, db)
        
        return AdminUserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            role_ids=role_ids,
            permissions=permissions,
            permission_names=_get_permission_names_from_ids(permissions, db)
        )
        
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
                permissions=_get_user_permissions_from_roles(user, db),
                permission_names=_get_permission_names_from_ids(_get_user_permissions_from_roles(user, db), db)
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
    """Update admin user - Supports both hex strings and simple integers"""
    try:
        user = _convert_id_to_user(user_id, db)
        
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
        user.updated_at = datetime.utcnow()
        
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
            permissions=_get_user_permissions_from_roles(user, db),
            permission_names=_get_permission_names_from_ids(_get_user_permissions_from_roles(user, db), db)
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
    """Delete admin user - Supports both hex strings and simple integers"""
    try:
        user = _convert_id_to_user(user_id, db)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        db.delete(user)
        db.commit()
        
        logger.info(f"Admin user deleted successfully: {user.email}")
        return True
        
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
    """Activate a user account - Supports both hex strings and simple integers"""
    try:
        user = _convert_id_to_user(user_id, db)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user.is_active = True
        user.updated_at = datetime.utcnow()
        
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
            permissions=_get_user_permissions_from_roles(user, db),
            permission_names=_get_permission_names_from_ids(_get_user_permissions_from_roles(user, db), db)
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
    """Deactivate a user account - Supports both hex strings and simple integers"""
    try:
        user = _convert_id_to_user(user_id, db)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user.is_active = False
        user.updated_at = datetime.utcnow()
        
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
            permissions=_get_user_permissions_from_roles(user, db),
            permission_names=_get_permission_names_from_ids(_get_user_permissions_from_roles(user, db), db)
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

