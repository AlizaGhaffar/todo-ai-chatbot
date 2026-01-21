import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  Bot, LogOut, Plus, CheckSquare, Square, Trash2,
  MessageCircle, AlertCircle
} from 'lucide-react';
import { getUser, isAuthenticated, logout } from '../services/auth';
import { fetchTasks, Task } from '../services/tasks';
import './TasksPage.css';

export default function TasksPage() {
  const navigate = useNavigate();
  const user = getUser();
  const isGuest = !isAuthenticated();

  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      setLoading(true);
      const data = await fetchTasks();
      setTasks(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const completedCount = tasks.filter(t => t.completed).length;
  const pendingCount = tasks.filter(t => !t.completed).length;

  return (
    <div className="tasks-container">
      {/* Header */}
      <header className="tasks-header">
        <Link to="/" className="logo">
          <Bot className="logo-icon" />
          <span>AI TaskBot</span>
        </Link>

        <div className="header-actions">
          {isGuest ? (
            <button className="create-account-btn" onClick={() => navigate('/signup')}>
              Create Account
            </button>
          ) : (
            <button className="logout-btn" onClick={handleLogout}>
              <LogOut size={18} />
              Logout
            </button>
          )}
        </div>
      </header>

      {/* Guest Banner */}
      {isGuest && (
        <div className="guest-banner">
          <AlertCircle size={18} />
          <div>
            <strong>Guest Mode</strong>
            <span>Tasks are saved in your browser only. Create an account to save permanently!</span>
          </div>
          <button onClick={() => navigate('/signup')}>Create Account</button>
        </div>
      )}

      {/* Main Content */}
      <main className="tasks-main">
        <div className="tasks-title-section">
          <h1>My Tasks</h1>
          {isGuest ? (
            <p>Try out AI TaskBot - no account needed!</p>
          ) : (
            <p>Welcome back, {user?.name}!</p>
          )}
        </div>

        {/* AI Chatbot Button */}
        <div className="chatbot-card">
          <div className="chatbot-info">
            <div className="chatbot-icon">
              <MessageCircle size={24} />
            </div>
            <div>
              <h3>AI Task Assistant</h3>
              <p>Chat with AI to manage your tasks naturally</p>
            </div>
          </div>
          <button className="chatbot-btn" onClick={() => navigate('/chat')}>
            <Bot size={20} />
            Open Chatbot
          </button>
        </div>

        {/* Task List */}
        <div className="tasks-card">
          <div className="tasks-card-header">
            <h2>Tasks</h2>
            <span className="task-count">{tasks.length} tasks</span>
          </div>

          {loading ? (
            <div className="tasks-loading">Loading tasks...</div>
          ) : error ? (
            <div className="tasks-error">{error}</div>
          ) : tasks.length === 0 ? (
            <div className="tasks-empty">
              <CheckSquare size={48} />
              <p>No tasks yet! Use the AI chatbot to add your first task.</p>
              <button onClick={() => navigate('/chat')}>
                <Plus size={18} />
                Add Task via Chat
              </button>
            </div>
          ) : (
            <div className="task-list">
              {tasks.map((task) => (
                <div
                  key={task.id}
                  className={`task-item ${task.completed ? 'completed' : ''}`}
                >
                  <div className="task-checkbox">
                    {task.completed ? (
                      <CheckSquare size={20} className="checked" />
                    ) : (
                      <Square size={20} />
                    )}
                  </div>
                  <div className="task-content">
                    <span className="task-title">{task.title}</span>
                    <span className="task-date">
                      {new Date(task.created_at).toLocaleDateString('en-US', {
                        month: 'short',
                        day: 'numeric',
                        year: 'numeric'
                      })}
                    </span>
                  </div>
                  <div className="task-actions">
                    <button className="delete-btn" title="Use chatbot to delete">
                      <Trash2 size={16} />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Stats */}
        <div className="tasks-stats">
          <div className="stat-card">
            <span className="stat-dot blue"></span>
            <span className="stat-label">Total</span>
            <span className="stat-value">{tasks.length}</span>
          </div>
          <div className="stat-card">
            <span className="stat-dot green"></span>
            <span className="stat-label">Completed</span>
            <span className="stat-value completed">{completedCount}</span>
          </div>
          <div className="stat-card">
            <span className="stat-dot yellow"></span>
            <span className="stat-label">Pending</span>
            <span className="stat-value pending">{pendingCount}</span>
          </div>
        </div>
      </main>
    </div>
  );
}
