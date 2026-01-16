import { useState } from 'react';

export default function AddDocumentForm({ onUpload }) {
  const [files, setFiles] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files);

    if (selectedFiles.length === 0) {
      setFiles([]);
      setError('');
      return;
    }

    // Validate batch size
    if (selectedFiles.length > 10) {
      setError('Maximum 10 files allowed per batch');
      setFiles([]);
      return;
    }

    // Validate each file
    const maxSize = 10 * 1024 * 1024; // 10MB in bytes
    const invalidFiles = [];

    for (const file of selectedFiles) {
      // Validate file type
      if (file.type !== 'application/pdf') {
        invalidFiles.push(`${file.name}: Only PDF files are allowed`);
        continue;
      }

      // Validate file size
      if (file.size > maxSize) {
        invalidFiles.push(`${file.name}: File size must be less than 10MB`);
      }
    }

    if (invalidFiles.length > 0) {
      setError(invalidFiles.join('; '));
      setFiles([]);
      return;
    }

    setError('');
    setFiles(selectedFiles);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (files.length === 0) return;

    setUploading(true);
    setError('');

    try {
      const formData = new FormData();

      // Append all files with 'files' field name
      files.forEach(file => {
        formData.append('files', file);
      });

      await onUpload(formData);

      // Reset form
      setFiles([]);
      setIsOpen(false);
    } catch (err) {
      setError(err.message || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
      >
        Upload PDF(s)
      </button>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-4 space-y-3">
      {error && (
        <div className="p-2 bg-red-100 border border-red-400 text-red-700 rounded text-sm">
          {error}
        </div>
      )}

      <div>
        <input
          type="file"
          accept="application/pdf"
          multiple
          onChange={handleFileChange}
          disabled={uploading}
          required
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {files.length > 0 && (
          <div className="mt-2 space-y-1">
            <p className="text-sm font-medium text-gray-700">
              {files.length} file{files.length !== 1 ? 's' : ''} selected:
            </p>
            <ul className="text-sm text-gray-600 space-y-1 max-h-32 overflow-y-auto">
              {files.map((file, index) => (
                <li key={index} className="flex justify-between">
                  <span className="truncate mr-2">{file.name}</span>
                  <span className="text-gray-500 whitespace-nowrap">
                    {formatFileSize(file.size)}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      <div className="flex gap-2">
        <button
          type="submit"
          disabled={files.length === 0 || uploading}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {uploading
            ? 'Uploading...'
            : `Upload ${files.length} PDF${files.length !== 1 ? 's' : ''}`
          }
        </button>
        <button
          type="button"
          onClick={() => {
            setIsOpen(false);
            setFiles([]);
            setError('');
          }}
          disabled={uploading}
          className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 disabled:bg-gray-100 disabled:cursor-not-allowed"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}
