"""
Main Admin controller with functional approach for 3-level SaaS system
"""
from typing import Optional, List
from uuid import UUID
from sqlmodel import Session, select
from fastapi import HTTPException, status
import json
from ..models.main_admin_user_model import (
    MainAdminUser, MainAdminUserCreate, MainAdminUserUpdate, MainAdminUserResponse
)
from ..models.main_admin_role_model import (
    MainAdminRole, MainAdminRoleCreate, MainAdminRoleUpdate, MainAdminRoleResponse
)
from ..models.main_admin_permission_model import (
    MainAdminPermission, MainAdminPermissionCreate, MainAdminPermissionUpdate, MainAdminPermissionResponse
)
from ..models.enterprise_client_model import (
    EnterpriseClient, EnterpriseClientCreate, EnterpriseClientUpdate, EnterpriseClientResponse
)
from ..utils.database_dependency import get_database_session
from ..utils.my_logger import get_logger
from ..utils.auth_utils import get_password_hash, verify_password

logger = get_logger("MAIN_ADMIN_CONTROLLER")

# ==================== MAIN ADMIN USER FUNCTIONS ====================

def create_main_admin_user(user_data: MainAdminUserCreate, db: Session) -> MainAdminUserResponse:
    """Create a new main admin user"""
    try:
        # Check if email already exists
        existing_user = get_main_admin_user_by_email(user_data.email, db)
        if existing_user:
            logger.warning(f"User creation failed: email {user_data.email} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        
        # Check if username already exists
        existing_username = get_main_admin_user_by_username(user_data.username, db)
        if existing_username:
            logger.warning(f"User creation failed: username {user_data.username} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Convert permissions list to JSON string
        permissions_json = json.dumps(user_data.permissions)
        
        # Create user object
        user = MainAdminUser(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            password=hashed_password,
            role_id=user_data.role_id,
            permissions=permissions_json
        )
        
        # Save to database
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"Main admin user created successfully: {user.email}")
        
        return MainAdminUserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            role_id=user.role_id,
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

def get_main_admin_user_by_email(email: str, db: Session) -> Optional[MainAdminUser]:
    """Get main admin user by email"""
    try:
        statement = select(MainAdminUser).where(MainAdminUser.email == email)
        return db.exec(statement).first()
    except Exception as e:
        logger.error(f"Error getting user by email: {e}")
        return None

def get_main_admin_user_by_username(username: str, db: Session) -> Optional[MainAdminUser]:
    """Get main admin user by username"""
    try:
        statement = select(MainAdminUser).where(MainAdminUser.username == username)
        return db.exec(statement).first()
    except Exception as e:
        logger.error(f"Error getting user by username: {e}")
        return None

def get_main_admin_user_by_id(user_id: str, db: Session) -> Optional[MainAdminUserResponse]:
    """Get main admin user by ID"""
    try:
        # Convert string to UUID
        user_uuid = UUID(user_id)
        statement = select(MainAdminUser).where(MainAdminUser.id == user_uuid)
        user = db.exec(statement).first()
        
        if not user:
            return None
        
        # Convert JSON permissions back to list
        permissions = json.loads(user.permissions) if user.permissions else []
        
        return MainAdminUserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            role_id=user.role_id,
            permissions=permissions
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        return None
    except Exception as e:
        logger.error(f"Error getting user by ID: {e}")
        return None

def get_all_main_admin_users(db: Session) -> List[MainAdminUserResponse]:
    """Get all main admin users"""
    try:
        statement = select(MainAdminUser)
        users = db.exec(statement).all()
        
        return [
            MainAdminUserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                full_name=user.full_name,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
                role_id=user.role_id,
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

def update_main_admin_user(user_id: str, user_data: MainAdminUserUpdate, db: Session) -> MainAdminUserResponse:
    """Update main admin user"""
    try:
        # Convert string to UUID
        user_uuid = UUID(user_id)
        statement = select(MainAdminUser).where(MainAdminUser.id == user_uuid)
        user = db.exec(statement).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check if new email already exists (if email is being updated)
        if user_data.email and user_data.email != user.email:
            existing_user = get_main_admin_user_by_email(user_data.email, db)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )
        
        # Check if new username already exists (if username is being updated)
        if user_data.username and user_data.username != user.username:
            existing_username = get_main_admin_user_by_username(user_data.username, db)
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
                elif field == "permissions" and value is not None:
                    value = json.dumps(value)
                setattr(user, field, value)
        
        # Update timestamp
        from datetime import datetime
        user.updated_at = datetime.utcnow()
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"Main admin user updated successfully: {user.email}")
        
        return MainAdminUserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            role_id=user.role_id,
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

