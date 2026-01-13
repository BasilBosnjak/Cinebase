from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
import httpx
import numpy as np
from ..database import get_db
from ..models import Document

router = APIRouter(prefix="/jobs", tags=["jobs"])

class JobMatchRequest(BaseModel):
    document_id: str
    location: Optional[str] = "Remote"
    results_wanted: Optional[int] = 10
    is_remote: Optional[bool] = True

class JobMatch(BaseModel):
    id: str
    title: str
    company: str
    location: str
    job_url: str
    description: str
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    similarity_score: float

class JobMatchResponse(BaseModel):
    query: str
    total_jobs_fetched: int
    matches: List[JobMatch]

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors"""
    a = np.array(vec1)
    b = np.array(vec2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

async def get_embedding(text: str) -> List[float]:
    """Get embedding from Ollama"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            "http://localhost:11434/api/embeddings",
            json={"model": "nomic-embed-text", "prompt": text[:4000]}
        )
        return response.json()["embedding"]

async def extract_job_keywords_via_rag(document_id: str) -> str:
    """Extract job title/keywords from CV using n8n RAG workflow"""
    query = """Based on this CV/resume, what is the most relevant job title this person should search for?
Return ONLY the job title (2-4 words max), nothing else. For example: "Software Engineer" or "Data Analyst" or "Product Manager"."""

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            "http://localhost:5678/webhook/rag-query",
            json={
                "document_id": document_id,
                "query": query
            }
        )
        result = response.json()

        # Extract the response text from n8n workflow output
        answer = ""
        if isinstance(result, dict):
            answer = result.get("response", result.get("answer", result.get("output", "")))
        elif isinstance(result, str):
            answer = result

        # Clean up the response - take first line, remove quotes
        answer = answer.strip().split('\n')[0].strip('"\'').strip()
        return answer if answer else "software engineer"

@router.post("/match", response_model=JobMatchResponse)
async def match_jobs(request: JobMatchRequest, db: Session = Depends(get_db)):
    """
    Find jobs that match a specific document using semantic similarity.

    1. Fetches the document's content and embedding from the database
    2. Extracts job keywords from CV using LLM
    3. Searches for jobs via JobSpy MCP server
    4. Generates embeddings for each job description
    5. Ranks jobs by cosine similarity to resume
    """

    # Get document with embedding
    result = db.execute(
        text("""
            SELECT id, content, embedding
            FROM documents
            WHERE id = :document_id
            AND embedding IS NOT NULL
        """),
        {"document_id": request.document_id}
    ).fetchone()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Document not found or embedding not yet generated. Please wait for processing to complete."
        )

    # Parse the embedding from pgvector format
    resume_embedding = result.embedding
    if isinstance(resume_embedding, str):
        # Parse string format "[0.1,0.2,...]" to list
        resume_embedding = [float(x) for x in resume_embedding.strip('[]').split(',')]

    # Extract job keywords from CV using RAG workflow
    search_term = await extract_job_keywords_via_rag(request.document_id)

    # Fetch jobs from JobSpy MCP server
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "http://localhost:9423/api",
                json={
                    "searchTerm": search_term,
                    "location": request.location,
                    "resultsWanted": request.results_wanted,
                    "isRemote": request.is_remote
                }
            )
            jobs_data = response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch jobs: {str(e)}")

    if jobs_data.get("count", 0) == 0:
        return JobMatchResponse(
            query=search_term,
            total_jobs_fetched=0,
            matches=[]
        )

    # Generate embeddings for each job and calculate similarity
    matches = []
    for job in jobs_data.get("jobs", []):
        try:
            # Create a combined text from job details for embedding
            job_text = f"{job.get('title', '')} at {job.get('company', '')}. {job.get('description', '')[:2000]}"

            # Get embedding for job
            job_embedding = await get_embedding(job_text)

            # Calculate similarity
            similarity = cosine_similarity(resume_embedding, job_embedding)

            matches.append(JobMatch(
                id=job.get("id", ""),
                title=job.get("title", ""),
                company=job.get("company", ""),
                location=job.get("location", ""),
                job_url=job.get("jobUrl", job.get("jobUrlDirect", "")),
                description=job.get("description", "")[:500] + "...",
                salary_min=job.get("minAmount"),
                salary_max=job.get("maxAmount"),
                similarity_score=round(similarity, 4)
            ))
        except Exception as e:
            # Skip jobs that fail embedding generation
            print(f"Failed to process job {job.get('id')}: {e}")
            continue

    # Sort by similarity score (highest first)
    matches.sort(key=lambda x: x.similarity_score, reverse=True)

    return JobMatchResponse(
        query=search_term,
        total_jobs_fetched=jobs_data.get("count", 0),
        matches=matches
    )

@router.get("/search")
async def search_jobs(
    search_term: str = "software engineer",
    location: str = "Remote",
    results_wanted: int = 10,
    is_remote: bool = True
):
    """
    Search for jobs without matching (direct proxy to JobSpy).
    """
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "http://localhost:9423/api",
                json={
                    "searchTerm": search_term,
                    "location": location,
                    "resultsWanted": results_wanted,
                    "isRemote": is_remote
                }
            )
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job search failed: {str(e)}")
