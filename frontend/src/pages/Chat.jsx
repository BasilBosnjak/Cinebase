import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../context/UserContext';
import { usersApi, ragApi } from '../services/api';

export default function Chat() {
  const { user } = useUser();
  const navigate = useNavigate();
  const messagesEndRef = useRef(null);

  const [messages, setMessages] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [selectedDoc, setSelectedDoc] = useState(null);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [loadingDocs, setLoadingDocs] = useState(true);

  useEffect(() => {
    if (!user) {
      navigate('/');
      return;
    }
    loadDocuments();
  }, [user, navigate]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const loadDocuments = async () => {
    try {
      setLoadingDocs(true);
      const docs = await usersApi.getDocuments(user.id);
      setDocuments(docs);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingDocs(false);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage = {
      type: 'user',
      content: input,
      timestamp: Date.now(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    setError('');

    try {
      const response = await ragApi.query(user.id, input, selectedDoc);

      const aiMessage = {
        type: 'ai',
        content: response.answer,
        sources: response.sources || [],
        timestamp: Date.now(),
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      setError(err.message);
      const errorMessage = {
        type: 'ai',
        content: 'Sorry, I encountered an error processing your question.',
        timestamp: Date.now(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (loadingDocs) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-gray-600">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">Ask Questions</h1>
            <div className="flex items-center gap-4">
              <select
                value={selectedDoc || ''}
                onChange={e => setSelectedDoc(e.target.value || null)}
                className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Documents</option>
                {documents.map(doc => (
                  <option key={doc.id} value={doc.id}>
                    {doc.original_filename}
                  </option>
                ))}
              </select>
              <button
                onClick={() => navigate('/dashboard')}
                className="px-4 py-2 text-sm text-gray-700 hover:text-gray-900"
              >
                Back to Dashboard
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Error Alert */}
      {error && (
        <div className="max-w-4xl mx-auto w-full px-4 pt-4">
          <div className="p-4 bg-red-50 text-red-600 rounded-lg">
            {error}
          </div>
        </div>
      )}

      {/* No Documents Message */}
      {documents.length === 0 && (
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <p className="text-gray-600 mb-4">
              You haven't uploaded any documents yet.
            </p>
            <button
              onClick={() => navigate('/dashboard')}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Upload a PDF
            </button>
          </div>
        </div>
      )}

      {/* Chat Messages */}
      {documents.length > 0 && (
        <>
          <main className="flex-1 max-w-4xl mx-auto w-full px-4 py-8 overflow-y-auto">
            {messages.length === 0 ? (
              <div className="text-center text-gray-500 py-12">
                <p className="text-lg mb-2">Welcome to your document assistant!</p>
                <p className="text-sm">Ask questions about your uploaded PDFs.</p>
              </div>
            ) : (
              <div className="space-y-4">
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex ${
                      message.type === 'user' ? 'justify-end' : 'justify-start'
                    }`}
                  >
                    <div
                      className={`max-w-2xl px-4 py-3 rounded-lg ${
                        message.type === 'user'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 text-gray-900'
                      }`}
                    >
                      <p className="whitespace-pre-wrap">{message.content}</p>
                      {message.sources && message.sources.length > 0 && (
                        <div className="mt-3 pt-3 border-t border-gray-300">
                          <p className="text-sm font-semibold mb-1">Sources:</p>
                          <div className="space-y-1">
                            {message.sources.map((source, idx) => (
                              <div key={idx} className="text-sm text-gray-600">
                                {source.filename} ({Math.round(source.similarity * 100)}% match)
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
            <div ref={messagesEndRef} />
          </main>

          {/* Input Area */}
          <div className="bg-white border-t border-gray-200">
            <div className="max-w-4xl mx-auto w-full px-4 py-4">
              {loading && (
                <div className="mb-2 text-sm text-gray-600">
                  Generating answer...
                </div>
              )}
              <div className="flex gap-2">
                <textarea
                  value={input}
                  onChange={e => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                  rows="2"
                  placeholder="Ask a question about your documents..."
                  disabled={loading}
                />
                <button
                  onClick={handleSend}
                  disabled={!input.trim() || loading}
                  className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
                >
                  Send
                </button>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
