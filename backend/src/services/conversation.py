"""
Conversation Service

Handles conversation and message persistence.
"""

import logging
from datetime import datetime
from typing import Optional
import uuid

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import Conversation, Message, MessageRole, MessageCreate

logger = logging.getLogger(__name__)

# Maximum messages to include in context
MAX_CONTEXT_MESSAGES = 10


async def get_or_create_conversation(
    session: AsyncSession,
    user_id: str
) -> Conversation:
    """
    Get the active conversation for a user, or create one if none exists.

    Args:
        session: Database session
        user_id: User's ID

    Returns:
        Active Conversation for the user
    """
    # Find the most recent conversation for the user
    query = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .limit(1)
    )
    result = await session.execute(query)
    conversation = result.scalar_one_or_none()

    if conversation:
        logger.debug(f"Found existing conversation {conversation.id} for user {user_id}")
        return conversation

    # Create new conversation
    conversation = Conversation(
        id=str(uuid.uuid4()),
        user_id=user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)

    logger.info(f"Created new conversation {conversation.id} for user {user_id}")
    return conversation


async def get_conversation_context(
    session: AsyncSession,
    conversation_id: str,
    limit: int = MAX_CONTEXT_MESSAGES
) -> list[Message]:
    """
    Get recent messages for conversation context.

    Args:
        session: Database session
        conversation_id: Conversation ID
        limit: Maximum messages to retrieve

    Returns:
        List of recent messages in chronological order
    """
    query = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    )
    result = await session.execute(query)
    messages = result.scalars().all()

    # Reverse to get chronological order
    return list(reversed(messages))


async def save_message(
    session: AsyncSession,
    user_id: str,
    conversation_id: str,
    role: MessageRole,
    content: str,
    tool_calls: Optional[list[dict]] = None
) -> Message:
    """
    Save a message to the conversation.

    Args:
        session: Database session
        user_id: User's ID
        conversation_id: Conversation ID
        role: Message role (user/assistant)
        content: Message content
        tool_calls: Optional tool calls (for assistant messages)

    Returns:
        Created Message
    """
    message = Message(
        id=str(uuid.uuid4()),
        user_id=user_id,
        conversation_id=conversation_id,
        role=role,
        content=content,
        tool_calls=tool_calls,
        created_at=datetime.utcnow(),
    )
    session.add(message)

    # Update conversation timestamp
    query = select(Conversation).where(Conversation.id == conversation_id)
    result = await session.execute(query)
    conversation = result.scalar_one_or_none()
    if conversation:
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)

    await session.commit()
    await session.refresh(message)

    logger.debug(f"Saved {role.value} message {message.id} to conversation {conversation_id}")
    return message


def format_messages_for_agent(messages: list[Message]) -> list[dict]:
    """
    Format messages for the OpenAI Agents SDK.

    Args:
        messages: List of Message objects

    Returns:
        List of message dicts in OpenAI format
    """
    formatted = []
    for msg in messages:
        formatted.append({
            "role": msg.role.value,
            "content": msg.content,
        })
    return formatted
