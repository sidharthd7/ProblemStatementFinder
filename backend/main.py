from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, Query
from sqlalchemy.orm import Session
from config.database import get_db
from services.data_loader import load_excel_data
from services.problem_analyzer import ProblemAnalyzer
from repositories.problem_repository import ProblemRepository
from models.schema import TeamProfile, ProblemStatement
from typing import List, Tuple, Optional
import json
import tempfile
from datetime import datetime

app = FastAPI()
problem_analyzer = ProblemAnalyzer()

@app.post("/upload-problems")
async def upload_problems(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_path = temp_file.name

    try:
        # Load problems from Excel
        problems = load_excel_data(temp_path)
        
        # Save to database
        problem_repo = ProblemRepository(db)
        for problem in problems:
            problem_repo.create_problem(problem)
        
        return {"message": f"Successfully loaded {len(problems)} problems"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/problems")
async def get_problems(db: Session = Depends(get_db)):
    problem_repo = ProblemRepository(db)
    problems = problem_repo.get_all_problems()
    return problems

@app.post("/match-problems")
async def match_problems(
    team_profile: TeamProfile,
    min_score: float = Query(0.5, ge=0.0, le=1.0),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    problem_repo = ProblemRepository(db)
    problems = problem_repo.get_all_problems()
    
    # Convert DB models to Pydantic models
    pydantic_problems = [ProblemStatement.from_orm(p) for p in problems]
    
    # Get ranked problems with detailed scores
    ranked_problems = problem_analyzer.rank_problems(pydantic_problems, team_profile)
    
    # Filter by minimum score and limit results
    filtered_problems = [
        {
            "problem": problem.dict(),
            "total_score": total_score,
            "score_breakdown": score_details
        }
        for problem, total_score, score_details in ranked_problems
        if total_score >= min_score
    ][:limit]
    
    return {
        "matches": filtered_problems,
        "total_results": len(filtered_problems),
        "team_size": team_profile.team_size,
        "analysis_timestamp": datetime.now().isoformat()
    }

@app.get("/problems/search")
async def search_problems(
    query: str,
    category: Optional[str] = None,
    tech_stack: Optional[List[str]] = Query(None),
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    problem_repo = ProblemRepository(db)
    problems = problem_repo.search_problems(
        query=query,
        category=category,
        tech_stack=tech_stack,
        difficulty=difficulty
    )
    return problems

@app.get("/analytics/categories")
async def get_category_stats(db: Session = Depends(get_db)):
    """Get statistics about problem categories"""
    problem_repo = ProblemRepository(db)
    return problem_repo.get_category_statistics()
