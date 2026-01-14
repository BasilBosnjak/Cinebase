# Cinebase

A full-stack application for storing and managing PDF files with email-only authentication. Features intelligent document processing with vector embeddings, semantic search, RAG (Retrieval-Augmented Generation) queries, and AI-powered job matching against uploaded resumes.

## Tech Stack

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Frontend**: React + Vite + Tailwind CSS
- **State Management**: React Context API
- **Database**: PostgreSQL with UUID primary keys + pgvector extension
- **Workflow Automation**: n8n (self-hosted)
- **Embeddings**: Hugging Face API (nomic-embed-text) or Ollama (local)
- **LLM**: Groq API (llama-3.1-8b-instant)
- **Job Search**: JobSpy MCP Server (scrapes Indeed, LinkedIn, Glassdoor, etc.)

## Project Structure

```
Cinebase/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── models/   # SQLAlchemy models
│   │   ├── schemas/  # Pydantic schemas
│   │   ├── routers/  # API endpoints
│   │   └── services/ # Business logic
│   └── requirements.txt
└── frontend/         # React frontend
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── context/
    │   └── services/
    └── package.json
```

## Database Schema

### users table
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PRIMARY KEY |
| email | VARCHAR(255) | UNIQUE, NOT NULL |
| created_at | TIMESTAMP | NOT NULL |

### documents table
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PRIMARY KEY |
| user_id | UUID | FOREIGN KEY → users(id) |
| file_path | VARCHAR(1000) | NOT NULL |
| original_filename | VARCHAR(500) | NOT NULL |
| file_size | INTEGER | NULL |
| mime_type | VARCHAR(100) | NULL |
| title | VARCHAR(500) | NULL |
| content | TEXT | NULL (stores extracted PDF text) |
| embedding | VECTOR(768) | NULL (vector embeddings for semantic search) |
| status | VARCHAR(50) | NOT NULL, DEFAULT 'active' |
| created_at | TIMESTAMP | NOT NULL |
| updated_at | TIMESTAMP | NOT NULL |

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 14+ with pgvector extension
- (Optional) Ollama for local embeddings
- (Optional) n8n for embedding workflow automation
- (Optional) JobSpy MCP Server for job matching

**For Production:**
- Hugging Face API key (for embeddings)
- Groq API key (for LLM)

### 1. Database Setup

```bash
# Create database
createdb linkmanager

# Or using psql
psql -U postgres
CREATE DATABASE linkmanager;
\q

# Enable pgvector extension
psql linkmanager
CREATE EXTENSION IF NOT EXISTS vector;
\q
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Update .env with your configuration:
# DATABASE_URL=postgresql://user:password@localhost:5432/linkmanager
# CORS_ORIGINS=http://localhost:5173,http://localhost:3000
# HUGGINGFACE_API_KEY=your_hf_api_key_here  # For production embeddings
# GROQ_API_KEY=your_groq_api_key_here        # For LLM queries

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Update .env with backend URL
# VITE_API_URL=http://localhost:8000

# Run development server
npm run dev
```

Frontend will be available at `http://localhost:5173`

### 4. Optional: Ollama Setup (Local Embeddings)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull embedding model (768 dimensions)
ollama pull nomic-embed-text

# Pull LLM model (for local RAG)
ollama pull llama3.2:3b

# Verify it's running
curl http://localhost:11434/api/embeddings \
  -d '{"model": "nomic-embed-text", "prompt": "test"}'
```

### 5. Optional: n8n Setup (Embedding Workflow Automation)

```bash
# Install n8n globally
npm install -g n8n

# Start n8n
n8n start

# Access n8n at http://localhost:5678
# Import the embedding workflow (see CLAUDE.md for workflow details)
```

### 6. Optional: JobSpy MCP Server (Job Matching)

```bash
# Clone and setup JobSpy MCP Server
cd /path/to/repos
git clone https://github.com/your-repo/jobspy-mcp-server
cd jobspy-mcp-server

# Install dependencies
npm install

# Start the server
ENABLE_SSE=1 node src/index.js

# Server runs at http://localhost:9423
# Health check: curl http://localhost:9423/health
```

## Testing the Complete Flow

### 1. Create a test user in the database

```bash
psql linkmanager
```

```sql
INSERT INTO users (id, email, created_at)
VALUES (gen_random_uuid(), 'test@example.com', NOW());
```

### 2. Test the application

1. Open `http://localhost:5173` in your browser
2. Enter `test@example.com` in the login form
3. You should be redirected to the dashboard
4. Click "Upload PDF" button
5. Select a PDF file from your computer and enter an optional title
6. Click "Upload PDF" - the file will be uploaded, text extracted, and embedding generated in the background
7. Click "View PDF" to open the PDF in a new tab
8. Click "Download" to download the PDF file
9. Click "Edit" to modify the document title
10. Click "Delete" to remove the document (deletes both DB record and file)
11. Verify stats cards update correctly

