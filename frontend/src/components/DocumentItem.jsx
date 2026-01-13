import { useState } from 'react';
import { documentsApi, jobsApi } from '../services/api';

export default function DocumentItem({ document, onUpdate, onDelete }) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(document.title || '');
  const [showJobModal, setShowJobModal] = useState(false);
  const [jobMatches, setJobMatches] = useState(null);
  const [jobLoading, setJobLoading] = useState(false);
  const [jobError, setJobError] = useState('');

  const handleSave = () => {
    onUpdate(document.id, { title });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setTitle(document.title || '');
    setIsEditing(false);
  };

  const handleFindJobs = async () => {
    setShowJobModal(true);
    setJobLoading(true);
    setJobError('');
    setJobMatches(null);

    try {
      const result = await jobsApi.matchJobs(document.id);
      setJobMatches(result);
    } catch (err) {
      setJobError(err.message || 'Failed to find matching jobs');
    } finally {
      setJobLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 0.8) return 'text-green-600 bg-green-100';
    if (score >= 0.6) return 'text-yellow-600 bg-yellow-100';
    return 'text-gray-600 bg-gray-100';
  };

  const getScoreLabel = (score) => {
    if (score >= 0.8) return 'Excellent';
    if (score >= 0.6) return 'Good';
    if (score >= 0.4) return 'Fair';
    return 'Low';
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
    <>
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
            <button
              onClick={handleFindJobs}
              className="text-sm text-green-600 hover:text-green-800 font-medium"
            >
              Find Jobs
            </button>
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

      {/* Job Matches Modal */}
      {showJobModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[80vh] overflow-hidden flex flex-col">
            <div className="p-4 border-b flex justify-between items-center">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">
                  Job Matches for {document.original_filename}
                </h3>
                {jobMatches && (
                  <p className="text-sm text-gray-500">
                    Searched for: "{jobMatches.query}" - Found {jobMatches.total_jobs_fetched} jobs
                  </p>
                )}
              </div>
              <button
                onClick={() => setShowJobModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-4">
              {jobLoading && (
                <div className="text-center py-12">
                  <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-600 border-t-transparent"></div>
                  <p className="mt-3 text-gray-600">Analyzing your CV and finding matching jobs...</p>
                  <p className="text-sm text-gray-500">This may take a minute</p>
                </div>
              )}

              {jobError && (
                <div className="p-4 bg-red-50 text-red-600 rounded-lg">
                  {jobError}
                </div>
              )}

              {!jobLoading && jobMatches && jobMatches.matches.length === 0 && (
                <div className="text-center py-12 text-gray-500">
                  No matching jobs found. Try uploading a more detailed CV.
                </div>
              )}

              {!jobLoading && jobMatches && jobMatches.matches.length > 0 && (
                <div className="space-y-3">
                  {jobMatches.matches.map((job, index) => (
                    <div key={job.id || index} className="border rounded-lg p-4">
                      <div className="flex items-start justify-between gap-4">
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="text-sm font-bold text-gray-400">#{index + 1}</span>
                            <h4 className="font-semibold text-gray-900 truncate">{job.title}</h4>
                          </div>
                          <p className="text-sm text-gray-700 font-medium">{job.company}</p>
                          <p className="text-sm text-gray-500">{job.location}</p>
                          {(job.salary_min || job.salary_max) && (
                            <p className="text-sm text-green-600 mt-1">
                              {job.salary_min && job.salary_max
                                ? `$${job.salary_min.toLocaleString()} - $${job.salary_max.toLocaleString()}`
                                : job.salary_min
                                ? `From $${job.salary_min.toLocaleString()}`
                                : `Up to $${job.salary_max.toLocaleString()}`
                              }
                            </p>
                          )}
                          <p className="text-sm text-gray-600 mt-2 line-clamp-2">{job.description}</p>
                          <a
                            href={job.job_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-block mt-2 text-sm text-blue-600 hover:text-blue-800"
                          >
                            View Job Posting
                          </a>
                        </div>
                        <div className="flex-shrink-0 text-right">
                          <div className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getScoreColor(job.similarity_score)}`}>
                            {Math.round(job.similarity_score * 100)}%
                          </div>
                          <p className="text-xs text-gray-500 mt-1">
                            {getScoreLabel(job.similarity_score)}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="p-4 border-t">
              <button
                onClick={() => setShowJobModal(false)}
                className="w-full px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
