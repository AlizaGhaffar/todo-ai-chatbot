import { useNavigate } from 'react-router-dom';
import { Bot, Zap, Shield, Brain } from 'lucide-react';
import './LandingPage.css';

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="landing-container">
      {/* Header */}
      <header className="landing-header">
        <div className="logo">
          <Bot className="logo-icon" />
          <span>AI TaskBot</span>
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero-section">
        {/* Cute Robot Mascot */}
        <div className="robot-mascot">
          <div className="robot-container">
            <div className="robot-antenna">
              <div className="antenna-ball"></div>
            </div>
            <div className="robot-head">
              <div className="robot-eyes">
                <div className="robot-eye left">
                  <div className="eye-pupil"></div>
                </div>
                <div className="robot-eye right">
                  <div className="eye-pupil"></div>
                </div>
              </div>
              <div className="robot-mouth"></div>
            </div>
            <div className="robot-body">
              <div className="robot-screen">
                <div className="screen-line"></div>
                <div className="screen-line"></div>
                <div className="screen-line short"></div>
              </div>
            </div>
            <div className="robot-arms">
              <div className="robot-arm left"></div>
              <div className="robot-arm right"></div>
            </div>
          </div>
          <div className="robot-shadow"></div>
        </div>

        {/* Hero Content */}
        <h1 className="hero-title">
          Welcome to <span className="gradient-text">AI TaskBot</span>
        </h1>
        <p className="hero-subtitle">
          Your intelligent AI assistant for managing tasks. Just chat naturally and let our AI handle the rest.
        </p>

        {/* CTA Buttons */}
        <div className="cta-buttons">
          <button className="btn btn-primary" onClick={() => navigate('/login')}>
            Sign In
          </button>
          <button className="btn btn-secondary" onClick={() => navigate('/signup')}>
            Create Account
          </button>
        </div>

        <p className="guest-link" onClick={() => navigate('/tasks')}>
          <Bot size={16} />
          Try without signing up
        </p>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="feature-card">
          <div className="feature-icon">
            <Zap size={24} />
          </div>
          <h3>Lightning Fast</h3>
          <p>Instant AI responses and task updates</p>
        </div>

        <div className="feature-card">
          <div className="feature-icon">
            <Shield size={24} />
          </div>
          <h3>Secure</h3>
          <p>Your data is safe with us</p>
        </div>

        <div className="feature-card">
          <div className="feature-icon">
            <Brain size={24} />
          </div>
          <h3>Smart AI</h3>
          <p>Intelligent task management</p>
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <p>Powered by AI - Built with love</p>
      </footer>
    </div>
  );
}
