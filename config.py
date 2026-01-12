import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    linkedin_client_id: Optional[str] = os.getenv("LINKEDIN_CLIENT_ID")
    linkedin_client_secret: Optional[str] = os.getenv("LINKEDIN_CLIENT_SECRET")
    linkedin_access_token: Optional[str] = os.getenv("LINKEDIN_ACCESS_TOKEN")
    linkedin_redirect_uri: str = os.getenv("LINKEDIN_REDIRECT_URI", "http://localhost:8000")
    server_host: str = "127.0.0.1"
    server_port: int = 8000
    
    # API Config
    api_base: str = "https://api.linkedin.com/v2"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
