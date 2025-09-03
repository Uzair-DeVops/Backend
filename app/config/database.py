import sys
import os
from pathlib import Path
from urllib.parse import urlparse, unquote
from sqlmodel import SQLModel, create_engine, Session, text
from .my_settings import settings
from ..utils.my_logger import get_logger


def initialize_database_engine():
    """
    Initialize SQLite SQLModel engine
    """
    try:
        get_logger(name="UZAIR").info("🔧 Initializing Database engine...")
        # Create SQLModel engine for SQLite ORM operations
        if settings.DATABASE_URL:
            database_url = settings.DATABASE_URL
        else:
            get_logger(name="UZAIR").error("❌ DATABASE_URL not configured")
            return None
            
        # For SQLite, we don't need connection pooling settings
        engine = create_engine(
            database_url,
            echo=True,  # Set to False in production
            connect_args={"check_same_thread": False}  # Required for SQLite with FastAPI
        )
        
        # test connection by executing a simple query
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        get_logger(name="UZAIR").info("✅ Database engine initialized successfully")
        return engine
    except Exception as e:
        get_logger(name="UZAIR").error(f"❌ Could not initialize Database engine: {e}")
        return None
