"""
MCP Server Database Connection

Provides async database session for MCP tools.
"""

import os
from typing import AsyncGenerator

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# Create async engine for Neon PostgreSQL
engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=os.getenv("LOG_LEVEL", "INFO").upper() == "DEBUG",
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

# Async session factory
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session for MCP tools."""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_db_session() -> AsyncSession:
    """Get a new database session (non-generator version for tools)."""
    return async_session_maker()
