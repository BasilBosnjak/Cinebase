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

@app.get("/debug/config")
def debug_config():
    """Debug endpoint to verify environment configuration"""
    from .services.ai import COHERE_API_KEY, GROQ_API_KEY, EMBEDDING_MODEL

    return {
        "embedding_provider": "Cohere",
        "embedding_model": EMBEDDING_MODEL,
        "cohere_api_key_set": bool(COHERE_API_KEY),
        "cohere_api_key_preview": f"{COHERE_API_KEY[:8]}...{COHERE_API_KEY[-4:]}" if COHERE_API_KEY else None,
        "groq_api_key_set": bool(GROQ_API_KEY),
        "groq_api_key_preview": f"{GROQ_API_KEY[:8]}...{GROQ_API_KEY[-4:]}" if GROQ_API_KEY else None,
    }

@app.get("/debug/test-embedding")
async def test_embedding():
    """Test endpoint to verify embedding generation works"""
    from .services.ai import get_embedding

    try:
        test_text = "This is a test document for embedding generation."
        embedding = await get_embedding(test_text)

        return {
            "success": True,
            "dimensions": len(embedding),
            "first_5_values": embedding[:5],
            "message": "Embedding generation successful!"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }
