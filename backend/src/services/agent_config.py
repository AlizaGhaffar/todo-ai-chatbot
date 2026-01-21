"""
AI Agent Configuration

Configures OpenAI Agents SDK with OpenRouter API backend.
Uses mistralai/devstral-2512:free model via OpenRouter's OpenAI-compatible endpoint.
"""

import os
import logging

from dotenv import load_dotenv
from openai import AsyncOpenAI

# Load environment variables FIRST
load_dotenv()

logger = logging.getLogger(__name__)

# Validate required environment variable
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    logger.warning("OPENROUTER_API_KEY not set - agent will not function")

# OpenRouter API configuration
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_MODEL = "mistralai/devstral-2512:free"


def get_openai_client() -> AsyncOpenAI:
    """
    Get AsyncOpenAI client configured for OpenRouter API.

    Returns:
        AsyncOpenAI client pointing to OpenRouter's OpenAI-compatible endpoint
    """
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY environment variable is required")

    return AsyncOpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
    )


def get_agent_model():
    """
    Get the OpenAI Agents SDK model configuration for OpenRouter.

    Returns:
        OpenAIChatCompletionsModel configured for OpenRouter
    """
    try:
        from agents import OpenAIChatCompletionsModel, set_tracing_disabled

        # Disable tracing for production
        set_tracing_disabled(True)

        client = get_openai_client()

        return OpenAIChatCompletionsModel(
            model=OPENROUTER_MODEL,
            openai_client=client,
        )
    except ImportError:
        logger.error("openai-agents package not installed")
        raise


# Agent configuration constants
AGENT_CONFIG = {
    "model": OPENROUTER_MODEL,
    "max_tokens": 1024,
    "temperature": 0.7,
    "context_window": 10,  # Max messages for conversation context
}
