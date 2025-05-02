from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

# Create database URL
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}/"
    f"{settings.POSTGRES_DB}"
)

logger.info(f"Attempting to connect to database at: postgresql://{settings.POSTGRES_USER}:***@{settings.POSTGRES_SERVER}/{settings.POSTGRES_DB}")

try:
    # Create engine
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,  # Enable connection pool "pre-ping" feature
    )
    
    # Test the connection
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        logger.info("Successfully connected to the database!")
        
except Exception as e:
    logger.error(f"Failed to connect to database: {str(e)}")
    raise

# Create SessionLocal class with sessionmaker factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()