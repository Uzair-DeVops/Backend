"""
Services package for business logic layer - Functional approach
"""

# Import all service functions
from .admin_user_service import *
from .admin_role_service import *
from .admin_permission_service import *
from .auth_service import *
from .enterprise_client_service import *
from .enterprise_admin_service import *
from .enterprise_role_service import *
from .enterprise_permission_service import *
from .enterprise_user_service import *
from .end_client_service import *

__all__ = [
    # Admin User Service Functions
    "create_admin_user_service",
    "get_admin_user_by_email_service",
    "get_admin_user_by_username_service", 
    "get_admin_user_by_id_service",
    "get_all_admin_users_service",
    "update_admin_user_service",
    "delete_admin_user_service",
    "verify_user_password_service",
    "activate_user_service",
    "deactivate_user_service",
    
    # Admin Role Service Functions
    "create_admin_role_service",
    "get_admin_role_by_name_service",
    "get_admin_role_by_id_service",
    "get_all_admin_roles_service",
    "update_admin_role_service", 
    "delete_admin_role_service",
    "activate_role_service",
    "deactivate_role_service",
    
    # Admin Permission Service Functions
    "create_admin_permission_service",
    "get_admin_permission_by_name_service",
    "get_admin_permission_by_id_service",
    "get_all_admin_permissions_service",
    "get_permissions_by_resource_service",
    "update_admin_permission_service",
    "delete_admin_permission_service",
    "activate_permission_service",
    "deactivate_permission_service",
    
    # Auth Service Functions
    "create_access_token_service",
    "verify_token_service",
    "authenticate_user_service",
    "get_current_user_service",
    "login_user_service",
    "refresh_token_service",
    "logout_user_service",
    "change_password_service",
    
    # Enterprise Client Service Functions
    "create_enterprise_client_service",
    "get_enterprise_client_by_name_service",
    "get_enterprise_client_by_email_service",
    "get_enterprise_client_by_id_service",
    "get_all_enterprise_clients_service",
    "update_enterprise_client_service",
    "delete_enterprise_client_service",
    "activate_enterprise_client_service",
    "deactivate_enterprise_client_service",
    "update_client_settings_service",
    
    # Enterprise Admin Service Functions
    "create_enterprise_admin_service",
    "get_enterprise_admin_by_email_service",
    "get_enterprise_admin_by_username_service",
    "get_enterprise_admin_by_id_service",
    "get_all_enterprise_admins_service",
    "get_enterprise_admins_by_client_service",
    "update_enterprise_admin_service",
    "delete_enterprise_admin_service",
    "verify_enterprise_admin_password_service",
    "activate_enterprise_admin_service",
    "deactivate_enterprise_admin_service",
    
    # Enterprise Role Service Functions
    "create_enterprise_role_service",
    "get_enterprise_role_by_name_service",
    "get_enterprise_role_by_id_service",
    "get_all_enterprise_roles_service",
    "get_enterprise_roles_by_client_service",
    "update_enterprise_role_service",
    "delete_enterprise_role_service",
    "activate_enterprise_role_service",
    "deactivate_enterprise_role_service",
    
    # Enterprise Permission Service Functions
    "create_enterprise_permission_service",
    "get_enterprise_permission_by_name_service",
    "get_enterprise_permission_by_id_service",
    "get_all_enterprise_permissions_service",
    "get_enterprise_permissions_by_client_service",
    "get_enterprise_permissions_by_resource_service",
    "update_enterprise_permission_service",
    "delete_enterprise_permission_service",
    "activate_enterprise_permission_service",
    "deactivate_enterprise_permission_service",
    
    # Enterprise User Service Functions
    "create_enterprise_user_service",
    "get_enterprise_user_by_email_service",
    "get_enterprise_user_by_username_service",
    "get_enterprise_user_by_id_service",
    "get_all_enterprise_users_service",
    "get_enterprise_users_by_client_service",
    "get_enterprise_users_by_type_service",
    "get_enterprise_users_by_creator_service",
    "update_enterprise_user_service",
    "delete_enterprise_user_service",
    "verify_enterprise_user_password_service",
    "activate_enterprise_user_service",
    "deactivate_enterprise_user_service",
    "update_enterprise_user_settings_service",
    
    # End Client Service Functions
    "create_end_client_service",
    "get_end_client_by_email_service",
    "get_end_client_by_id_service",
    "get_all_end_clients_service",
    "get_end_clients_by_enterprise_service",
    "get_end_clients_by_creator_service",
    "update_end_client_service",
    "delete_end_client_service",
    "activate_end_client_service",
    "deactivate_end_client_service",
    "update_end_client_settings_service"
]
