from fastapi import APIRouter, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from ..dependencies import get_current_active_user
from ...core.metrics import ACTIVE_USERS

router = APIRouter()

@router.get("/metrics")
async def metrics():
    """
    Expose Prometheus metrics endpoint.
    This endpoint should be protected in production and only accessible to monitoring systems.
    """
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

@router.get("/metrics/active-users")
async def active_users(current_user = get_current_active_user):
    """
    Update and get the number of active users.
    This is a protected endpoint that requires authentication.
    """
    # In a real application, you would implement proper user session tracking
    # This is just a simple example
    ACTIVE_USERS.inc()
    return {"active_users": ACTIVE_USERS._value.get()} 