import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

# Compute absolute path to backend directory
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_SQLITE_PATH = os.path.join(BACKEND_DIR, "careerpilot.db").replace("\\", "/")

class Settings(BaseSettings):
    PROJECT_NAME: str = "CareerPilot AI - Recruiter Module"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Absolute path database default
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{DEFAULT_SQLITE_PATH}"
    )
    
    # JWT Auth
    JWT_SECRET: str = os.getenv("JWT_SECRET", "careerpilot_recruiter_jwt_secret_key_2026_super_safe")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000"
    ]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
