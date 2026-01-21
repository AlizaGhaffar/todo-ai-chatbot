"""
Chat API Routes

Handles chat interactions with the AI agent.
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.database import get_session
from src.auth.config import get_current_user_id
from src.models import MessageRole
from src.services.conversation import (
    get_or_create_conversation,
    get_conversation_context,
    save_message,
    format_messages_for_agent,
)
from src.services.agent import process_chat_message

logger = logging.getLogger(__name__)

router = APIRouter()


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""

    message: str = Field(..., min_length=1, max_length=10000, description="User's message")


class ToolCallInfo(BaseModel):
    """Information about a tool call made by the agent."""

    tool: str
    input: dict


class ChatResponse(BaseModel):
    """Response from chat endpoint."""

    message: str = Field(..., description="Assistant's response")
    conversation_id: str = Field(..., description="Conversation ID")
    tool_calls: Optional[list[ToolCallInfo]] = Field(None, description="Tool calls made")


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    session: AsyncSession = Depends(get_session),
):
    """
    Send a message to the AI assistant.

    The assistant can help with task management:
    - Add tasks: "Add a task to buy groceries"
    - List tasks: "Show my tasks"
    - Complete tasks: "Complete task 1" or "Mark buy groceries as done"
    - Update tasks: "Update task 1 to Review report"
    - Delete tasks: "Delete task 1"

    Args:
        user_id: User identifier
        request: Chat message

    Returns:
        Assistant's response with optional tool call information
    """
    # Validate user_id
    validated_user_id = get_current_user_id(user_id)

    logger.info(f"Chat request from user {validated_user_id}: {request.message[:50]}...")

    try:
        # Get or create conversation
        conversation = await get_or_create_conversation(session, validated_user_id)

        # Get conversation history for context
        history_messages = await get_conversation_context(session, conversation.id)
        formatted_history = format_messages_for_agent(history_messages)

        # Save user message
        await save_message(
            session=session,
            user_id=validated_user_id,
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content=request.message,
        )

        # Process through AI agent
        agent_response = await process_chat_message(
            user_id=validated_user_id,
            message=request.message,
            conversation_history=formatted_history,
        )

        # Save assistant response
        await save_message(
            session=session,
            user_id=validated_user_id,
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content=agent_response["content"],
            tool_calls=agent_response.get("tool_calls"),
        )

        logger.info(f"Chat response sent for user {validated_user_id}")

        return ChatResponse(
            message=agent_response["content"],
            conversation_id=conversation.id,
            tool_calls=[
                ToolCallInfo(**tc) for tc in agent_response.get("tool_calls", [])
            ] if agent_response.get("tool_calls") else None,
        )

    except Exception as e:
        logger.error(f"Chat error for user {validated_user_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat: {str(e)}"
        )


@router.post("/{user_id}/chat/new", response_model=dict)
async def start_new_conversation(
    user_id: str,
    session: AsyncSession = Depends(get_session),
):
    """
    Start a fresh conversation, discarding previous context.

    Args:
        user_id: User identifier

    Returns:
        New conversation ID
    """
    from datetime import datetime
    import uuid
    from src.models import Conversation

    validated_user_id = get_current_user_id(user_id)

    # Create new conversation
    conversation = Conversation(
        id=str(uuid.uuid4()),
        user_id=validated_user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)

    logger.info(f"New conversation {conversation.id} created for user {validated_user_id}")

    return {
        "conversation_id": conversation.id,
        "message": "New conversation started."
    }
