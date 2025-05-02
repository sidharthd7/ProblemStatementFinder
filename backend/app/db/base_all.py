# Import all models here for Alembic to detect them
from app.db.base import Base  # noqa
from app.models.user import User  # noqa
from app.models.team import Team  # noqa
from app.models.problem import Problem  # noqa