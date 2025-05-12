from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from ..schemas.problem import Problem, ProblemMatch
from ..schemas.team import Team
import cohere
from ..services.cohere_service import get_team_embedding, get_problem_recommendations, analyze_skill_gap
from ..core.config import settings

# class ProblemMatcherService:
#     def __init__(self):
#         self.vectorizer = TfidfVectorizer(
#             stop_words='english',
#             max_features=5000,
#             ngram_range=(1, 2)
#         )
        
#         # Weights for diff. matching criteria
#         self.weights = {
#             'tech_stack': 0.6,
#             'description': 0.4
#         }

#     def find_matches(
#         self,
#         problems: List[Problem],
#         team: Team,
#         limit: int = 10
#     ) -> List[ProblemMatch]:
#         """
#         Find the best matching problems for a team
#         """
#         if not problems:
#             return []

#         # tech stack similarity
#         tech_scores = self._calculate_tech_similarity(problems, team.tech_skills)
        
#         # description similarity
#         desc_scores = self._calculate_description_similarity(problems, team)
        
#         # Combined
#         final_scores = []
#         for i, problem in enumerate(problems):
#             score = (
#                 tech_scores[i] * self.weights['tech_stack'] +
#                 desc_scores[i] * self.weights['description']
#             )
            
#             final_scores.append({
#                 'problem': problem,
#                 'score': round(float(score) * 100, 2),
#                 'tech_match': round(float(tech_scores[i]) * 100, 2)
#             })

#         # sort and return
#         matches = sorted(final_scores, key=lambda x: x['score'], reverse=True)
#         return matches[:limit]

#     def _calculate_tech_similarity(
#         self,
#         problems: List[Problem],
#         team_skills: List[str]
#     ) -> np.ndarray:
#         """
#         Calculate similarity between problem tech stack and team skills
#         """
#         scores = []
#         team_skills_lower = [skill.lower() for skill in team_skills]
        
#         for problem in problems:
#             problem_tech = [tech.lower() for tech in problem.tech_stack]
            
#             # Jaccard similarity
#             intersection = len(set(team_skills_lower) & set(problem_tech))
#             union = len(set(team_skills_lower) | set(problem_tech))
            
#             score = intersection / union if union > 0 else 0
#             scores.append(score)
            
#         return np.array(scores)

#     def _calculate_description_similarity(
#         self,
#         problems: List[Problem],
#         team: Team
#     ) -> np.ndarray:
#         """
#         Calculate similarity between problem descriptions and team profile
#         """
#         # problem description collection
#         descriptions = [p.description for p in problems]

#         team_profile = f"{' '.join(team.tech_skills)} {team.experience_level}"
        
#         # Adding team profile to collection
#         all_texts = descriptions + [team_profile]
        
#         # TF-IDF
#         tfidf_matrix = self.vectorizer.fit_transform(all_texts)
        
#         # similarity between each problem and team profile
#         similarities = cosine_similarity(
#             tfidf_matrix[:-1],  # All problems
#             tfidf_matrix[-1:]   # Team profile
#         ).flatten()
        
#         return similarities
    
def match_problems_to_team(team_profile: Dict, problems: List[Dict]) -> List[Dict]:
    """
    Match problems to team profile and generate recommendations
    """
    co = cohere.Client(settings.COHERE_API_KEY)
    
    # Get team embedding
    team_embedding = get_team_embedding(team_profile)
    
    # Get problem embeddings
    problem_descriptions = [p['description'] for p in problems]
    problem_embeddings = co.embed(texts=problem_descriptions).embeddings
    
    # Calculate similarities
    similarities = cosine_similarity([team_embedding], problem_embeddings)[0]
    
    # Generate recommendations and create results
    results = []
    for i, (problem, similarity) in enumerate(zip(problems, similarities)):
        recommendation = get_problem_recommendations(team_profile, problem, similarity)
        skill_gap = analyze_skill_gap(team_profile, problem)
        
        results.append({
            'problem_id': problem['id'],
            'similarity_score': float(similarity),
            'recommendation': recommendation,
            'skill_gap_analysis': skill_gap,
            'problem_details': problem
        })
    
    # Sort by similarity score
    results.sort(key=lambda x: x['similarity_score'], reverse=True)
    
    return results