"""Services module for AI Todo Chatbot."""

from .agent_config import get_agent_model, get_openai_client, AGENT_CONFIG
from .agent_prompt import SYSTEM_PROMPT
from .agent import create_agent, process_chat_message
from .conversation import (
    get_or_create_conversation,
    get_conversation_context,
    save_message,
    format_messages_for_agent,
)

__all__ = [
    "get_agent_model",
    "get_openai_client",
    "AGENT_CONFIG",
    "SYSTEM_PROMPT",
    "create_agent",
    "process_chat_message",
    "get_or_create_conversation",
    "get_conversation_context",
    "save_message",
    "format_messages_for_agent",
]
