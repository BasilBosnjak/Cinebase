# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Link Manager is a full-stack application for storing and managing links with email-only authentication. The project is structured for future RAG (Retrieval-Augmented Generation) integration, storing link content in the database for processing.

**Tech Stack:**
- Backend: FastAPI + SQLAlchemy + PostgreSQL
- Frontend: React + Vite + Tailwind CSS
- State Management: React Context API
- Database: PostgreSQL with UUID primary keys

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

## Important Implementation Details

### Authentication
- **Email-only authentication** - no passwords or OAuth
- Login endpoint checks if email exists in users table
- User data stored in localStorage (id, email, created_at)
- Frontend sends user_id with all API requests

### Link Status System
- Status field exists for future RAG processing
- Default status: `"active"` (not "pending")
- Status can be updated via PUT `/links/{link_id}` endpoint
- Frontend displays all statuses with green badge

### Database Relationships
- Users → Links: One-to-many with CASCADE delete
- Links have `content` field (TEXT) for storing webpage text
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

## Testing Workflow

After making changes:

1. **Backend**: Restart uvicorn server (Ctrl+C then re-run)
2. **Frontend**: Vite hot-reloads automatically
3. **Database schema changes**: Requires server restart + possible manual SQL migration
4. **Test full flow**: Login → View dashboard → Add/edit/delete link → Verify stats

Use Swagger UI (`/docs`) to test backend endpoints independently.
