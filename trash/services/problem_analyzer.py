from typing import List, Tuple
from models.schema import ProblemStatement, TeamProfile
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

class ProblemAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=1000,
            ngram_range=(1, 2)
        )
    
    def calculate_text_similarity(self, team_skills: List[str], problem_description: str) -> float:
        """Calculate similarity between team skills and problem description"""
        combined_text = [' '.join(team_skills), problem_description]
        tfidf_matrix = self.vectorizer.fit_transform(combined_text)
        return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    def calculate_skill_match_score(self, required_skills: List[str], team_skills: List[str]) -> float:
        """Calculate how well team skills match required skills"""
        if not required_skills:
            return 1.0
        
        # Convert to lowercase for better matching
        required_lower = [skill.lower() for skill in required_skills]
        team_lower = [skill.lower() for skill in team_skills]
        
        matches = sum(1 for skill in required_lower if any(team_skill in skill or skill in team_skill for team_skill in team_lower))
        return matches / len(required_skills)
    
    def calculate_difficulty_score(self, problem_difficulty: str, team_proficiency: List[str]) -> float:
        """Calculate if problem difficulty matches team proficiency"""
        difficulty_levels = {"Beginner": 1, "Easy": 1, "Medium": 2, "Intermediate": 2, "Hard": 3, "Expert": 3}
        
        problem_level = difficulty_levels.get(problem_difficulty, 2)
        team_levels = [difficulty_levels.get(level, 2) for level in team_proficiency]
        avg_team_level = sum(team_levels) / len(team_levels)
        
        # Return higher score if team level matches or exceeds problem level
        return 1.0 if avg_team_level >= problem_level else avg_team_level / problem_level
    
    def calculate_time_feasibility(self, problem: ProblemStatement, team: TeamProfile) -> float:
        # Simple scoring based on deadline and estimated duration
        estimated_weeks = problem.requirements.estimated_duration_weeks
        available_weeks = (team.deadline - datetime.now()).days / 7
        
        if available_weeks <= 0:
            return 0.0
        
        if estimated_weeks <= available_weeks:
            return 1.0
        
        return available_weeks / estimated_weeks
    
    def rank_problems(self, problems: List[ProblemStatement], team: TeamProfile) -> List[Tuple[ProblemStatement, float, dict]]:
        """Rank problems based on multiple criteria and return detailed scores"""
        ranked_problems = []
        team_skills = [member.skill for member in team.technical_skills]
        team_proficiency = [member.proficiency_level for member in team.technical_skills]
        
        for problem in problems:
            # Calculate individual scores
            skill_score = self.calculate_skill_match_score(problem.tech_stack, team_skills)
            text_similarity = self.calculate_text_similarity(team_skills, problem.description)
            difficulty_score = self.calculate_difficulty_score(problem.difficulty_level, team_proficiency)
            
            # Domain match score
            domain_score = 1.0
            if team.preferred_domains and problem.category:
                domain_score = 1.0 if problem.category in team.preferred_domains else 0.5
            
            # Calculate weighted total score
            scores = {
                "skill_match": skill_score * 0.35,
                "content_relevance": text_similarity * 0.25,
                "difficulty_match": difficulty_score * 0.20,
                "domain_match": domain_score * 0.20
            }
            
            total_score = sum(scores.values())
            ranked_problems.append((problem, total_score, scores))
        
        return sorted(ranked_problems, key=lambda x: x[1], reverse=True)
