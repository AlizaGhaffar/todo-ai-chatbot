"""
FastAPI Application

Main entry point for the AI Todo Chatbot API.
"""

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.db.database import init_db
from src.db.health import check_db_health
from .middleware import setup_error_handlers, setup_logging_middleware

# Load environment
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    logger.info("Starting AI Todo Chatbot API...")

    # Initialize database tables (gracefully handle failures)
    try:
        await init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.warning(f"Database initialization failed: {e}")
        logger.warning("Server will start but database features may not work")

    yield

    logger.info("Shutting down AI Todo Chatbot API...")


# Create FastAPI application
app = FastAPI(
    title="AI Todo Chatbot API",
    description="Natural language task management chatbot API",
    version="0.1.0",
    lifespan=lifespan,
)

# Setup CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup middleware
setup_logging_middleware(app)
setup_error_handlers(app)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    db_health = await check_db_health()
    return {
        "status": "healthy" if db_health["status"] == "healthy" else "degraded",
        "service": "ai-todo-chatbot",
        "database": db_health
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "AI Todo Chatbot API",
        "version": "0.1.0",
        "docs": "/docs"
    }


# Import and include routers
from .routes.chat import router as chat_router
from .routes.auth import router as auth_router
from .routes.tasks import router as tasks_router

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks_router, prefix="/api", tags=["tasks"])
app.include_router(chat_router, prefix="/api", tags=["chat"])
