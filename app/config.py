from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration settings."""
    
    # App Info
    app_name: str = "DevCraft"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # Google Gemini API
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"
    
    # PostgreSQL Database
    database_url: str = "postgresql://user:password@localhost:5432/devcraft"
    
    # LLM Settings
    max_ideas: int = 5
    temperature: float = 0.7
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
