"""
Error Handling Middleware

Provides consistent error responses across the API.
"""

import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str, status_code: int = 400, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class TaskNotFoundError(AppException):
    """Task not found exception."""

    def __init__(self, task_id: int, user_id: str):
        super().__init__(
            message=f"Task {task_id} not found for user {user_id}",
            status_code=404,
            details={"task_id": task_id, "user_id": user_id}
        )


class ConversationNotFoundError(AppException):
    """Conversation not found exception."""

    def __init__(self, conversation_id: str):
        super().__init__(
            message=f"Conversation {conversation_id} not found",
            status_code=404,
            details={"conversation_id": conversation_id}
        )


def setup_error_handlers(app: FastAPI) -> None:
    """Setup error handlers for the FastAPI application."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.warning(f"App exception: {exc.message}", extra={"details": exc.details})
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.message,
                "details": exc.details
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning(f"Validation error: {exc.errors()}")
        return JSONResponse(
            status_code=422,
            content={
                "error": "Validation error",
                "details": exc.errors()
            }
        )

    @app.exception_handler(SQLAlchemyError)
    async def database_exception_handler(request: Request, exc: SQLAlchemyError):
        logger.error(f"Database error: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Database error",
                "details": {"message": "An internal database error occurred"}
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "details": {"message": "An unexpected error occurred"}
            }
        )
