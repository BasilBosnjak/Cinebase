# Link Manager Frontend

React frontend for the Link Manager application.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

3. Update `.env` with your backend URL:
```
VITE_API_URL=http://localhost:8000
```

4. Run the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Features

- Email-only authentication
- Dashboard with link statistics
- Add, edit, and delete links
- Responsive design with Tailwind CSS
- Centralized API service
- Protected routes with React Router

## Tech Stack

- React 18
- Vite
- React Router DOM
- Tailwind CSS
- Context API for state management
