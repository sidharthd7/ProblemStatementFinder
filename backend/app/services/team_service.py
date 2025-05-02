from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from ..models.team import Team
from ..schemas.team import TeamCreate, TeamUpdate
from .base import CRUDBase

class TeamService(CRUDBase[Team, TeamCreate, TeamUpdate]):
    def get_by_owner(
        self,
        db: Session,
        *,
        owner_id: int
    ) -> Optional[Team]:
        return db.query(Team).filter(Team.owner_id == owner_id).first()

    def get_multi_by_owner(
        self,
        db: Session,
        *,
        owner_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Team]:
        return (
            db.query(Team)
            .filter(Team.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_owner(
        self,
        db: Session,
        *,
        obj_in: TeamCreate,
        owner_id: int
    ) -> Team:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Team(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

team_service = TeamService(Team)