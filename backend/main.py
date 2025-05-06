from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from contextlib import asynccontextmanager

# Import routers
from app.api.endpoints import auth, teams, problems

# Import config and dependencies
from app.core.config import settings
from app.db.session import get_db
from app.core.exceptions import DatabaseError, FileProcessingError

# Import services
from app.services.file_processor import FileProcessorService
from app.services.problem_matcher import ProblemMatcherService

# Import schemas
from app.schemas.problem import Problem, ProblemMatch
from app.schemas.team import Team, TeamCreate

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    logger.info("Starting up Problem Statement Finder API")
    
    yield
    
    logger.info("Shutting down Problem Statement Finder API")
        
    
# Initialize FastAPI app
app = FastAPI(
    title="Problem Statement Finder",
    description="""
    An API for matching problem statements with teams based on their skills and requirements.
    
    Key features:
    * Upload and process problem statement Excel and CSV files
    * Manage teams and their technical requirements
    * Match problems with teams based on skills
    * User authentication and authorization
    """,
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  
        "http://localhost:5173"   
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers 
app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["Authentication"]
)

app.include_router(
    teams.router,
    prefix=f"{settings.API_V1_STR}/teams",
    tags=["Teams"]
)

app.include_router(
    problems.router,
    prefix=f"{settings.API_V1_STR}/problems",
    tags=["Problems"]
)

# Initialize services
file_processor = FileProcessorService()
problem_matcher = ProblemMatcherService()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Problem Statement Finder API",
        version="1.0.0",
        description="""
        The Problem Statement Finder API helps match teams with suitable problem statements
        based on their technical skills and requirements.
        
        ## Authentication
        
        All API endpoints except login and signup require Bearer token authentication.
        To authenticate:
        1. Create an account using `/auth/signup`
        2. Get your token using `/auth/login`
        3. Include the token in the Authorization header: `Bearer <your_token>`
        
        ## File Upload
        
        When uploading problem statements:
        * Only Excel files (.xlsx, .xls) are accepted
        * The file should contain problem statements and optional tech requirements
        * The system will automatically identify relevant columns
        
        ## Team Management
        
        Teams can be created with:
        * Team name
        * Technical skills
        * Team size
        * Experience level
        * Optional deadline
        
        ## Problem Matching
        
        Problems are matched based on:
        * Technical skill requirements
        * Team experience level
        * Problem complexity
        """,
        routes=app.routes,
    )

    # specific endpoint documentation
    for path in openapi_schema["paths"]:
        # File upload endpoint
        if path.endswith("/upload"):
            openapi_schema["paths"][path]["post"]["description"] = """
            Upload an Excel file containing problem statements.
            
            The file should contain:
            * Problem statements/descriptions
            * Optional technical requirements
            * Optional difficulty levels
            
            The system will:
            1. Validate the file format
            2. Extract problem statements
            3. Identify technical requirements
            4. Store in the database
            5. Return processed problems
            
            Error Handling:
            * Invalid file format: 400 Bad Request
            * Malformed data: 422 Unprocessable Entity
            * Server errors: 500 Internal Server Error
            """
        
        # Team creation endpoint
        elif path.endswith("/teams"):
            openapi_schema["paths"][path]["post"]["description"] = """
            Create a new team with technical requirements.
            
            Required fields:
            * Team name
            * Technical skills (array of strings)
            * Team size (integer)
            * Experience level (string)
            
            Optional fields:
            * Deadline (datetime)
            
            The team will be associated with the authenticated user.
            """

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Health check endpoint
@app.get(
    "/health",
    tags=["Health Check"],
    summary="Check API health",
    response_description="Health check response"
)
async def health_check():
    """
    Health check endpoint to verify API is running.
    
    Returns:
        dict: Status information including version and environment
    """
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }

# Root endpoint
@app.get(
    "/",
    tags=["Root"],
    summary="Root endpoint",
    response_description="Welcome message"
)
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        dict: Basic API information and links to documentation
    """
    return {
        "name": "Problem Statement Finder API",
        "version": settings.VERSION,
        "documentation": "/api/docs",
        "redoc": "/api/redoc"
    }

# Global exception handlers
@app.exception_handler(DatabaseError)
async def database_exception_handler(request, exc):
    """
    Handle database-related exceptions
    """
    logger.error(f"Database error: {str(exc)}")
    return {
        "detail": str(exc),
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
    }

@app.exception_handler(FileProcessingError)
async def file_processing_exception_handler(request, exc):
    """
    Handle file processing exceptions
    """
    logger.error(f"File processing error: {str(exc)}")
    return {
        "detail": str(exc),
        "status_code": status.HTTP_400_BAD_REQUEST
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Handle any uncaught exceptions
    """
    logger.error(f"Uncaught exception: {str(exc)}")
    return {
        "detail": "An unexpected error occurred",
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  
        log_level="info"
    )