from pydantic_settings import BaseSettings
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    PROJECT_NAME: str = "Problem Statement Finder"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    
    # JWT token
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  
    
    class Config:
        env_file = ".env"
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        logger.info(f"Loaded configuration:")
        logger.info(f"POSTGRES_SERVER: {self.POSTGRES_SERVER}")
        logger.info(f"POSTGRES_USER: {self.POSTGRES_USER}")
        logger.info(f"POSTGRES_DB: {self.POSTGRES_DB}")
        logger.info(f"Database URL will be: postgresql://{self.POSTGRES_USER}:***@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}")

settings = Settings()