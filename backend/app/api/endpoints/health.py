from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from ...db.session import get_db
from ...core.metrics import track_request_metrics
import psutil
import redis
from ...core.config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/health")
@track_request_metrics
async def health_check(db: Session = Depends(get_db)):
    """
    Comprehensive health check endpoint that monitors:
    - Database connectivity
    - Redis cache connectivity
    - System resources (CPU, Memory)
    - Disk space
    """
    health_status = {
        "status": "healthy",
        "components": {
            "database": {"status": "healthy"},
            "cache": {"status": "healthy"},
            "system": {"status": "healthy"}
        }
    }

    # Check database health
    try:
        db.execute(text("SELECT 1"))
        health_status["components"]["database"]["status"] = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        health_status["components"]["database"]["status"] = "unhealthy"
        health_status["components"]["database"]["error"] = str(e)
        health_status["status"] = "degraded"

    # Check Redis cache health
    try:
        redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            socket_timeout=1
        )
        redis_client.ping()
        health_status["components"]["cache"]["status"] = "healthy"
    except Exception as e:
        logger.error(f"Redis health check failed: {str(e)}")
        health_status["components"]["cache"]["status"] = "unhealthy"
        health_status["components"]["cache"]["error"] = str(e)
        health_status["status"] = "degraded"

    # Check system resources
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        health_status["components"]["system"] = {
            "status": "healthy",
            "metrics": {
                "cpu_usage": f"{cpu_percent}%",
                "memory_usage": f"{memory.percent}%",
                "disk_usage": f"{disk.percent}%"
            }
        }

        # Set system status to degraded if any metric is above threshold
        if cpu_percent > 80 or memory.percent > 80 or disk.percent > 80:
            health_status["components"]["system"]["status"] = "degraded"
            health_status["status"] = "degraded"

    except Exception as e:
        logger.error(f"System health check failed: {str(e)}")
        health_status["components"]["system"]["status"] = "unhealthy"
        health_status["components"]["system"]["error"] = str(e)
        health_status["status"] = "degraded"

    # If any component is unhealthy, return 503
    if any(comp["status"] == "unhealthy" for comp in health_status["components"].values()):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=health_status
        )

    return health_status

@router.get("/health/live")
async def liveness_check():
    """
    Simple liveness check endpoint for Kubernetes
    """
    return {"status": "alive"}

@router.get("/health/ready")
async def readiness_check(db: Session = Depends(get_db)):
    """
    Readiness check endpoint for Kubernetes
    Verifies that the application is ready to accept traffic
    """
    try:
        # Check database connection
        db.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service not ready"
        ) 