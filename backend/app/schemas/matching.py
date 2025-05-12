from pydantic import BaseModel
from typing import List, Dict, Optional

class TeamProfile(BaseModel):
    size: int
    experience: str
    skills: List[str]
    deadline: int

class ProblemDetails(BaseModel):
    id: str
    description: str
    required_skills: List[str]
    complexity: str
    deadline: int

class MatchResult(BaseModel):
    problem_id: str
    similarity_score: float
    recommendation: str
    skill_gap_analysis: str
    problem_details: ProblemDetails

class MatchResponse(BaseModel):
    status: str
    matches: List[MatchResult]