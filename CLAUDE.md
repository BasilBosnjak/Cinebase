# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Cinebase is a full-stack application for storing and managing PDF files with email-only authentication. The project is structured for future RAG (Retrieval-Augmented Generation) integration, storing PDF content in the database for processing.

**Tech Stack:**
- Backend: FastAPI + SQLAlchemy + PostgreSQL
- Frontend: React + Vite + Tailwind CSS
- State Management: React Context API
- Database: PostgreSQL with UUID primary keys + pgvector extension
- Workflow Automation: n8n (self-hosted)
- Embeddings: Ollama with nomic-embed-text model
- LLM: Ollama with llama3.2:3b model
- Job Search: JobSpy MCP Server (scrapes Indeed, LinkedIn, Glassdoor, etc.)

## Development Commands

### Backend (Python/FastAPI)

```bash
cd backend

# Setup
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file with:
# DATABASE_URL=postgresql://user:password@localhost:5432/linkmanager
# CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# API documentation available at:
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc)
```

### Frontend (React/Vite)

```bash
cd frontend

# Setup
npm install

# Create .env file with:
# VITE_API_URL=http://localhost:8000

# Run development server (port 5173)
npm run dev

# Build for production
npm build

# Lint code
npm run lint

# Preview production build
npm run preview
```

### Database Setup

```bash
# Create PostgreSQL database
createdb linkmanager

# Or using psql
psql -U postgres -c "CREATE DATABASE linkmanager;"

# Create a test user
psql linkmanager -c "INSERT INTO users (id, email, created_at) VALUES (gen_random_uuid(), 'test@example.com', NOW());"
```

## Architecture

### Backend Architecture

**Database Schema Management:**
- Uses SQLAlchemy's `Base.metadata.create_all()` in `app/main.py` - tables are auto-created on startup
- **No Alembic migrations** - schema changes are applied at the model level
- All IDs use UUIDs (not serial integers)

**Request Flow:**
```
FastAPI Router → Pydantic Schema (validation) → SQLAlchemy Model → PostgreSQL
```

**Module Structure:**
- `app/models/` - SQLAlchemy ORM models (User, Link)
- `app/schemas/` - Pydantic models for request/response validation
- `app/routers/` - API endpoint handlers (auth, users, links)
- `app/services/` - Business logic (currently empty, for future use)
- `app/database.py` - Database connection and session management
- `app/config.py` - Settings via pydantic-settings

**Key Design Patterns:**
- Routers are organized by resource (not by operation)
- Status field defaults to "active" (not "pending") - links are immediately active
- Foreign key cascade: Deleting a user deletes all their links (`ON DELETE CASCADE`)

### Frontend Architecture

**State Management:**
- User authentication state: React Context (`src/context/UserContext.jsx`)
- Persisted to localStorage for session persistence
- No Redux or Zustand - Context API only

**API Communication:**
- **All API calls centralized** in `src/services/api.js`
- Custom `ApiError` class for error handling
- Three namespaced API modules: `authApi`, `usersApi`, `linksApi`

**Component Structure:**
```
App.jsx (Router)
  → UserProvider (Context)
    → Login (page) OR Dashboard (page, protected)
      → StatsCard, LinkItem, AddLinkForm (components)
```

**Routing:**
- React Router DOM with protected routes
- `ProtectedRoute` component checks authentication before rendering
- Unauthenticated users redirected to login

**Key Frontend Patterns:**
- All async operations have loading and error states
- Components follow controlled input pattern
- Modal/forms use local state toggle pattern (open/closed)

## RAG & Embedding System

### Overview
When a PDF is uploaded, an n8n workflow automatically generates vector embeddings for semantic search and RAG queries.

### Workflow Flow
```
User uploads PDF → FastAPI saves & extracts text → Triggers n8n webhook →
n8n generates embedding via Ollama → Stores vector in PostgreSQL (pgvector) →
Ready for semantic search/RAG queries
```

### n8n Workflow Nodes
1. **Webhook** - Receives `document_id` from FastAPI on PDF upload
2. **PostgreSQL** - Fetches document content: `SELECT id, user_id, content, original_filename FROM documents WHERE id = '{{ $json.body.document_id }}'::uuid`
3. **JavaScript (Chunking)** - Splits text into 2000-char chunks with sanitization
4. **HTTP Request (Ollama)** - Calls `http://localhost:11434/api/embeddings` with `nomic-embed-text` model
5. **JavaScript (Averaging)** - Averages chunk embeddings into single document embedding
6. **PostgreSQL** - Updates document: `UPDATE documents SET embedding = '{{ JSON.stringify($json.embedding) }}'::vector WHERE id = '{{ $json.document_id }}'::uuid`

### Setup Requirements

**Ollama:**
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull embedding model (768 dimensions)
ollama pull nomic-embed-text

