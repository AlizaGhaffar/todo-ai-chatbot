"""
Auth API Routes

Handles user authentication - signup, login, and current user.
"""

import logging
from pydantic import BaseModel, Field, EmailStr
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.database import get_session
from src.auth.config import (
    create_user,
    authenticate_user,
    create_access_token,
    get_current_user,
)
from src.models.user import User, UserRead

logger = logging.getLogger(__name__)

router = APIRouter()


class SignupRequest(BaseModel):
    """Request body for signup."""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)


class LoginRequest(BaseModel):
    """Request body for login."""
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    """Response for auth endpoints."""
    user: UserRead
    token: str


@router.post("/signup", response_model=AuthResponse)
async def signup(
    request: SignupRequest,
    session: AsyncSession = Depends(get_session),
):
    """
    Create a new user account.

    Returns the user data and an access token.
    """
    logger.info(f"Signup attempt for email: {request.email}")

    user = await create_user(
        session=session,
        name=request.name,
        email=request.email,
        password=request.password,
    )

    token = create_access_token(user.id)

    logger.info(f"User created successfully: {user.id}")

    return AuthResponse(
        user=UserRead(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=user.created_at,
        ),
        token=token,
    )


@router.post("/login", response_model=AuthResponse)
async def login(
    request: LoginRequest,
    session: AsyncSession = Depends(get_session),
):
    """
    Login with email and password.

    Returns the user data and an access token.
    """
    logger.info(f"Login attempt for email: {request.email}")

    user = await authenticate_user(
        session=session,
        email=request.email,
        password=request.password,
    )

    token = create_access_token(user.id)

    logger.info(f"User logged in successfully: {user.id}")

    return AuthResponse(
        user=UserRead(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=user.created_at,
        ),
        token=token,
    )


@router.get("/me", response_model=UserRead)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    """
    Get the current authenticated user.

    Requires a valid access token in the Authorization header.
    """
    return UserRead(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        created_at=current_user.created_at,
    )
