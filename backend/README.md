# Link Manager Backend

FastAPI backend for the Link Manager application.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL database:
```bash
createdb linkmanager
```

4. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

5. Update `.env` with your database credentials:
```
DATABASE_URL=postgresql://user:password@localhost:5432/linkmanager
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

6. Run the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## API Endpoints

- `POST /auth/login` - Email lookup
- `GET /users/{user_id}/links` - Get all links for user
- `POST /users/{user_id}/links` - Create new link
- `PUT /links/{link_id}` - Update link
- `DELETE /links/{link_id}` - Delete link
- `GET /users/{user_id}/stats` - Get dashboard stats

## Database Models

- **users**: id, email, created_at
- **links**: id, user_id, url, title, content, status, created_at, updated_at
