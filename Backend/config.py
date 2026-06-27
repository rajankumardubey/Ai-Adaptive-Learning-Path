import os
try:
    # pydantic v2+ uses the separate pydantic-settings package
    from pydantic_settings import BaseSettings # type: ignore
except Exception:
    try:
        # Fallback for environments with pydantic v1
        from pydantic import BaseSettings
    except Exception:
        raise ImportError("pydantic or pydantic-settings is required. Run 'pip install pydantic[email] pydantic-settings'")
from typing import List

class Settings(BaseSettings): # type: ignore
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/adaptive_learning")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API Settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # AI/ML
    HF_API_KEY: str = os.getenv("HF_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MODEL_PATH: str = os.getenv("MODEL_PATH", "./models")
    
    # Email
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
