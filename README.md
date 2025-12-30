# PDF Manager Application

A full-stack PDF document management application with email-only authentication. Users can upload, manage, and track PDF files with automatic text extraction for future RAG integration.

## Tech Stack

- **Backend**: Python with FastAPI
- **Frontend**: React with Vite
- **Database**: PostgreSQL
- **Styling**: Tailwind CSS

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
| status | VARCHAR(50) | NOT NULL, DEFAULT 'pending' |
| created_at | TIMESTAMP | NOT NULL |
| updated_at | TIMESTAMP | NOT NULL |

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 14+

### 1. Database Setup

```bash
# Create database
createdb linkmanager

# Or using psql
psql -U postgres
CREATE DATABASE linkmanager;
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

# Update .env with your database credentials
# DATABASE_URL=postgresql://user:password@localhost:5432/linkmanager
# CORS_ORIGINS=http://localhost:5173,http://localhost:3000

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
6. Click "Upload PDF" - the file will be uploaded, text extracted, and appear in the list
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
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | Email lookup - returns user data if exists |
| GET | `/users/{user_id}/documents` | Get all PDF documents for user |
| POST | `/users/{user_id}/documents` | Upload new PDF (multipart/form-data, extracts text) |
| PUT | `/documents/{document_id}` | Update document (title, status) |
| DELETE | `/documents/{document_id}` | Delete document (DB + file) |
| GET | `/documents/{document_id}/download` | Download PDF file |
| GET | `/documents/{document_id}/view` | View PDF inline |
| GET | `/users/{user_id}/stats` | Get dashboard stats |

## Features

- Email-only authentication (no passwords)
- PDF file upload and storage (local filesystem)
- Automatic PDF text extraction (using pypdf)
- Document management (upload, view, download, delete)
- Status tracking (pending, processing, processed, failed)
- Dashboard with statistics
- Responsive design
- File size validation (10MB max)
- Secure file storage with UUID-based filenames
- Extracted text storage for future RAG integration

## Development Notes

- Backend uses SQLAlchemy ORM with PostgreSQL
- Frontend uses React Context for state management
- All API calls centralized in `frontend/src/services/api.js`
- CORS configured for local development
- Database tables created automatically on backend startup
