"""
Database initialization and table creation for Main Admin system
"""
import json
from sqlmodel import SQLModel, create_engine, Session
from .database import initialize_database_engine
from .my_settings import settings
# Main Admin Level Models
from ..models.admin_user_model import AdminUser
from ..models.admin_role_model import AdminRole
from ..models.admin_permission_model import AdminPermission
from ..models.enterprise_client_model import EnterpriseClient
from ..utils.my_logger import get_logger
from ..utils.auth_utils import get_password_hash

logger = get_logger("DB_INIT")

def create_tables() -> bool:
    """Create all database tables"""
    try:
        # Initialize database engine
        engine = initialize_database_engine()
        if not engine:
            logger.error("❌ Failed to initialize database engine")
            return False
        
        # Create all tables
        SQLModel.metadata.create_all(engine)
        
        # Initialize default main admin data
        initialize_default_main_admin_data(engine)
        
        logger.info("✅ Database tables created successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creating database tables: {e}")
        return False

def initialize_default_main_admin_data(engine):
    """Initialize default main admin roles, permissions, and admin user"""
    try:
        with Session(engine) as session:
            # Create default main admin permissions first
            create_default_admin_permissions(session)
            
            # Create default main admin roles
            create_default_admin_roles(session)
            
            # Create default enterprise client role
            create_default_admin_client_role(session)
            
            # Create default main admin user
            create_default_admin_user(session)
            
            session.commit()
            logger.info("✅ Default main admin data initialized successfully")
            
    except Exception as e:
        logger.error(f"❌ Error initializing default main admin data: {e}")
        raise

def create_default_admin_roles(session: Session):
    """Create default main admin roles"""
    # First, get all permissions to assign to main_admin role
    all_permissions = session.query(AdminPermission).all()
    all_permission_ids = [str(permission.id) for permission in all_permissions]
    
    # Get specific permissions for different roles
    finance_permissions = session.query(AdminPermission).filter(
        AdminPermission.name.in_([
            "view_enterprise",
            "view_main_admin_users"
        ])
    ).all()
    finance_permission_ids = [str(permission.id) for permission in finance_permissions]
    
    support_permissions = session.query(AdminPermission).filter(
        AdminPermission.name.in_([
            "view_enterprise",
            "view_main_admin_users"
        ])
    ).all()
    support_permission_ids = [str(permission.id) for permission in support_permissions]
    
    account_permissions = session.query(AdminPermission).filter(
        AdminPermission.name.in_([
            "view_enterprise",
            "update_enterprise",
            "view_main_admin_users"
        ])
    ).all()
    account_permission_ids = [str(permission.id) for permission in account_permissions]
    
    default_roles = [
        {
            "name": "main_admin",
            "description": "Main system administrator with full access",
            "is_system_role": True,
            "permissions": json.dumps(all_permission_ids)
        },
        {
            "name": "finance_manager",
            "description": "Finance team manager",
            "is_system_role": False,
            "permissions": json.dumps(finance_permission_ids)
        },
        {
            "name": "support_manager",
            "description": "Support team manager",
            "is_system_role": False,
            "permissions": json.dumps(support_permission_ids)
        },
        {
            "name": "account_manager",
            "description": "Account management team",
            "is_system_role": False,
            "permissions": json.dumps(account_permission_ids)
        }
    ]
    
    for role_data in default_roles:
        existing_role = session.query(AdminRole).filter(AdminRole.name == role_data["name"]).first()
        if not existing_role:
            role = AdminRole(**role_data)
            session.add(role)
            logger.info(f"Created default main admin role: {role_data['name']}")

def create_default_admin_permissions(session: Session):
    """Create default main admin permissions"""
    default_permissions = [
        {
            "name": "create_enterprise",
            "description": "Create new enterprise clients",
            "action": "create",
            "resource": "enterprise"
        },
        {
            "name": "view_enterprise",
            "description": "View enterprise client information",
            "action": "read",
            "resource": "enterprise"
        },
        {
            "name": "update_enterprise",
            "description": "Update enterprise client information",
            "action": "update",
            "resource": "enterprise"
        },
        {
            "name": "delete_enterprise",
            "description": "Delete enterprise clients",
            "action": "delete",
            "resource": "enterprise"
        },
        {
            "name": "create_main_admin_user",
            "description": "Create main admin users",
            "action": "create",
            "resource": "main_admin_user"
        },
        {
            "name": "view_main_admin_users",
            "description": "View main admin users",
            "action": "read",
            "resource": "main_admin_user"
        },
        {
            "name": "update_main_admin_user",
            "description": "Update main admin users",
            "action": "update",
            "resource": "main_admin_user"
        },
        {
            "name": "delete_main_admin_user",
            "description": "Delete main admin users",
            "action": "delete",
            "resource": "main_admin_user"
        },
        {
            "name": "manage_roles",
            "description": "Manage roles and permissions",
            "action": "manage",
            "resource": "role"
        }
    ]
    
    for permission_data in default_permissions:
        existing_permission = session.query(AdminPermission).filter(AdminPermission.name == permission_data["name"]).first()
        if not existing_permission:
            permission = AdminPermission(**permission_data)
            session.add(permission)
            logger.info(f"Created default main admin permission: {permission_data['name']}")

def create_default_admin_user(session: Session):
    """Create default main admin user"""
    # Check if main admin user already exists
    existing_admin = session.query(AdminUser).filter(AdminUser.email == "mainadmin@example.com").first()
    if existing_admin:
        logger.info("Default main admin user already exists")
        return
    
    # Get main admin role
    main_admin_role = session.query(AdminRole).filter(AdminRole.name == "main_admin").first()
    if not main_admin_role:
        logger.error("Main admin role not found, cannot create main admin user")
        return
    
    # Get all permissions for main admin
    all_permissions = session.query(AdminPermission).all()
    permission_ids = [str(permission.id) for permission in all_permissions]
    
    # Create main admin user with multiple roles (for now just main_admin role)
    role_ids = [str(main_admin_role.id)]
    
    # Create main admin user
    main_admin_user = AdminUser(
        email="mainadmin@example.com",
        username="mainadmin",
        full_name="Main System Administrator",
        password=get_password_hash("mainadmin123"),  # Default password
        role_ids=json.dumps(role_ids),  # JSON string of role IDs
        permissions=json.dumps(permission_ids)  # JSON string of permission IDs
    )
    
    session.add(main_admin_user)
    
    logger.info("✅ Default main admin user created successfully")
    logger.info("📧 Main Admin Email: mainadmin@example.com")
    logger.info("🔑 Main Admin Password: mainadmin123")
    logger.info("⚠️  Please change the main admin password after first login!")

def create_default_admin_client_role(session: Session):
    """Create default enterprise client role"""
    # Check if enterprise client role already exists
    existing_role = session.query(AdminRole).filter(AdminRole.name == "enterprise_client").first()
    if existing_role:
        logger.info("Default admin client role already exists")
        return
    
    # Get basic permissions for enterprise clients
    basic_permissions = session.query(AdminPermission).filter(
        AdminPermission.name.in_([
            "view_enterprise",
            "update_enterprise"
        ])
    ).all()
    basic_permission_ids = [str(permission.id) for permission in basic_permissions]
    
    # Create enterprise client role
    enterprise_client_role = AdminRole(
        name="enterprise_client",
        description="Default role for enterprise clients",
        is_system_role=True,
        permissions=json.dumps(basic_permission_ids)
    )
    
    session.add(enterprise_client_role)
    logger.info("✅ Default admin client role created successfully")
