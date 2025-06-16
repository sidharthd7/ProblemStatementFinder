from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from contextlib import asynccontextmanager

#  routers
from app.api.endpoints import auth, teams, problems, matching

# config and dependencies
from app.core.config import settings
from app.db.session import get_db
from app.core.exceptions import DatabaseError, FileProcessingError
from app.core.rate_limit import rate_limiter
from app.core.logging import logger

# services
from app.services.file_processor import FileProcessorService
from app.services.problem_matcher import match_problems_to_team

# schemas
from app.schemas.problem import Problem, ProblemMatch
from app.schemas.team import Team, TeamCreate

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Problem Statement Finder API")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"API Version: {settings.VERSION}")
    
    yield
    
    logger.info("Shutting down Problem Statement Finder API")

# FastAPI app
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
    version=settings.VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Security Middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)



# Rate Limiting Middleware
@app.middleware("http")
async def rate_limit_middleware(request, call_next):
    await rate_limiter.check_rate_limit(request)
    response = await call_next(request)
    return response

# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

# routers 
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

app.include_router(
    matching.router,
    prefix=f"{settings.API_V1_STR}/matching",
    tags=["Matching"]
)

# Initialize services
file_processor = FileProcessorService()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Problem Statement Finder API",
        version=settings.VERSION,
        description="""
        The Problem Statement Finder API helps match teams with suitable problem statements
        based on their technical skills and requirements.
        
        ## Authentication
        
        All API endpoints except login and signup require Bearer token authentication.
        To authenticate:
        1. Create an account using `/auth/signup`
        2. Get your token using `/auth/login`
        3. Include the token in the Authorization header: `Bearer <your_token>`
        
        ## Security
        
        The API implements several security measures:
        * Rate limiting to prevent abuse
        * CORS protection
        * Security headers
        * Trusted host validation
        
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
        "environment": settings.ENVIRONMENT,
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
        "environment": settings.ENVIRONMENT,
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
    Handle all other exceptions
    """
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
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