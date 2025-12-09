"""
Application configuration management
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Curita RAG Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 3050
    
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    # Database
    DATABASE_URL: Optional[str] = None
    
    # Embedding Model
    EMBEDDING_MODEL: str = "Snowflake/snowflake-arctic-embed-xs"
    EMBEDDING_DIMENSION: int = 384
    
    # Document Processing (LangChain)
    DEFAULT_CHUNK_SIZE: int = 1000
    DEFAULT_CHUNK_OVERLAP: int = 200
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_API_KEY: Optional[str] = None
    
    # Search
    DEFAULT_TOP_K: int = 5
    DEFAULT_SIMILARITY_THRESHOLD: float = 0.0
    
    # Tables
    DOCUMENTS_TABLE: str = "documents"
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE_ENABLED: bool = True
    LOG_FILE_MAX_BYTES: int = 10485760  # 10MB
    LOG_FILE_BACKUP_COUNT: int = 5
    LOG_JSON_FORMAT: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache() 
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
