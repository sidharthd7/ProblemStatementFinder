from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ...core.exceptions import DatabaseError
from ...core.security import create_access_token, verify_password
from ...db.session import get_db
from ...schemas.user import UserCreate, User
from ...services.user_service import user_service
import logging
import traceback
from sqlalchemy import text
import sys

logger = logging.getLogger(__name__)
router = APIRouter()
logger.setLevel(logging.DEBUG)


@router.post("/signup", response_model=User)
async def signup(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Create new user
    """
    try:
        logger.debug("Starting signup process")
        logger.debug(f"Received user data: {user_in.dict(exclude={'password'})}")
        
        # Check database connection
        try:
            logger.debug("Testing database connection...")
            result = db.execute(text("SELECT 1"))
            result.scalar()  # Actually fetch the result
            logger.debug("Database connection successful")
        except Exception as e:
            logger.error("Database connection test failed")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Error message: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database connection error: {str(e)}"
            )

        # Check if user exists
        try:
            logger.debug(f"Checking if user exists with email: {user_in.email}")
            existing_user = user_service.get_by_email(db, email=user_in.email)
            if existing_user:
                logger.warning(f"User with email {user_in.email} already exists")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            logger.debug("No existing user found with this email")
        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error while checking existing user")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Error message: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error checking user existence: {str(e)}"
            )

        # Create new user
        try:
            logger.debug("Attempting to create new user")
            new_user = user_service.create(db, obj_in=user_in)
            logger.info(f"Successfully created user with email: {user_in.email}")
            return new_user
        except Exception as e:
            logger.error("Error while creating new user")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Error message: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating user: {str(e)}"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Unexpected error during signup process")
        logger.error(f"Error type: {type(e)}")
        logger.error(f"Error message: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.post("/login")
async def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login
    """
    try:
        # Authenticate user
        user = user_service.authenticate(
            db,
            email=form_data.username,
            password=form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        elif not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )

        # Create access token
        return {
            "access_token": create_access_token(user.id),
            "token_type": "bearer"
        }

    except DatabaseError as e:
        logger.error(f"Database error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login error occurred"
        )