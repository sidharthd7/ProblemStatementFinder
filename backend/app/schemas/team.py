from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TeamBase(BaseModel):
    name: str
    tech_skills: List[str]
    team_size: int
    experience_level: str
    deadline: Optional[datetime] = None

class TeamCreate(TeamBase):
    pass

class TeamUpdate(TeamBase):
    name: Optional[str] = None
    tech_skills: Optional[List[str]] = None
    team_size: Optional[int] = None
    experience_level: Optional[str] = None

class TeamInDBBase(TeamBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Team(TeamInDBBase):
    pass