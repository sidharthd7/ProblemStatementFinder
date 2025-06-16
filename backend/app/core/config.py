from pydantic_settings import BaseSettings
from typing import Optional, List
import logging
from pydantic import AnyHttpUrl, validator

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    PROJECT_NAME: str = "Problem Statement Finder"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    
    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    
    # Redis Cache
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    CACHE_EXPIRE_SECONDS: int = 3600  # 1 hour
    
    # API Keys
    COHERE_API_KEY: str
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: List[AnyHttpUrl] = []
    
    # SMTP settings for alerts
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    ALERT_EMAIL_RECIPIENTS: Optional[str] = None
    
    # Monitoring settings
    ENABLE_METRICS: bool = True
    ENABLE_ALERTS: bool = True
    ALERT_THRESHOLDS: dict = {
        "cpu_usage": 80,
        "memory_usage": 80,
        "disk_usage": 80,
        "error_rate": 5,
        "response_time": 2.0
    }
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Security Headers
    ALLOWED_HOSTS: List[str] = ["*"]
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Testing
    TESTING: bool = False
    TEST_DATABASE_URL: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        logger.info(f"Loaded configuration:")
        logger.info(f"Environment: {self.ENVIRONMENT}")
        logger.info(f"Version: {self.VERSION}")
        logger.info(f"POSTGRES_SERVER: {self.POSTGRES_SERVER}")
        logger.info(f"POSTGRES_USER: {self.POSTGRES_USER}")
        logger.info(f"POSTGRES_DB: {self.POSTGRES_DB}")
        logger.info(f"Database URL will be: postgresql://{self.POSTGRES_USER}:***@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}")
        logger.info(f"CORS Origins: {self.CORS_ORIGINS}")
        logger.info(f"Rate Limit: {self.RATE_LIMIT_PER_MINUTE} requests per minute")
        logger.info(f"Redis Host: {self.REDIS_HOST}")
        logger.info(f"Cache Expiration: {self.CACHE_EXPIRE_SECONDS} seconds")

settings = Settings()