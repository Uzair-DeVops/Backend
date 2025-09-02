from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from .config.database import (
    initialize_database_engine,
)
from .config.init_db import create_tables
from .utils.my_logger import get_logger
from .config.my_settings import settings
from .routes import (
    admin_user_router,
    admin_role_router,
    admin_permission_router,
    enterprise_client_router,
    enterprise_admin_router,
    enterprise_role_router,
    enterprise_permission_router,
    enterprise_user_router,
    end_client_router,
    auth_router
)
# LIFESPAN
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    await startup_event(app)

    # This is where the app runs (yield)
    yield 

    # Shutdown event
    await shutdown_event(app)

# FASTAPI APP
app = FastAPI(
    version="0.1.0",
    # lifespan=lifespan  
)

# CORS MIDDLEWARE
# ROUTES
app.include_router(auth_router, prefix="/auth")
app.include_router(admin_user_router)
app.include_router(admin_role_router)
app.include_router(admin_permission_router)
app.include_router(enterprise_client_router)
app.include_router(enterprise_admin_router)
app.include_router(enterprise_role_router)
app.include_router(enterprise_permission_router)
app.include_router(enterprise_user_router)
app.include_router(end_client_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# STARTUP EVENT
async def startup_event(app: FastAPI):
    get_logger(name="UZAIR").info("🚀 Starting up Data Migration Project...")
    
    # Initialize and store in app.state
    app.state.database_engine = initialize_database_engine()
    
    # Create database tables
    try:
        success = create_tables()
        if success:
            get_logger(name="UZAIR").info("✅ Database tables created successfully")
        else:
            get_logger(name="UZAIR").error("❌ Failed to create database tables")
    except Exception as e:
        get_logger(name="UZAIR").error(f"❌ Error creating database tables: {e}")

# ROOT REDIRECT TO DOCS
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

# HEALTH CHECK
@app.get("/health")
async def health_check():
    return {"status": "The server is running successfully"}

# SHUTDOWN EVENT
async def shutdown_event(app: FastAPI):
    get_logger(name="UZAIR").info("🛑 Shutting down Data Migration Project...")
   