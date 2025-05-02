from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProblemBase(BaseModel):
    title: str
    description: str
    tech_stack: List[str]

class ProblemCreate(ProblemBase):
    pass

class ProblemUpdate(ProblemBase):
    title: Optional[str] = None
    description: Optional[str] = None
    tech_stack: Optional[List[str]] = None

class ProblemInDBBase(ProblemBase):
    id: int
    created_at: datetime
    source_file: str

    class Config:
        from_attributes = True

class Problem(ProblemInDBBase):
    pass

class ProblemMatch(BaseModel):
    problem: Problem
    score: float
    tech_match: float