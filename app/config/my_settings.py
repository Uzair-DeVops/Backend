from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")

    # Other settings
    PORT: int = int(os.getenv("PORT", "8000"))


    
    class Config:
        env_file = ".env"

settings = Settings() 