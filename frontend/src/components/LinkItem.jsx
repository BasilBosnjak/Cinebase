import { useState } from 'react';

export default function LinkItem({ link, onUpdate, onDelete }) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(link.title || '');
  const [url, setUrl] = useState(link.url);

  const handleSave = () => {
    onUpdate(link.id, { title, url });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setTitle(link.title || '');
    setUrl(link.url);
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
        <input
          type="url"
          placeholder="URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
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
        {link.title && (
          <h4 className="text-sm font-medium text-gray-900 truncate">
            {link.title}
          </h4>
        )}
        <a
          href={link.url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-sm text-blue-600 hover:text-blue-800 truncate block"
        >
          {link.url}
        </a>
        <div className="mt-2 flex items-center gap-3 text-xs text-gray-500">
          <span className="px-2 py-1 rounded-full bg-green-100 text-green-800">
            {link.status}
          </span>
          <span>{new Date(link.created_at).toLocaleDateString()}</span>
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
          onClick={() => onDelete(link.id)}
          className="px-3 py-1 text-sm text-red-600 hover:text-red-800"
        >
          Delete
        </button>
      </div>
    </div>
  );
}
