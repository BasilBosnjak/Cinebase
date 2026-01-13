from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from .config import settings
from .database import engine, Base
from .routers import auth_router, users_router, documents_router, rag_router, jobs_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PDF Manager API", version="1.0.0")

# Create uploads directory on startup
@app.on_event("startup")
async def startup_event():
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

origins = settings.cors_origins.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(documents_router)
app.include_router(rag_router)
app.include_router(jobs_router)

@app.get("/")
def root():
    return {"message": "PDF Manager API", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}
