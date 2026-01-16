import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../context/UserContext';
import { usersApi, documentsApi } from '../services/api';
import StatsCard from '../components/StatsCard';
import DocumentItem from '../components/DocumentItem';
import AddDocumentForm from '../components/AddDocumentForm';

export default function Dashboard() {
  const { user, logout } = useUser();
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!user) {
      navigate('/');
      return;
    }
    loadData();
  }, [user, navigate]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [statsData, documentsData] = await Promise.all([
        usersApi.getStats(user.id),
        usersApi.getDocuments(user.id),
      ]);
      setStats(statsData);
      setDocuments(documentsData);
      setError('');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleUploadDocument = async (formData) => {
    try {
      await usersApi.uploadDocument(user.id, formData);
      loadData();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleUpdateDocument = async (documentId, updates) => {
    try {
      await documentsApi.update(documentId, updates);
      loadData();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDeleteDocument = async (documentId) => {
    if (!confirm('Are you sure you want to delete this document?')) return;
    try {
      await documentsApi.delete(documentId);
      loadData();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-gray-600">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">PDF Manager</h1>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-600">{user?.email}</span>
            <button
              onClick={() => navigate('/chat')}
              className="px-4 py-2 text-sm bg-purple-600 text-white rounded-md hover:bg-purple-700"
            >
              Ask Questions
            </button>
            <button
              onClick={handleLogout}
              className="px-4 py-2 text-sm text-gray-700 hover:text-gray-900"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-4 p-4 bg-red-50 text-red-600 rounded-lg">
            {error}
          </div>
        )}

        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <StatsCard
              title="Total Documents"
              value={stats.total_documents}
            />
            <StatsCard
              title="Recent (7 days)"
              value={stats.recent_documents_count}
            />
          </div>
        )}

        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-gray-900">Your Documents</h2>

          <AddDocumentForm onUpload={handleUploadDocument} />

          {documents.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              No documents yet. Upload your first PDF above!
            </div>
          ) : (
            <div className="space-y-3">
              {documents.map((document) => (
                <DocumentItem
                  key={document.id}
                  document={document}
                  onUpdate={handleUpdateDocument}
                  onDelete={handleDeleteDocument}
                />
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
