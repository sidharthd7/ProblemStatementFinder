import cohere
from typing import Dict, List
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

def get_team_embedding(team_profile: Dict) -> List[float]:
    """
    Convert team profile into an embedding vector using Cohere
    """
    co = cohere.Client(settings.COHERE_API_KEY)
    
    # Create a natural language description of the team
    team_description = f"""
    Team Profile:
    - Size: {team_profile['size']} members
    - Experience Level: {team_profile['experience']}
    - Skills: {', '.join(team_profile['skills'])}
    - Project Deadline: {team_profile['deadline']} days
    """
    
    response = co.embed(texts=[team_description])
    return response.embeddings[0]


def get_problem_recommendations(team_profile: Dict, problem: Dict, similarity_score: float) -> str:
    """
    Generate a natural language recommendation using Cohere
    """
    co = cohere.Client(settings.COHERE_API_KEY)
    
    prompt = f"""
    Team Profile:
    - Size: {team_profile['size']} members
    - Experience Level: {team_profile['experience']}
    - Skills: {', '.join(team_profile['skills'])}
    - Project Deadline: {team_profile['deadline']} days

    Problem Statement:
    {problem['description']}

    Match Score: {similarity_score}

    Based on the team profile and problem statement above, provide a brief, natural explanation of why this problem might be a good match for the team. Focus on the most relevant aspects like skills match, team size appropriateness, and deadline feasibility.
    """
    try:
        
        response = co.generate(
            prompt=prompt,
            max_tokens=80,
            temperature=0.7,
            k=0,
            stop_sequences=[],
            return_likelihoods='NONE'
        )
        
        return response.generations[0].text.strip()
    
    except Exception as e:
        logger.error(f"Cohere API error: {e}")
        logger.error(f"Prompt sent: {prompt}")
        return "Could not generate recommendation due to an external error."

def analyze_skill_gap(team_profile: Dict, problem: Dict) -> str:
    """
    Analyze the skill gap between team's current skills and problem requirements
    """
    co = cohere.Client(settings.COHERE_API_KEY)
    
    # Find missing skills
    team_skills = set(skill.lower() for skill in team_profile['skills'])
    required_skills = set(skill.lower() for skill in problem['required_skills'])
    missing_skills = required_skills - team_skills
    
    prompt = f"""
    Team Profile:
    - Current Skills: {', '.join(team_profile['skills'])}
    - Experience Level: {team_profile['experience']}
    
    Problem Requirements:
    - Required Skills: {', '.join(problem['required_skills'])}
    - Missing Skills: {', '.join(missing_skills) if missing_skills else 'None'}
    
    Based on the team's current skills and the problem requirements, provide a brief analysis of:
    1. The skill gaps that need to be addressed
    2. How critical each missing skill is for the project
    Keep the response concise and actionable.
    """
    try:
        response = co.generate(
            prompt=prompt,
            max_tokens=108,
            temperature=0.7,
            k=0,
            stop_sequences=[],
            return_likelihoods='NONE'
        )
    
        return response.generations[0].text.strip()
    
    except Exception as e:
        logger.error(f"Cohere API error: {e}")
        logger.error(f"Prompt sent: {prompt}")
        return "Could not analyze skill gaps due to an external error."