from typing import List, Tuple
from models.schema import ProblemStatement, TeamProfile
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ProblemAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
    
    def calculate_skill_match_score(self, required_skills: List[str], team_skills: List[str]) -> float:
        if not required_skills:
            return 1.0
        
        team_skills_set = set(team_skills)
        required_skills_set = set(required_skills)
        
        if not required_skills_set:
            return 1.0
            
        matching_skills = team_skills_set.intersection(required_skills_set)
        return len(matching_skills) / len(required_skills_set)
    
    def calculate_time_feasibility(self, problem: ProblemStatement, team: TeamProfile) -> float:
        # Simple scoring based on deadline and estimated duration
        estimated_weeks = problem.requirements.estimated_duration_weeks
        available_weeks = (team.deadline - datetime.now()).days / 7
        
        if available_weeks <= 0:
            return 0.0
        
        if estimated_weeks <= available_weeks:
            return 1.0
        
        return available_weeks / estimated_weeks
    
    def rank_problems(self, problems: List[ProblemStatement], team: TeamProfile) -> List[Tuple[ProblemStatement, float]]:
        ranked_problems = []
        
        team_skills = [member.skill for member in team.technical_skills]
        
        for problem in problems:
            # Calculate different scoring components
            skill_score = self.calculate_skill_match_score(problem.tech_stack, team_skills)
            time_score = self.calculate_time_feasibility(problem, team)
            team_size_fit = (
                problem.requirements.min_team_size <= team.team_size <= problem.requirements.max_team_size
            )
            
            # Combine scores (you can adjust weights based on importance)
            total_score = (
                skill_score * 0.4 +
                time_score * 0.3 +
                (1.0 if team_size_fit else 0.0) * 0.3
            )
            
            ranked_problems.append((problem, total_score))
        
        # Sort by score in descending order
        return sorted(ranked_problems, key=lambda x: x[1], reverse=True)
