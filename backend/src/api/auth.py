from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from .. import models
from ..models.user import UserCreate, UserInDB
from ..services.auth_service import AuthService
from ..config import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new user account
    """
    auth_service = AuthService()
    
    # Check if user already exists
    existing_user = await auth_service.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )
    
    # Create the new user
    user = await auth_service.create_user(db, user_data)
    return user

@router.post("/signin", response_model=UserInDB)
async def signin(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return user data
    """
    auth_service = AuthService()
    
    user = await auth_service.authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    return user