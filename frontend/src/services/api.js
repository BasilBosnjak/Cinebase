const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
    this.name = 'ApiError';
  }
}

async function fetchApi(endpoint, options = {}) {
  const response = await fetch(`${API_URL}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
    throw new ApiError(error.detail || 'Request failed', response.status);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export const authApi = {
  login: async (email) => {
    return fetchApi('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email }),
    });
  },
};

export const usersApi = {
  getDocuments: async (userId) => {
    return fetchApi(`/users/${userId}/documents`);
  },

  uploadDocument: async (userId, formData) => {
    const response = await fetch(`${API_URL}/users/${userId}/documents`, {
      method: 'POST',
      body: formData,
      // No Content-Type header - let browser set multipart boundary
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Upload failed' }));
      throw new ApiError(error.detail || 'Upload failed', response.status);
    }

    return response.json();
  },

  getStats: async (userId) => {
    return fetchApi(`/users/${userId}/stats`);
  },
};

export const documentsApi = {
  update: async (documentId, updates) => {
    return fetchApi(`/documents/${documentId}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  },

  delete: async (documentId) => {
    return fetchApi(`/documents/${documentId}`, {
      method: 'DELETE',
    });
  },

  getDownloadUrl: (documentId) => {
    return `${API_URL}/documents/${documentId}/download`;
  },

  getViewUrl: (documentId) => {
    return `${API_URL}/documents/${documentId}/view`;
  },
};
