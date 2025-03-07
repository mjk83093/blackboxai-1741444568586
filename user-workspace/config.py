from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "Work Production AI Agent"
    DEBUG: bool = False
    
    # Microsoft OAuth Settings
    MS_CLIENT_ID: str = ""
    MS_CLIENT_SECRET: str = ""
    MS_TENANT_ID: str = ""
    MS_REDIRECT_URI: str = "http://localhost:8000/auth/microsoft/callback"
    
    # Google OAuth Settings
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/google/callback"
    
    # OpenAI Settings
    OPENAI_API_KEY: str = ""
    
    # Security Settings
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database Settings
    DATABASE_URL: str = "sqlite:///./workproduction.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