def delete_main_admin_user(user_id: str, db: Session) -> bool:
    """Delete main admin user"""
    try:
        # Convert string to UUID
        user_uuid = UUID(user_id)
        statement = select(MainAdminUser).where(MainAdminUser.id == user_uuid)
        user = db.exec(statement).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        db.delete(user)
        db.commit()
        
        logger.info(f"Main admin user deleted successfully: {user.email}")
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

# ==================== MAIN ADMIN ROLE FUNCTIONS ====================

def create_main_admin_role(role_data: MainAdminRoleCreate, db: Session) -> MainAdminRoleResponse:
    """Create a new main admin role"""
    try:
        # Check if role name already exists
        existing_role = get_main_admin_role_by_name(role_data.name, db)
        if existing_role:
            logger.warning(f"Role creation failed: name {role_data.name} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role name already exists"
            )
        
        # Create role object
        role = MainAdminRole(
            name=role_data.name,
            description=role_data.description,
            is_system_role=role_data.is_system_role
        )
        
        # Save to database
        db.add(role)
        db.commit()
        db.refresh(role)
        
        logger.info(f"Main admin role created successfully: {role.name}")
        
        return MainAdminRoleResponse(
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

def get_main_admin_role_by_name(role_name: str, db: Session) -> Optional[MainAdminRole]:
    """Get main admin role by name"""
    try:
        statement = select(MainAdminRole).where(MainAdminRole.name == role_name)
        return db.exec(statement).first()
    except Exception as e:
        logger.error(f"Error getting role by name: {e}")
        return None

def get_main_admin_role_by_id(role_id: str, db: Session) -> Optional[MainAdminRoleResponse]:
    """Get main admin role by ID"""
    try:
        # Convert string to UUID
        role_uuid = UUID(role_id)
        statement = select(MainAdminRole).where(MainAdminRole.id == role_uuid)
        role = db.exec(statement).first()
        
        if not role:
            return None
        
        return MainAdminRoleResponse(
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

def get_all_main_admin_roles(db: Session) -> List[MainAdminRoleResponse]:
    """Get all main admin roles"""
    try:
        statement = select(MainAdminRole)
        roles = db.exec(statement).all()
        
        return [
            MainAdminRoleResponse(
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

# ==================== MAIN ADMIN PERMISSION FUNCTIONS ====================

def create_main_admin_permission(permission_data: MainAdminPermissionCreate, db: Session) -> MainAdminPermissionResponse:
    """Create a new main admin permission"""
    try:
        # Check if permission name already exists
        existing_permission = get_main_admin_permission_by_name(permission_data.name, db)
        if existing_permission:
            logger.warning(f"Permission creation failed: name {permission_data.name} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Permission name already exists"
            )
        
        # Create permission object
        permission = MainAdminPermission(
            name=permission_data.name,
            description=permission_data.description,
            action=permission_data.action,
            resource=permission_data.resource
        )
        
        # Save to database
        db.add(permission)
        db.commit()
        db.refresh(permission)
        
        logger.info(f"Main admin permission created successfully: {permission.name}")
        
        return MainAdminPermissionResponse(
            id=permission.id,
            name=permission.name,
            description=permission.description,
            action=permission.action,
            resource=permission.resource,
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

def get_main_admin_permission_by_name(permission_name: str, db: Session) -> Optional[MainAdminPermission]:
    """Get main admin permission by name"""
    try:
        statement = select(MainAdminPermission).where(MainAdminPermission.name == permission_name)
        return db.exec(statement).first()
    except Exception as e:
        logger.error(f"Error getting permission by name: {e}")
        return None

def get_all_main_admin_permissions(db: Session) -> List[MainAdminPermissionResponse]:
    """Get all main admin permissions"""
    try:
        statement = select(MainAdminPermission)
        permissions = db.exec(statement).all()
        
        return [
            MainAdminPermissionResponse(
                id=permission.id,
                name=permission.name,
                description=permission.description,
                action=permission.action,
                resource=permission.resource,
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

# ==================== ENTERPRISE CLIENT FUNCTIONS ====================

def create_enterprise_client(client_data: EnterpriseClientCreate, db: Session) -> EnterpriseClientResponse:
    """Create a new enterprise client"""
    try:
        # Check if email already exists
        existing_client = get_enterprise_client_by_email(client_data.email, db)
        if existing_client:
            logger.warning(f"Enterprise client creation failed: email {client_data.email} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        
        # Create client object
        client = EnterpriseClient(
            name=client_data.name,
            email=client_data.email,
            contact_person=client_data.contact_person,
            phone=client_data.phone,
            address=client_data.address
        )
        
        # Save to database
        db.add(client)
        db.commit()
        db.refresh(client)
        
        logger.info(f"Enterprise client created successfully: {client.name}")
        
        return EnterpriseClientResponse(
            id=client.id,
            name=client.name,
            email=client.email,
            contact_person=client.contact_person,
            phone=client.phone,
            address=client.address,
            is_active=client.is_active,
            created_at=client.created_at,
            updated_at=client.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enterprise client creation error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating enterprise client"
        )

def get_enterprise_client_by_email(email: str, db: Session) -> Optional[EnterpriseClient]:
    """Get enterprise client by email"""
    try:
        statement = select(EnterpriseClient).where(EnterpriseClient.email == email)
        return db.exec(statement).first()
    except Exception as e:
        logger.error(f"Error getting enterprise client by email: {e}")
        return None

def get_enterprise_client_by_id(client_id: str, db: Session) -> Optional[EnterpriseClientResponse]:
    """Get enterprise client by ID"""
    try:
        # Convert string to UUID
        client_uuid = UUID(client_id)
        statement = select(EnterpriseClient).where(EnterpriseClient.id == client_uuid)
        client = db.exec(statement).first()
        
        if not client:
            return None
        
        return EnterpriseClientResponse(
            id=client.id,
            name=client.name,
            email=client.email,
            contact_person=client.contact_person,
            phone=client.phone,
            address=client.address,
            is_active=client.is_active,
            created_at=client.created_at,
            updated_at=client.updated_at
        )
        
    except ValueError as e:
        logger.error(f"Invalid UUID format: {e}")
        return None
    except Exception as e:
        logger.error(f"Error getting enterprise client by ID: {e}")
        return None

def get_all_enterprise_clients(db: Session) -> List[EnterpriseClientResponse]:
    """Get all enterprise clients"""
    try:
        statement = select(EnterpriseClient)
        clients = db.exec(statement).all()
        
        return [
            EnterpriseClientResponse(
                id=client.id,
                name=client.name,
                email=client.email,
                contact_person=client.contact_person,
                phone=client.phone,
                address=client.address,
                is_active=client.is_active,
                created_at=client.created_at,
                updated_at=client.updated_at
            )
            for client in clients
        ]
        
    except Exception as e:
        logger.error(f"Error getting all enterprise clients: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving enterprise clients"
        )
