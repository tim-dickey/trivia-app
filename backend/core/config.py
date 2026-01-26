"""
Core configuration settings for trivia-app backend
Uses pydantic-settings for environment variable management
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "trivia-app"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql://trivia_user:trivia_pass@localhost:5432/trivia_db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT Authentication
    SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Security
    BCRYPT_SALT_ROUNDS: int = 12
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings()
