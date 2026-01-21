"""
Logging Middleware

Provides structured logging for API requests.
"""

import logging
import time
import uuid
from typing import Callable

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate request ID
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id

        # Log request
        start_time = time.time()
        logger.info(
            f"[{request_id}] Request: {request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "query": str(request.query_params),
            }
        )

        # Process request
        response = await call_next(request)

        # Calculate duration
        duration_ms = (time.time() - start_time) * 1000

        # Log response
        logger.info(
            f"[{request_id}] Response: {response.status_code} ({duration_ms:.2f}ms)",
            extra={
                "request_id": request_id,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            }
        )

        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        return response


def setup_logging_middleware(app: FastAPI) -> None:
    """Setup logging middleware for the FastAPI application."""
    app.add_middleware(RequestLoggingMiddleware)
