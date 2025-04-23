from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from services.data_loader import load_excel_data
from services.problem_analyzer import ProblemAnalyzer
from repositories.problem_repository import ProblemRepository
from models.schema import TeamProfile, ProblemStatement
from typing import List, Tuple
import json
import tempfile

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
    db: Session = Depends(get_db)
):
    problem_repo = ProblemRepository(db)
    problems = problem_repo.get_all_problems()
    
    # Convert DB models to Pydantic models for the analyzer
    pydantic_problems = [ProblemStatement.from_orm(p) for p in problems]
    
    # Rank problems
    ranked_problems = problem_analyzer.rank_problems(pydantic_problems, team_profile)
    
    return {
        "matches": [
            {
                "problem": problem.dict(),
                "match_score": score
            }
            for problem, score in ranked_problems[:10]
        ]
    }
