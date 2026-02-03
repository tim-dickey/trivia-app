"""
Core configuration settings for trivia-app backend
Uses pydantic-settings for environment variable management
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import Optional
import secrets


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
    # Generate with: openssl rand -hex 32
    SECRET_KEY: str = secrets.token_hex(32)  # Auto-generate if not provided
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
    
    @field_validator('SECRET_KEY')
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Validate SECRET_KEY is strong enough"""
        if len(v) < 32:
            raise ValueError(
                "SECRET_KEY must be at least 32 characters long. "
                "Generate one with: openssl rand -hex 32"
            )
        # Warn about common insecure values
        insecure_values = [
            "CHANGE_THIS_IN_PRODUCTION",
            "your-secret-key-here",
            "secret",
            "password",
            "12345",
        ]
        if v.lower() in [x.lower() for x in insecure_values]:
            raise ValueError(
                f"SECRET_KEY contains an insecure default value. "
                "Generate a secure key with: openssl rand -hex 32"
            )
        return v


settings = Settings()
