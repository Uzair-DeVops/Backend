"""
App routes package
"""

# Import routes when they exist
from .user_routes import router as user_router
from .role_routes import router as role_router
from .scope_routes import router as scope_router
from .rbac_routes import router as rbac_router

__all__ = [
    "user_router",
    "role_router",
    "scope_router",
    "rbac_router",
]
