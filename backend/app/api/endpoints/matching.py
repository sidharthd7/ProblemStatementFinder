from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ...schemas.matching import TeamProfile, ProblemDetails, MatchResponse
from ...services.problem_matcher import match_problems_to_team
# from ...services.problem_matcher import ProblemMatcherService

router = APIRouter()

@router.post("/match", response_model=MatchResponse)
async def match_problems(
    team_profile: TeamProfile,
    problems: List[ProblemDetails]
):
    """
    Match problems to team profile and return recommendations
    """
    try:
        # Convert Pydantic models to dictionaries
        team_dict = team_profile.dict()
        problems_dict = [p.dict() for p in problems]
        
        # Get matches using the new matching function
        matches = match_problems_to_team(team_dict, problems_dict)
        
        return {
            "status": "success",
            "matches": matches
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error matching problems: {str(e)}"
        )
