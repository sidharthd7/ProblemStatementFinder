from fastapi import UploadFile
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
import tempfile
import os
from pathlib import Path
import logging
from datetime import datetime
from ..core.exceptions import FileProcessingError, MalformedDataError
from ..schemas.problem import ProblemCreate
from ..models.problem import Problem
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class FileProcessorService:
    def __init__(self):
        # Common problem statement column names to look for
        self.possible_column_names = [
            'problem statement', 'problem description', 'description',
            'statement', 'problem', 'challenge', 'project'
        ]
        
        # Keywords that might indicate problem statement columns
        self.content_indicators = [
            'implement', 'create', 'develop', 'build', 'design',
            'requirement', 'feature', 'functionality'
        ]

    async def process_file(self, file: UploadFile, db: Session, team_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Process uploaded Excel file and extract problem statements
        """
        try:
            ext = os.path.splitext(file.filename)[1].lower()
            if ext not in (('.xlsx', '.xls', '.csv')):
                raise FileProcessingError("Only Excel (.xlsx, .xls) or CSV (.csv) files are allowed")
            
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='ext') as tmp:
                content = await file.read()
                tmp.write(content)
                tmp_path = tmp.name

            try:
                if ext == ".csv":
                    df = pd.read_csv(tmp_path)
                else:
                    df = pd.read_excel(tmp_path)
                
                
                # Process and extract problems
                problems = self._extract_problems(df)
                
                stored_problems = self._store_problems(db, problems, file.filename)
                
                return stored_problems

            finally:
                # Clean up temporary file
                os.unlink(tmp_path)

        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            raise FileProcessingError(str(e))
        
    def _store_problems(
        self,
        db: Session,
        problems: List[ProblemCreate],
        source_file: str
    ) -> List[Problem]:
        """
        Store processed problems in database
        """
        
        current_time = datetime.utcnow()
        stored_problems = []
        for prob in problems:
            db_problem = Problem(
                title=prob.title,
                description=prob.description,
                tech_stack=prob.tech_stack,
                source_file=source_file, 
                created_at=current_time
            )
            db.add(db_problem)
            stored_problems.append(db_problem)
        
        try:
            db.commit()
            for prob in stored_problems:
                db.refresh(prob)
            return stored_problems
        except Exception as e:
            db.rollback()
            logger.error(f"Database error storing problems: {str(e)}")
            raise FileProcessingError("Error storing problems in database")
        

    def _read_excel_file(self, file_path: str) -> pd.DataFrame:
        """
        Read Excel file with various attempts to handle different formats
        """
        try:
            # Try reading with default sheet
            df = pd.read_excel(file_path)
            
            # If empty, try other sheet names
            if df.empty:
                xl = pd.ExcelFile(file_path)
                for sheet in xl.sheet_names:
                    df = pd.read_excel(file_path, sheet_name=sheet)
                    if not df.empty:
                        break

            if df.empty:
                raise MalformedDataError("No data found in Excel file")

            return df

        except Exception as e:
            logger.error(f"Error reading Excel file: {str(e)}")
            raise FileProcessingError(f"Error reading Excel file: {str(e)}")

    def _extract_problems(self, df: pd.DataFrame) -> List[ProblemCreate]:
        """
        Extract problem statements from DataFrame
        """
        # Find the most likely problem statement column
        problem_col = self._identify_problem_column(df)
        if not problem_col:
            raise MalformedDataError("Could not identify problem statement column")

        # Extract tech stack if available
        tech_stack_col = self._identify_tech_stack_column(df)
        problems = []
        
        for idx, row in df.iterrows():
            try:
                problem_text = str(row[problem_col]).strip()
                
                # Skip empty or invalid problems
                if problem_text.lower() in ['nan', '', 'none']:
                    continue

                # Extract tech stack if available
                tech_stack = []
                if tech_stack_col:
                    tech_stack = self._extract_tech_stack(row[tech_stack_col])

                # Create problem object
                problem = ProblemCreate(
                    title=self._generate_title(problem_text),
                    description=problem_text,
                    tech_stack=tech_stack
                )
                problems.append(problem)
                
            except Exception as e:
                logger.warning(f"Error processing row {idx}: {str(e)}")
                continue
            
        if not problems:
            raise MalformedDataError("No valid problem statements found in file")

        return problems

    def _identify_problem_column(self, df: pd.DataFrame) -> str:
        """
        Identify the column containing problem statements
        """
        # Try exact matches first
        for col in df.columns:
            if str(col).lower() in self.possible_column_names:
                return col

        # Try content-based identification
        max_score = 0
        best_col = None
        
        for col in df.columns:
            if df[col].dtype != object:
                continue
                
            score = 0
            sample = df[col].dropna().astype(str).head(5)
            
            for text in sample:
                # Score based on text length and content indicators
                text_lower = text.lower()
                score += len(text) / 100  # Longer texts are more likely to be descriptions
                
                for indicator in self.content_indicators:
                    if indicator in text_lower:
                        score += 2

            if score > max_score:
                max_score = score
                best_col = col

        return best_col

    def _identify_tech_stack_column(self, df: pd.DataFrame) -> str:
        """
        Identify column containing technology requirements
        """
        tech_keywords = ['technology', 'tech stack', 'technical', 'skills', 'requirements']
        
        for col in df.columns:
            if any(keyword in str(col).lower() for keyword in tech_keywords):
                return col
        
        return None

    def _extract_tech_stack(self, tech_text: str) -> List[str]:
        """
        Extract technology stack from text
        """
        if pd.isna(tech_text) or not tech_text:
            return []

        
        # Split by common separators and clean up
        tech_stack = str(tech_text).replace(' and ', ',').replace('&', ',').replace(';', ',').split(',')
        tech_stack = [tech.strip() for tech in tech_stack if tech.strip()]
        
        return tech_stack
    

    def _generate_title(self, description: str, max_length: int = 100) -> str:
        """
        Generate a title from the problem description
        """
        # Split into sentences
        sentences = description.split('.')
        
        # Use first sentence if it's not too long
        title = sentences[0].strip()
        if len(title) <= max_length:
            return title
        
        # Otherwise, truncate with ellipsis
        return title[:max_length-3] + '...'