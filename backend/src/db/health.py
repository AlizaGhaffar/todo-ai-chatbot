"""
Database Health Check

Verifies database connectivity and basic operations.
"""

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import text

from .database import engine


async def check_db_health() -> dict:
    """
    Check database connectivity.

    Returns:
        dict with health status and details
    """
    try:
        async with engine.connect() as conn:
            # Simple query to verify connection
            result = await conn.execute(text("SELECT 1"))
            result.fetchone()

        return {
            "status": "healthy",
            "database": "connected",
            "message": "Database connection successful"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "message": str(e)
        }


async def verify_tables_exist(session: AsyncSession) -> dict:
    """
    Verify all required tables exist.

    Returns:
        dict with table verification status
    """
    required_tables = ["tasks", "conversations", "messages"]
    existing_tables = []
    missing_tables = []

    try:
        for table in required_tables:
            result = await session.execute(
                text(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = :table)"),
                {"table": table}
            )
            exists = result.scalar()
            if exists:
                existing_tables.append(table)
            else:
                missing_tables.append(table)

        return {
            "status": "healthy" if not missing_tables else "degraded",
            "existing_tables": existing_tables,
            "missing_tables": missing_tables
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
