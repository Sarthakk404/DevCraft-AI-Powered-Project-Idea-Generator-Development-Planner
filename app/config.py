from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App Info
    app_name: str = "DevCraft"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Groq API
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"
    
    # SQLite Database
    database_url: str = "sqlite:///./devcraft.db"
    
    # LLM Settings
    max_ideas: int = 5
    
    class Config:
        env_file = ".env"

def get_settings():
    return Settings()
