from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "AutoQ"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    SECRET_KEY: str = "default-secret-key-change-in-production"
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    
    # Database
    DATABASE_URL: str = "sqlite:///./autoq.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # File Storage
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 52428800  # 50MB
    ALLOWED_EXTENSIONS: str = "pdf"
    
    # JWT Authentication
    JWT_SECRET_KEY: str = "default-jwt-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # NLP Models
    SPACY_MODEL: str = "en_core_web_sm"
    TRANSFORMERS_MODEL: str = "distilbert-base-uncased"
    USE_GPU: bool = False
    
    # Question Generation
    DEFAULT_QUESTIONS_PER_PAPER: int = 20
    MIN_QUESTION_LENGTH: int = 10
    MAX_QUESTION_LENGTH: int = 500
    
    # Export Settings
    INSTITUTION_NAME: str = "Your Institution"
    INSTITUTION_LOGO: str = "./assets/logo.png"
    DEFAULT_PAPER_TEMPLATE: str = "standard"
    
    # Security
    ENABLE_ENCRYPTION: bool = True
    LOCAL_PROCESSING_ONLY: bool = False
    
    # Email (optional)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "your-email@gmail.com"
    SMTP_PASSWORD: str = "your-app-password"
    EMAIL_FROM: str = "noreply@autoq.edu"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields from .env


settings = Settings()
