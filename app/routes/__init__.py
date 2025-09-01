"""
App routes package
"""

# Import admin routes
from .admin_user_routes import router as admin_user_router
from .admin_role_routes import router as admin_role_router
from .admin_permission_routes import router as admin_permission_router
from .enterprise_client_routes import router as enterprise_client_router

# Import enterprise admin routes
from .enterprise_admin_routes import router as enterprise_admin_router

# Import enterprise role routes
from .enterprise_role_routes import router as enterprise_role_router

# Import enterprise permission routes
from .enterprise_permission_routes import router as enterprise_permission_router

# Import enterprise user routes
from .enterprise_user_routes import router as enterprise_user_router

# Import end client routes
from .end_client_routes import router as end_client_router

# Import auth routes
from .auth_routes import auth_router

__all__ = [
    "admin_user_router",
    "admin_role_router", 
    "admin_permission_router",
    "enterprise_client_router",
    "enterprise_admin_router",
    "enterprise_role_router",
    "enterprise_permission_router",
    "enterprise_user_router",
    "end_client_router",
    "auth_router",
]
