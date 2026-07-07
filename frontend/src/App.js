import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [backendHealth, setBackendHealth] = useState('checking');
  const [showSources, setShowSources] = useState(true);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Check backend health
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await axios.get(`${API_URL}/health`, { timeout: 5000 });
        setBackendHealth('connected');
      } catch (error) {
        setBackendHealth('disconnected');
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message
    const userMessage = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post(`${API_URL}/chat`, {
        question: input,
      });

      const { answer, sources, snippets } = response.data;
      const assistantMessage = {
        role: 'assistant',
        content: answer,
        sources: sources || [],
        snippets: snippets || [],
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: `Error: ${error.response?.data?.error || 'Failed to get response from backend'}`,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setMessages([]);
  };

  const getStatusColor = () => {
    return backendHealth === 'connected'
      ? '#4ade80'
      : backendHealth === 'checking'
      ? '#facc15'
      : '#ef4444';
  };

  return (
    <div className="app">
      <div className="container">
        {/* Header */}
        <header className="header">
          <div className="header-content">
            <div className="title-section">
              <h1>🦟 MalariaAI RAG</h1>
              <p>Retrieval Augmented Generation System for Malaria Policies</p>
            </div>
            <div className="header-controls">
              <div className="status-indicator">
                <div
                  className="status-dot"
                  style={{ backgroundColor: getStatusColor() }}
                  title={`Backend: ${backendHealth}`}
                />
                <span className="status-text">{backendHealth}</span>
              </div>
              <button className="btn-clear" onClick={handleClear}>
                Clear Chat
              </button>
            </div>
          </div>
        </header>

        {/* Messages Area */}
        <div className="messages-container">
          {messages.length === 0 ? (
            <div className="welcome-message">
              <h2>Welcome to MalariaAI RAG</h2>
              <p>Ask questions about malaria policies and get answers backed by documents.</p>
              <div className="example-questions">
                <p>Example questions:</p>
                <ul>
                  <li>What are the preventive measures for malaria?</li>
                  <li>What are the treatment protocols for malaria?</li>
                  <li>What is the epidemiology of malaria?</li>
                </ul>
              </div>
            </div>
          ) : (
            messages.map((message, index) => (
              <div key={index} className={`message message-${message.role}`}>
                <div className="message-header">
                  <span className="message-role">
                    {message.role === 'user' ? '👤 You' : '🤖 Assistant'}
                  </span>
                </div>
                <div className="message-content">{message.content}</div>
                {message.sources && message.sources.length > 0 && showSources && (
                  <div className="message-sources">
                    <div className="sources-card">
                      <div className="sources-title">Document Cited</div>
                      <div className="sources-list">
                        {message.sources.map((source, i) => (
                          <div key={i} className="source-item">
                            <span className="source-name">
                              [{source.id || i + 1}] {source.citation || source.document || `Document ${i + 1}`}
                            </span>
                            {source.page_number != null && source.page_number !== undefined && (
                              <span className="source-page">Page {source.page_number}</span>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="sources-card citations-card">
                      <div className="sources-title">Citations</div>
                      <div className="sources-list">
                        {message.sources.map((source, i) => (
                          <div key={i} className="citation-item">
                            <div className="citation-label">
                              <span className="citation-id">[{source.id || i + 1}]</span>
                              <span className="citation-text">
                                {source.citation || source.document || `Document ${i + 1}`}
                              </span>
                            </div>
                            {message.snippets && message.snippets[i] && (
                              <div className="citation-snippet">{message.snippets[i]}</div>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))
          )}
          {loading && (
            <div className="message message-assistant">
              <div className="message-header">
                <span className="message-role">🤖 Assistant</span>
              </div>
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Settings & Input */}
        <div className="input-section">
          <div className="settings">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={showSources}
                onChange={(e) => setShowSources(e.target.checked)}
              />
              Show Sources
            </label>
          </div>

          <form onSubmit={handleSendMessage} className="input-form">
            <div className="input-wrapper">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask a question about malaria policies..."
                disabled={loading || backendHealth === 'disconnected'}
              />
              <button
                type="submit"
                disabled={loading || !input.trim() || backendHealth === 'disconnected'}
                className="btn-send"
              >
                {loading ? '⏳' : '➤'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;
