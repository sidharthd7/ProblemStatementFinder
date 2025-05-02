from fastapi import APIRouter, UploadFile, File, HTTPException
from services.file_processor import FileProcessor
from typing import List
import tempfile
from pathlib import Path
import shutil

router = APIRouter()
file_processor = FileProcessor()

@router.post("/upload-and-process")
async def upload_and_process(
    file: UploadFile = File(...),
    team_skills: List[str] = []
):
    """
    Upload and process an Excel file to find matching problems for the team.
    """
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=400,
            detail="Only Excel files (.xlsx, .xls) are allowed"
        )

    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = Path(tmp.name)

    try:
        # Process the file
        results = await file_processor.process_file(tmp_path, team_skills)
        return {
            "success": True,
            "results": results
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )
    finally:
        # Clean up temporary file
        tmp_path.unlink()