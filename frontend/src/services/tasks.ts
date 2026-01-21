/**
 * Tasks Service for AI Todo Chatbot
 *
 * Handles task operations with the backend API.
 */

import { getAuthHeaders, getUser } from './auth';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

// Helper to get status string
export function getTaskStatus(task: Task): 'pending' | 'completed' {
  return task.completed ? 'completed' : 'pending';
}

/**
 * Fetch all tasks for the current user.
 */
export async function fetchTasks(): Promise<Task[]> {
  const user = getUser();

  // For guests, use a generated user ID
  const userId = user?.id || getGuestUserId();

  const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks`, {
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
  });

  if (!response.ok) {
    // If 404, return empty array (no tasks endpoint yet)
    if (response.status === 404) {
      return [];
    }
    throw new Error('Failed to fetch tasks');
  }

  return response.json();
}

/**
 * Get or generate a guest user ID.
 * Stored in localStorage for persistence.
 */
export function getGuestUserId(): string {
  const GUEST_ID_KEY = 'guest_user_id';
  let guestId = localStorage.getItem(GUEST_ID_KEY);

  if (!guestId) {
    guestId = `guest-${Math.random().toString(36).substring(2, 10)}`;
    localStorage.setItem(GUEST_ID_KEY, guestId);
  }

  return guestId;
}

/**
 * Get the current user ID (authenticated or guest).
 */
export function getCurrentUserId(): string {
  const user = getUser();
  return user?.id || getGuestUserId();
}
