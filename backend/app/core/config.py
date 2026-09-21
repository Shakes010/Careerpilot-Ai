import os
from typing import List, Union
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Absolute path to backend/.env
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(BASE_DIR, ".env")

# Ensure environment variables are loaded into os.environ from backend/.env
if os.path.exists(ENV_PATH):
    load_dotenv(dotenv_path=ENV_PATH, override=True)
else:
    load_dotenv(override=True)

class Settings(BaseSettings):
    PROJECT_NAME: str = "CareerPilot AI - Student Module"
    SECRET_KEY: str = "careerpilot-ai-super-secret-jwt-key-for-student-module"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database connection string (supports SQLite for zero-config dev & PostgreSQL for production)
    DATABASE_URL: str = "sqlite:///./careerpilot.db"
    
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]

    class Config:
        case_sensitive = True
        env_file = ENV_PATH
        extra = "ignore"

settings = Settings()