# Verify it's running
curl http://localhost:11434/api/embeddings -d '{"model": "nomic-embed-text", "prompt": "test"}'
```

**PostgreSQL pgvector:**
```sql
CREATE EXTENSION IF NOT EXISTS vector;
ALTER TABLE documents ADD COLUMN embedding vector(768);
```

**n8n:**
- Self-hosted at `http://localhost:5678`
- Webhook URL configured in `backend/app/routers/users.py` (upload endpoint)
- Workflow must be **activated** (toggle in top-right of n8n editor)

### RAG Query Endpoint
- `POST /rag/query` - Forwards queries to n8n workflow for RAG processing
- Located in `backend/app/routers/rag.py`

## Job Matching System

### Overview
The job matching feature uses semantic similarity to match job postings against the user's uploaded resume. Jobs are fetched from multiple job boards via the JobSpy MCP Server.

### Job Matching Flow
```
User requests job match (POST /jobs/match) →
FastAPI fetches user's resume embedding from PostgreSQL →
FastAPI calls JobSpy MCP Server to search jobs →
For each job: generate embedding via Ollama →
Calculate cosine similarity between resume & job embeddings →
Return jobs ranked by similarity score
```

### JobSpy MCP Server Setup
Located at `/home/basil/repos/jobspy-mcp-server`

```bash
# Start the MCP server (required for job matching)
cd /home/basil/repos/jobspy-mcp-server
ENABLE_SSE=1 node src/index.js

# Server runs at http://localhost:9423
# Health check: curl http://localhost:9423/health
```

**Supported Job Boards:**
- Indeed
- LinkedIn
- Glassdoor
- Google Jobs
- ZipRecruiter
- Bayt
- Naukri

### Job Matching Endpoints
Located in `backend/app/routers/jobs.py`:

- `POST /jobs/match` - Match jobs against user's resume
  ```json
  {
    "user_id": "uuid",
    "search_term": "software engineer",
    "location": "Remote",
    "results_wanted": 10,
    "is_remote": true
  }
  ```
  Returns jobs ranked by `similarity_score` (0-1, higher = better match)

- `GET /jobs/search` - Direct job search without matching (proxy to JobSpy)

### How Similarity Matching Works
1. Resume text is converted to a 768-dimensional vector (embedding)
2. Each job description is also converted to a 768-dimensional vector
3. Cosine similarity measures the angle between vectors
4. Score of 1.0 = identical meaning, 0.0 = unrelated, -1.0 = opposite

## Important Implementation Details

### Authentication
- **Email-only authentication** - no passwords or OAuth
- Login endpoint checks if email exists in users table
- User data stored in localStorage (id, email, created_at)
- Frontend sends user_id with all API requests

### documents table
- Consists of: id, user_id, file_path, original_filename, file_size,
mime_type, title, content, status, embedding, created_at, updated_at
- `embedding` column is type `vector(768)` (pgvector) for semantic search

### Database Relationships
- Users → Documents: One-to-many with CASCADE delete
- Documents have `content` field (TEXT) for storing text
- `updated_at` timestamp auto-updates on record modification

### CORS Configuration
- Configured in `backend/app/main.py`
- Origins read from `.env` file (`CORS_ORIGINS`)
- Allows credentials, all methods, all headers

## Common Gotchas

1. **Backend database auto-creation**: Tables are created automatically on server start. If you change models, restart the server. Existing columns won't be altered - you may need to manually update the database.

2. **Frontend environment variables**: Must be prefixed with `VITE_` to be accessible via `import.meta.env`

3. **User ID in API calls**: Most endpoints require `user_id` parameter. Frontend gets this from UserContext after login.

4. **Python version**: Use `python3` command (not `python`) for virtual environment creation

5. **Status field**: New links are created with status="active" automatically. Don't manually set to "pending".

6. **n8n workflow activation**: The embedding workflow must be **activated** in n8n (toggle switch in top-right). If embeddings aren't being generated, check that the workflow is active and Ollama is running.

7. **Ollama must be running**: Embeddings require Ollama to be running (`ollama serve` or it runs as a service). Test with: `curl http://localhost:11434/api/embeddings -d '{"model": "nomic-embed-text", "prompt": "test"}'`

8. **JobSpy MCP Server must be running**: Job matching requires the MCP server at `http://localhost:9423`. Start with: `cd /home/basil/repos/jobspy-mcp-server && ENABLE_SSE=1 node src/index.js`

9. **Job matching requires resume with embedding**: The `/jobs/match` endpoint requires the user to have uploaded a PDF that has been processed (embedding generated). If embedding is null, job matching will fail.

## Testing Workflow

After making changes:

1. **Backend**: Restart uvicorn server (Ctrl+C then re-run)
2. **Frontend**: Vite hot-reloads automatically
3. **Database schema changes**: Requires server restart + possible manual SQL migration
4. **Test full flow**: Login → View dashboard → Add/edit/delete link → Verify stats

Use Swagger UI (`/docs`) to test backend endpoints independently.
