from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...core.exceptions import DatabaseError
from ...db.session import get_db
from ...schemas.team import TeamCreate, Team, TeamUpdate
from ...services.team_service import team_service
from ..deps import get_current_user
from ...core.metrics import track_request_metrics, track_db_operation
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=Team, status_code=status.HTTP_201_CREATED)
@track_request_metrics
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
        return await create_team_with_metrics(db, team_in, current_user.id)

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
@track_request_metrics
async def get_teams(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get all teams for the current user
    """
    try:
        return await get_teams_with_metrics(db, current_user.id)
    except DatabaseError as e:
        logger.error(f"Database error fetching teams: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching teams"
        )

@router.put("/{team_id}", response_model=Team)
@track_request_metrics
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
        team = await get_team_with_metrics(team_id, current_user.id, db)
        
        # Update team
        return await update_team_with_metrics(db, team, team_in)

    except DatabaseError as e:
        logger.error(f"Database error updating team: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating team"
        )
        
@router.get("/{team_id}", response_model=Team)
@track_request_metrics
async def get_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get a specific team by ID
    """
    return await get_team_with_metrics(team_id, current_user.id, db)

@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
@track_request_metrics
async def delete_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Delete a team by ID
    """
    team = await get_team_with_metrics(team_id, current_user.id, db)
    await delete_team_with_metrics(db, team_id)
    return

# Helper functions with metrics
@track_db_operation("insert", "teams")
async def create_team_with_metrics(db: Session, team_in: TeamCreate, owner_id: int):
    return team_service.create_with_owner(
        db=db,
        obj_in=team_in,
        owner_id=owner_id
    )

@track_db_operation("select", "teams")
async def get_teams_with_metrics(db: Session, owner_id: int):
    return team_service.get_multi_by_owner(
        db=db,
        owner_id=owner_id
    )

@track_db_operation("select", "teams")
async def get_team_with_metrics(team_id: int, user_id: int, db: Session):
    team = team_service.get(db=db, id=team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    if team.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this team"
        )
    return team

@track_db_operation("update", "teams")
async def update_team_with_metrics(db: Session, team: Team, team_in: TeamUpdate):
    return team_service.update(
        db=db,
        db_obj=team,
        obj_in=team_in
    )

@track_db_operation("delete", "teams")
async def delete_team_with_metrics(db: Session, team_id: int):
    team_service.remove(db=db, id=team_id)