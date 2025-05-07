from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...core.exceptions import DatabaseError
from ...db.session import get_db
from ...schemas.team import TeamCreate, Team, TeamUpdate
from ...services.team_service import team_service
from ..deps import get_current_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=Team)
async def create_team(
    team_in: TeamCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Create a new team
    """
    try:
        # Validating team data
        if team_in.team_size <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Team size must be greater than 0"
            )

        # Creating team
        return team_service.create_with_owner(
            db=db,
            obj_in=team_in,
            owner_id=current_user.id
        )

    except DatabaseError as e:
        logger.error(f"Database error creating team: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating team"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@router.get("/", response_model=List[Team])
async def get_teams(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get all teams for the current user
    """
    try:
        return team_service.get_multi_by_owner(
            db=db,
            owner_id=current_user.id
        )
    except DatabaseError as e:
        logger.error(f"Database error fetching teams: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching teams"
        )

@router.put("/{team_id}", response_model=Team)
async def update_team(
    team_id: int,
    team_in: TeamUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Update a team
    """
    try:
        # Get existing team
        team = team_service.get(db=db, id=team_id)
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        
        # Check owner
        if team.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to modify this team"
            )

        # Update team
        return team_service.update(
            db=db,
            db_obj=team,
            obj_in=team_in
        )

    except DatabaseError as e:
        logger.error(f"Database error updating team: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating team"
        )