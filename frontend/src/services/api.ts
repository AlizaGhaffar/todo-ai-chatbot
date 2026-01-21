/**
 * API Service for AI Todo Chatbot
 *
 * Handles communication with the backend chat API.
 */

import { getAuthHeaders } from './auth';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Ensure API paths include /api prefix
const getApiUrl = (path: string) => `${API_BASE_URL}/api${path}`;

export interface ToolCall {
  tool: string;
  input: Record<string, unknown>;
}

export interface ChatResponse {
  message: string;
  conversation_id: string;
  tool_calls?: ToolCall[];
}

export interface ChatError {
  error: string;
  details?: Record<string, unknown>;
}

/**
 * Send a chat message to the AI assistant.
 *
 * @param userId - User identifier
 * @param message - User's message
 * @returns Chat response from the assistant
 */
export async function sendChatMessage(
  userId: string,
  message: string
): Promise<ChatResponse> {
  const response = await fetch(getApiUrl(`/${userId}/chat`), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
    body: JSON.stringify({ message }),
  });

  if (!response.ok) {
    const error: ChatError = await response.json().catch(() => ({
      error: 'Unknown error occurred',
    }));
    throw new Error(error.error || `HTTP ${response.status}`);
  }

  return response.json();
}

/**
 * Start a new conversation, discarding previous context.
 *
 * @param userId - User identifier
 * @returns New conversation info
 */
export async function startNewConversation(
  userId: string
): Promise<{ conversation_id: string; message: string }> {
  const response = await fetch(getApiUrl(`/${userId}/chat/new`), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
  });

  if (!response.ok) {
    const error: ChatError = await response.json().catch(() => ({
      error: 'Unknown error occurred',
    }));
    throw new Error(error.error || `HTTP ${response.status}`);
  }

  return response.json();
}

/**
 * Check API health status.
 *
 * @returns Health status
 */
export async function checkHealth(): Promise<{
  status: string;
  service: string;
  database: { status: string };
}> {
  const response = await fetch(`${API_BASE_URL}/health`);

  if (!response.ok) {
    throw new Error(`Health check failed: HTTP ${response.status}`);
  }

  return response.json();
}
