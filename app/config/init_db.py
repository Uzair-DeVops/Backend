"""
Database initialization and table creation
"""
from sqlmodel import SQLModel, create_engine, Session
from .database import initialize_database_engine
from .my_settings import settings
from ..models.user_model import UserCreate, UserCreateWithRoles
from ..models.role_model import Role
from ..models.scope_model import Scope
from ..models.user_role_model import UserRole
from ..models.role_scope_model import RoleScope
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
        
        # Initialize default data
        initialize_default_data(engine)
        
        logger.info("✅ Database tables created successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creating database tables: {e}")
        return False

def initialize_default_data(engine):
    """Initialize default roles, scopes, and admin user"""
    try:
        with Session(engine) as session:
            # Create default roles
            create_default_roles(session)
            
            # Create default scopes
            create_default_scopes(session)
            
            # Create default admin user
            create_default_admin(session)
            
            session.commit()
            logger.info("✅ Default data initialized successfully")
            
    except Exception as e:
        logger.error(f"❌ Error initializing default data: {e}")
        raise

def create_default_roles(session: Session):
    """Create default roles if they don't exist"""
    default_roles = [
        {
            "name": "admin",
            "description": "Administrator with full system access",
            "is_system_role": True
        },
        {
            "name": "user",
            "description": "Regular user with basic access",
            "is_system_role": True
        },
        {
            "name": "moderator",
            "description": "Moderator with limited administrative access",
            "is_system_role": True
        }
    ]
    
    for role_data in default_roles:
        existing_role = session.query(Role).filter(Role.name == role_data["name"]).first()
        if not existing_role:
            role = Role(**role_data)
            session.add(role)
            logger.info(f"Created default role: {role_data['name']}")

def create_default_scopes(session: Session):
    """Create default scopes if they don't exist"""
    default_scopes = [
        {
            "name": "user:read",
            "description": "Read user information",
            "resource": "user",
            "action": "read"
        },
        {
            "name": "user:write",
            "description": "Create and update users",
            "resource": "user",
            "action": "write"
        },
        {
            "name": "user:delete",
            "description": "Delete users",
            "resource": "user",
            "action": "delete"
        },
        {
            "name": "role:read",
            "description": "Read role information",
            "resource": "role",
            "action": "read"
        },
        {
            "name": "role:write",
            "description": "Create and update roles",
            "resource": "role",
            "action": "write"
        },
        {
            "name": "role:delete",
            "description": "Delete roles",
            "resource": "role",
            "action": "delete"
        },
        {
            "name": "scope:read",
            "description": "Read scope information",
            "resource": "scope",
            "action": "read"
        },
        {
            "name": "scope:write",
            "description": "Create and update scopes",
            "resource": "scope",
            "action": "write"
        },
        {
            "name": "scope:delete",
            "description": "Delete scopes",
            "resource": "scope",
            "action": "delete"
        }
    ]
    
    for scope_data in default_scopes:
        existing_scope = session.query(Scope).filter(Scope.name == scope_data["name"]).first()
        if not existing_scope:
            scope = Scope(**scope_data)
            session.add(scope)
            logger.info(f"Created default scope: {scope_data['name']}")

def create_default_admin(session: Session):
    """Create default admin user if it doesn't exist"""
    # Check if admin user already exists
    existing_admin = session.query(UserCreate).filter(UserCreate.email == "admin@example.com").first()
    if existing_admin:
        logger.info("Default admin user already exists")
        return
    
    # Get admin role
    admin_role = session.query(Role).filter(Role.name == "admin").first()
    if not admin_role:
        logger.error("Admin role not found, cannot create admin user")
        return
    
    # Create admin user
    admin_user = UserCreate(
        email="admin@example.com",
        username="admin",
        full_name="System Administrator",
        password=get_password_hash("admin123"),  # Default password
        is_active=True
    )
    
    session.add(admin_user)
    session.commit()
    session.refresh(admin_user)
    
    # Assign admin role to admin user
    user_role = UserRole(
        user_id=admin_user.id,
        role_id=admin_role.id,
        assigned_by=admin_user.id  # Self-assigned
    )
    
    session.add(user_role)
    
    # Assign all scopes to admin role
    all_scopes = session.query(Scope).all()
    for scope in all_scopes:
        role_scope = RoleScope(
            role_id=admin_role.id,
            scope_id=scope.id
        )
        session.add(role_scope)
    
    logger.info("✅ Default admin user created successfully")
    logger.info("📧 Admin Email: admin@example.com")
    logger.info("🔑 Admin Password: admin123")
    logger.info("⚠️  Please change the admin password after first login!")
