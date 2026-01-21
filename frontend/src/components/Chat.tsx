import { useState, useRef, useEffect, FormEvent } from 'react';
import { Bot } from 'lucide-react';
import { sendChatMessage, startNewConversation, ChatResponse, ToolCall } from '../services/api';
import './Chat.css';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  toolCalls?: ToolCall[];
  timestamp: Date;
}

interface ChatProps {
  userId: string;
}

export default function Chat({ userId }: ChatProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Add welcome message on mount
  useEffect(() => {
    const welcomeMessage: Message = {
      id: 'welcome',
      role: 'assistant',
      content: `Hello! I'm your AI task assistant. I can help you manage your todo list.

Try saying things like:
- "Add a task to buy groceries"
- "Show my tasks"
- "Complete task 1"
- "Delete the grocery task"

What would you like to do?`,
      timestamp: new Date(),
    };
    setMessages([welcomeMessage]);
  }, []);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setError(null);

    try {
      const response: ChatResponse = await sendChatMessage(userId, userMessage.content);

      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: response.message,
        toolCalls: response.tool_calls,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setConversationId(response.conversation_id);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to send message';
      setError(errorMessage);

      // Add error message to chat
      const errorAssistantMessage: Message = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: `Sorry, I encountered an error: ${errorMessage}. Please try again.`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorAssistantMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewConversation = async () => {
    try {
      setIsLoading(true);
      const response = await startNewConversation(userId);
      setConversationId(response.conversation_id);
      setMessages([
        {
          id: 'new-conversation',
          role: 'assistant',
          content: 'Started a fresh conversation. How can I help you with your tasks?',
          timestamp: new Date(),
        },
      ]);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start new conversation');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2><Bot size={20} /> AI Task Assistant</h2>
        <button onClick={handleNewConversation} disabled={isLoading} className="new-chat-btn">
          New Chat
        </button>
      </div>

      <div className="messages-container">
        {messages.map((msg) => (
          <div key={msg.id} className={`message ${msg.role}`}>
            <div className="message-content">
              {msg.content.split('\n').map((line, i) => (
                <p key={i}>{line}</p>
              ))}
              {msg.toolCalls && msg.toolCalls.length > 0 && (
                <div className="tool-calls">
                  <small>Actions taken:</small>
                  <ul>
                    {msg.toolCalls.map((tc, i) => (
                      <li key={i}>
                        <code>{tc.tool}</code>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
            <div className="message-time">
              {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message assistant loading">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {error && <div className="error-banner">{error}</div>}

      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message... (e.g., 'Add task to call mom')"
          disabled={isLoading}
          autoFocus
        />
        <button type="submit" disabled={isLoading || !input.trim()}>
          Send
        </button>
      </form>

      {conversationId && (
        <div className="conversation-id">
          <small>Conversation: {conversationId.slice(0, 8)}...</small>
        </div>
      )}
    </div>
  );
}
