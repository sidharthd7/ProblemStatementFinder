# backend/models/schema.py
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class TeamMember(BaseModel):
    skill: str
    proficiency_level: str  # "Beginner", "Intermediate", "Expert"

class TeamProfile(BaseModel):
    team_size: int
    technical_skills: List[TeamMember]
    preferred_domains: List[str] = []
    deadline: datetime

class ProjectRequirements(BaseModel):
    min_team_size: int
    max_team_size: int
    required_skills: List[str]
    estimated_duration_weeks: int
    difficulty_level: str

# Enhance existing ProblemStatement
class ProblemStatement(BaseModel):
    title: str
    description: str
    category: Optional[str] = None
    difficulty_level: Optional[str] = "Medium"
    tech_stack: List[str]
    source: str
    created_at: datetime
    updated_at: datetime
    requirements: ProjectRequirements  # Add this field