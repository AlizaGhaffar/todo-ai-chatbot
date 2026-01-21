import { Link } from 'react-router-dom';
import { Bot, ArrowLeft } from 'lucide-react';
import Chat from '../components/Chat';
import { getCurrentUserId } from '../services/tasks';
import '../components/Chat.css';

export default function ChatPage() {
  const userId = getCurrentUserId();

  return (
    <div className="chat-page">
      <header className="chat-page-header">
        <Link to="/" className="logo">
          <Bot className="logo-icon" />
          <span>AI TaskBot</span>
        </Link>

        <Link to="/tasks" className="back-btn">
          <ArrowLeft size={18} />
          Back to Tasks
        </Link>
      </header>

      <div className="chat-wrapper">
        <Chat userId={userId} />
      </div>
    </div>
  );
}
