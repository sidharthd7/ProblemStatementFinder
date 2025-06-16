from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...core.exceptions import (
    FileProcessingError,
    InvalidFileFormatError,
    MalformedDataError,
    DatabaseError
)
from ...db.session import get_db
from ...schemas.problem import ProblemMatch, Problem
from ...models.team import Team
from ...services.file_processor import FileProcessorService
from ...services.problem_matcher import match_problems_to_team
from ...schemas.matching import MatchResponse
from ..deps import get_current_user
from ...core.metrics import track_request_metrics, track_db_operation
import logging
import traceback

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/upload", response_model=MatchResponse)
@track_request_metrics
async def upload_and_process(
    file: UploadFile = File(...),
    team_id: int = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Upload and process an Excel file containing problem statements.
    Optionally match with a specific team's skills.
    """
    try:
        # services
        file_processor = FileProcessorService()

        # processing file
        try:
            problems = await file_processor.process_file(file, db)
            logger.info(f"Successfully processed {len(problems)} problems")
        except InvalidFileFormatError as e:
            logger.error(f"Invalid file format: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except MalformedDataError as e:
            logger.error(f"Malformed data: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e)
            )
        except FileProcessingError as e:
            logger.error(f"File processing error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error processing file"
            )
        except Exception as e:
            logger.error(f"Unexpected error in file processing: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error in file processing: {str(e)}"
            )

        # If team_id provided, get team and match problems
        if team_id:
            try:
                team = await get_team_with_metrics(team_id, current_user.id, db)
                
                team_profile = {
                    "size": team.team_size,
                    "experience": team.experience_level,
                    "skills": team.tech_skills,
                    "deadline": team.deadline or 30
                }
                problems_list = [
                    {
                        "id": str(p.id),
                        "description": p.description,
                        "required_skills": p.tech_stack,
                        "complexity": getattr(p, "complexity", "medium"),
                        "deadline": getattr(p, "deadline", 30)
                    }
                    for p in problems
                ]
                matches = match_problems_to_team(team_profile, problems_list)
                return {"status": "success", "matches": matches}
                
            except Exception as e:
                logger.error(f"Error matching problems with team: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error matching problems with team: {str(e)}"
                )
        
        # If no team_id, return problems without matching
        return [{"problem": p, "score": 0, "tech_match": 0} for p in problems[:10]]

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in upload endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.get("/problems/{problem_id}", response_model=Problem)
@track_request_metrics
async def get_problem(
    problem_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Retrieve a specific problem by ID
    """
    try:
        problem = await get_problem_with_metrics(problem_id, db)
        if not problem:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Problem not found"
            )
        return problem
        
    except DatabaseError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )

@track_db_operation("select", "teams")
async def get_team_with_metrics(team_id: int, user_id: int, db: Session):
    team = db.query(Team).filter(Team.id == team_id).first()
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

@track_db_operation("select", "problems")
async def get_problem_with_metrics(problem_id: int, db: Session):
    return db.query(Problem).filter(Problem.id == problem_id).first()