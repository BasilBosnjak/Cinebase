import { useState } from 'react';
import { documentsApi } from '../services/api';

export default function DocumentItem({ document, onUpdate, onDelete }) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(document.title || '');

  const handleSave = () => {
    onUpdate(document.id, { title });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setTitle(document.title || '');
    setIsEditing(false);
  };

  if (isEditing) {
    return (
      <div className="bg-white rounded-lg shadow p-4 space-y-3">
        <input
          type="text"
          placeholder="Title (optional)"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <div className="flex gap-2">
          <button
            onClick={handleSave}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Save
          </button>
          <button
            onClick={handleCancel}
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
          >
            Cancel
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow p-4 flex items-start justify-between">
      <div className="flex-1 min-w-0">
        {document.title && (
          <h4 className="text-sm font-medium text-gray-900 truncate">
            {document.title}
          </h4>
        )}
        <div className="flex items-center gap-2 mt-1">
          <svg className="w-5 h-5 text-red-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
          </svg>
          <span className="text-sm font-medium text-gray-900 truncate">
            {document.original_filename}
          </span>
          {document.file_size && (
            <span className="text-xs text-gray-500">
              ({(document.file_size / 1024).toFixed(1)} KB)
            </span>
          )}
        </div>
        <div className="mt-2 flex items-center gap-3">
          <a
            href={documentsApi.getViewUrl(document.id)}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-blue-600 hover:text-blue-800"
          >
            View PDF
          </a>
          <a
            href={documentsApi.getDownloadUrl(document.id)}
            download
            className="text-sm text-blue-600 hover:text-blue-800"
          >
            Download
          </a>
          <span className="text-xs text-gray-500">
            {new Date(document.created_at).toLocaleDateString()}
          </span>
        </div>
      </div>
      <div className="flex gap-2 ml-4">
        <button
          onClick={() => setIsEditing(true)}
          className="px-3 py-1 text-sm text-blue-600 hover:text-blue-800"
        >
          Edit
        </button>
        <button
          onClick={() => onDelete(document.id)}
          className="px-3 py-1 text-sm text-red-600 hover:text-red-800"
        >
          Delete
        </button>
      </div>
    </div>
  );
}
