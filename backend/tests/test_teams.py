import pytest
from fastapi import status
from app.schemas.team import TeamCreate

def test_create_team(client, auth_headers):
    """Test creating a new team"""
    team_data = {
        "name": "Test Team",
        "tech_skills": ["Python", "FastAPI"],
        "team_size": 3,
        "experience_level": "Intermediate"
    }
    
    response = client.post(
        "/api/v1/teams/",
        json=team_data,
        headers=auth_headers
    )
    print("RESPONSE STATUS:", response.status_code)
    print("RESPONSE JSON:", response.json())
    assert response.status_code == 201
 
    data = response.json()
    assert data["name"] == team_data["name"]
    assert data["tech_skills"] == team_data["tech_skills"]
    assert data["team_size"] == team_data["team_size"]
    assert data["experience_level"] == team_data["experience_level"]

def test_get_teams(client, auth_headers, test_team):
    """Test getting all teams for a user"""
    response = client.get(
        "/api/v1/teams/",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == test_team.name

def test_get_team(client, auth_headers, test_team):
    """Test getting a specific team"""
    response = client.get(
        f"/api/v1/teams/{test_team.id}",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == test_team.name
    assert data["id"] == test_team.id

def test_update_team(client, auth_headers, test_team):
    """Test updating a team"""
    update_data = {
        "name": "Updated Team",
        "tech_skills": ["Python", "FastAPI", "React"],
        "team_size": 4,
        "experience_level": "Advanced"
    }
    
    response = client.put(
        f"/api/v1/teams/{test_team.id}",
        json=update_data,
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["tech_skills"] == update_data["tech_skills"]
    assert data["team_size"] == update_data["team_size"]
    assert data["experience_level"] == update_data["experience_level"]

def test_delete_team(client, auth_headers, test_team):
    """Test deleting a team"""
    response = client.delete(
        f"/api/v1/teams/{test_team.id}",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify team is deleted
    response = client.get(
        f"/api/v1/teams/{test_team.id}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_create_team_validation(client, auth_headers):
    """Test team creation validation"""
    # Test missing required field
    team_data = {
        "name": "Test Team",
        "tech_skills": ["Python"],
        # Missing size and experience_level
    }
    
    response = client.post(
        "/api/v1/teams/",
        json=team_data,
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

@pytest.fixture(scope="function")
def test_team(db_session, test_user):
    from app.models.team import Team

    team = Team(
        name="Test Team",
        tech_skills=["Python", "FastAPI"],
        team_size=3,
        experience_level="Intermediate",
        owner_id=test_user.id
    )
    db_session.add(team)
    db_session.commit()
    db_session.refresh(team)
    return team

def test_unauthorized_access(client):
    """Test accessing team endpoints without authentication"""
    response = client.get("/api/v1/teams/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED 
    
    