### 3. Test API endpoints directly

```bash
# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'

# Get user documents (replace USER_ID with actual UUID)
curl http://localhost:8000/users/{USER_ID}/documents

# Upload PDF (requires a PDF file)
curl -X POST http://localhost:8000/users/{USER_ID}/documents \
  -F "file=@sample.pdf" \
  -F "title=My Document"

# Get stats
curl http://localhost:8000/users/{USER_ID}/stats

# Download document
curl http://localhost:8000/documents/{DOCUMENT_ID}/download -o downloaded.pdf

# View document (inline)
curl http://localhost:8000/documents/{DOCUMENT_ID}/view

# RAG query
curl -X POST http://localhost:8000/rag/query \
  -H "Content-Type: application/json" \
  -d '{"user_id": "{USER_ID}", "query": "What are the main topics in my documents?"}'

# Job matching (requires resume PDF with embedding)
curl -X POST http://localhost:8000/jobs/match \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "{USER_ID}",
    "search_term": "software engineer",
    "location": "Remote",
    "results_wanted": 10,
    "is_remote": true
  }'
```

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | Email lookup - returns user data if exists |

### Document Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/{user_id}/documents` | Get all PDF documents for user |
| POST | `/users/{user_id}/documents` | Upload new PDF (multipart/form-data, extracts text + generates embedding) |
| PUT | `/documents/{document_id}` | Update document (title, status) |
| DELETE | `/documents/{document_id}` | Delete document (DB + file) |
| GET | `/documents/{document_id}/download` | Download PDF file |
| GET | `/documents/{document_id}/view` | View PDF inline |
| GET | `/users/{user_id}/stats` | Get dashboard stats |

### RAG & AI Features
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/rag/query` | Query documents using RAG (semantic search + LLM) |

### Job Matching
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/jobs/match` | Match jobs against user's resume (requires uploaded PDF with embedding) |
| GET | `/jobs/search` | Direct job search (proxy to JobSpy, no matching) |

## Features

### Core Features
- Email-only authentication (no passwords)
- PDF file upload and storage (local filesystem)
- Automatic PDF text extraction (using pypdf)
- Document management (upload, view, download, edit, delete)
- Dashboard with real-time statistics
- Responsive design with Tailwind CSS
- File size validation (10MB max)
- Secure file storage with UUID-based filenames

### AI & Semantic Search
- **Vector Embeddings**: Automatic generation of 768-dimensional embeddings for all uploaded PDFs
- **Semantic Search**: Find documents by meaning, not just keywords
- **RAG Queries**: Ask questions about your documents, get AI-generated answers with source citations
- **Cloud Deployment Ready**: Uses Hugging Face API for embeddings, Groq for LLM (or Ollama for local)

### Job Matching
- **Resume Analysis**: Upload your resume/CV as a PDF
- **AI-Powered Matching**: Automatically matches job postings to your resume using semantic similarity
- **Multi-Platform Search**: Searches Indeed, LinkedIn, Glassdoor, ZipRecruiter, and more via JobSpy
- **Relevance Scoring**: Jobs ranked by similarity score (0-1 scale)
- **Smart Job Title Extraction**: LLM extracts optimal job title from your resume

## Development Notes

### Architecture
- Backend uses SQLAlchemy ORM with PostgreSQL + pgvector extension
- Frontend uses React Context for state management
- All API calls centralized in `frontend/src/services/api.js`
- Database tables created automatically on backend startup (no Alembic migrations)
- Status field defaults to "active" (not "pending") - documents are immediately active

### AI/ML Pipeline
- **Embeddings**: Generated via background task after PDF upload using Hugging Face API (production) or Ollama (local)
- **Vector Storage**: 768-dimensional embeddings stored in PostgreSQL using pgvector
- **RAG**: Combines semantic search (cosine similarity) with LLM text generation
- **Job Matching**: Calculates cosine similarity between resume embedding and job description embeddings

### Deployment
- **Frontend**: Deploy to Vercel (requires `vercel.json` in frontend directory for SPA routing)
- **Backend**: Deploy to any Python-compatible platform (Railway, Render, Fly.io, etc.)
- **Environment Variables Required**:
  - `DATABASE_URL`: PostgreSQL connection string
  - `HUGGINGFACE_API_KEY`: For embeddings in production
  - `GROQ_API_KEY`: For LLM queries
  - `CORS_ORIGINS`: Comma-separated list of allowed origins

### Key Implementation Details
- All IDs use UUIDs (not serial integers)
- Foreign key cascade: Deleting a user deletes all their documents
- File storage uses UUID-based filenames for security
- Embedding generation happens asynchronously (non-blocking)

For detailed implementation guidance, see `CLAUDE.md` in the repository root.
