import pandas as pd
from typing import List, Dict, Any
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)

class FileProcessor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=5000,
            ngram_range=(1, 2)
        )
    
    async def process_file(self, file_path: Path, team_skills: List[str]) -> List[Dict[str, Any]]:
        """
        Process the uploaded Excel file and return matched problems based on team skills.
        """
        try:
            # Read Excel file
            df = await self._read_excel_file(file_path)
            
            # Preprocess and validate data
            df = await self._preprocess_data(df)
            
            # Extract relevant columns
            problems = self._extract_problem_statements(df)
            
            # Calculate matches
            matches = await self._calculate_matches(problems, team_skills)
            
            return matches

        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            raise

    async def _read_excel_file(self, file_path: Path) -> pd.DataFrame:
        """
        Read and validate Excel file.
        """
        try:
            # Try different sheet names and headers
            possible_sheet_names = [0, 'Sheet1', 'Problems', 'Problem Statements']
            
            for sheet in possible_sheet_names:
                try:
                    df = pd.read_excel(file_path, sheet_name=sheet)
                    if not df.empty:
                        return df
                except Exception:
                    continue
            
            raise ValueError("No valid data found in Excel file")
            
        except Exception as e:
            logger.error(f"Error reading Excel file: {str(e)}")
            raise

    async def _preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess and clean the data.
        """
        # Identify potential problem statement columns
        text_columns = df.select_dtypes(include=['object']).columns
        
        # Look for columns that might contain problem statements
        problem_col = None
        for col in text_columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['problem', 'description', 'statement']):
                problem_col = col
                break
        
        if not problem_col:
            # If no obvious column found, use the column with the longest text
            avg_lengths = df[text_columns].apply(lambda x: x.str.len().mean())
            problem_col = avg_lengths.idxmax()

        # Clean the data
        df[problem_col] = df[problem_col].astype(str).apply(self._clean_text)
        
        return df[[problem_col]].copy()

    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize text data.
        """
        # Convert to string and lowercase
        text = str(text).lower()
        
        # Remove special characters but keep meaningful punctuation
        text = ' '.join(text.split())
        
        return text

    def _extract_problem_statements(self, df: pd.DataFrame) -> List[str]:
        """
        Extract problem statements from the dataframe.
        """
        return df[df.columns[0]].tolist()

    async def _calculate_matches(
        self, 
        problems: List[str], 
        team_skills: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Calculate matches between problems and team skills.
        """
        # Create skill profile
        team_profile = ' '.join(team_skills)
        
        # Combine problems and team profile for vectorization
        all_texts = problems + [team_profile]
        
        # Calculate TF-IDF
        tfidf_matrix = self.vectorizer.fit_transform(all_texts)
        
        # Calculate similarity between each problem and team profile
        similarities = cosine_similarity(
            tfidf_matrix[:-1],  # All problems
            tfidf_matrix[-1:]   # Team profile
        ).flatten()
        
        # Create results
        results = []
        for prob, score in zip(problems, similarities):
            results.append({
                'statement': prob,
                'score': round(float(score) * 100, 2),
                'keywords': self._extract_keywords(prob)
            })
        
        # Sort by score and get top 10
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:10]

    def _extract_keywords(self, text: str, num_keywords: int = 5) -> List[str]:
        """
        Extract key terms from the problem statement.
        """
        # Use TF-IDF to identify important terms
        vectorizer = TfidfVectorizer(stop_words='english', max_features=num_keywords)
        try:
            tfidf = vectorizer.fit_transform([text])
            feature_names = vectorizer.get_feature_names_out()
            return feature_names.tolist()
        except:
            return []