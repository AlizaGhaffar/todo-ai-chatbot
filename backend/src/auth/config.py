"""
Better Auth Configuration

JWT-based authentication for the AI Todo Chatbot.
"""

import os
import uuid
from datetime import datetime, timedelta
from typing import Optional, Annotated

import bcrypt
import jwt
from fastapi import HTTPException, Depends, Header
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.db.database import get_session
from src.models.user import User

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "your-super-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24 * 7  # 1 week


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def create_access_token(user_id: str) -> str:
    """Create a JWT access token."""
    expiration = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    payload = {
        "sub": user_id,
        "exp": expiration,
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> Optional[str]:
    """Decode a JWT access token and return the user_id."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
    """Get a user by email."""
    result = await session.exec(select(User).where(User.email == email))
    return result.first()


async def get_user_by_id(session: AsyncSession, user_id: str) -> Optional[User]:
    """Get a user by ID."""
    result = await session.exec(select(User).where(User.id == user_id))
    return result.first()


async def create_user(
    session: AsyncSession,
    name: str,
    email: str,
    password: str
) -> User:
    """Create a new user."""
    # Check if user already exists
    existing = await get_user_by_email(session, email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        id=str(uuid.uuid4()),
        name=name,
        email=email,
        password_hash=hash_password(password),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def authenticate_user(
    session: AsyncSession,
    email: str,
    password: str
) -> User:
    """Authenticate a user and return the user object."""
    user = await get_user_by_email(session, email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return user


def get_optional_token(
    authorization: Optional[str] = Header(None, alias="Authorization")
) -> Optional[str]:
    """Extract token from Authorization header (optional)."""
    if not authorization:
        return None
    if not authorization.startswith("Bearer "):
        return None
    return authorization[7:]


async def get_current_user_optional(
    token: Optional[str] = Depends(get_optional_token),
    session: AsyncSession = Depends(get_session),
) -> Optional[User]:
    """Get the current authenticated user (optional - returns None if not authenticated)."""
    if not token:
        return None

    user_id = decode_access_token(token)
    if not user_id:
        return None

    user = await get_user_by_id(session, user_id)
    return user


async def get_current_user(
    token: Optional[str] = Depends(get_optional_token),
    session: AsyncSession = Depends(get_session),
) -> User:
    """Get the current authenticated user (required - raises 401 if not authenticated)."""
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Authentication required. Please login or signup."
        )

    user_id = decode_access_token(token)
    user = await get_user_by_id(session, user_id)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def get_current_user_id(user_id: str) -> str:
    """
    Validate user_id from path parameter (for guest access).
    This is kept for backward compatibility with guest users.
    """
    if not user_id or not user_id.strip():
        raise HTTPException(status_code=400, detail="User ID cannot be empty")

    if len(user_id) > 100:
        raise HTTPException(status_code=400, detail="User ID too long (max 100 characters)")

    sanitized = user_id.strip()
    if not all(c.isalnum() or c in "_-" for c in sanitized):
        raise HTTPException(
            status_code=400,
            detail="User ID can only contain letters, numbers, underscores, and hyphens"
        )

    return sanitized
