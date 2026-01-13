from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
import asyncio
from concurrent.futures import ThreadPoolExecutor
from ..database import get_db
from ..services.ai import get_embedding, extract_job_title

router = APIRouter(prefix="/jobs", tags=["jobs"])

# Thread pool for running sync JobSpy in async context
executor = ThreadPoolExecutor(max_workers=2)


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


class UserDigest(BaseModel):
    user_id: str
    email: str
    document_name: str
    search_term: str
    top_matches: List[JobMatch]


class WeeklyDigestResponse(BaseModel):
    total_users: int
    digests: List[UserDigest]


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors"""
    a = np.array(vec1)
    b = np.array(vec2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def search_jobs_sync(
    search_term: str,
    location: str = "Remote",
    results_wanted: int = 10,
    is_remote: bool = True
) -> List[dict]:
    """
    Search for jobs using JobSpy library (synchronous).
    Returns list of job dictionaries.
    """
    try:
        from jobspy import scrape_jobs
        import pandas as pd

        jobs_df = scrape_jobs(
            site_name=["indeed", "linkedin", "glassdoor"],
            search_term=search_term,
            location=location,
            results_wanted=results_wanted,
            is_remote=is_remote,
            country_indeed="USA"
        )

        if jobs_df is None or jobs_df.empty:
            return []

        # Convert DataFrame to list of dicts
        jobs = []
        for idx, row in jobs_df.iterrows():
            jobs.append({
                "id": str(row.get("id", idx)),
                "title": str(row.get("title", "")),
                "company": str(row.get("company", "")),
                "location": str(row.get("location", "")),
                "job_url": str(row.get("job_url", "")),
                "description": str(row.get("description", ""))[:2000],
                "min_amount": row.get("min_amount") if pd.notna(row.get("min_amount")) else None,
                "max_amount": row.get("max_amount") if pd.notna(row.get("max_amount")) else None,
            })

        return jobs

    except Exception as e:
        print(f"[JobSpy] Error searching jobs: {e}")
        return []


async def search_jobs_async(
    search_term: str,
    location: str = "Remote",
    results_wanted: int = 10,
    is_remote: bool = True
) -> List[dict]:
    """Async wrapper for JobSpy search"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        executor,
        search_jobs_sync,
        search_term,
        location,
        results_wanted,
        is_remote
    )


async def process_jobs_with_embeddings(
    jobs: List[dict],
    resume_embedding: List[float]
) -> List[JobMatch]:
    """Generate embeddings for jobs and calculate similarity scores"""
    matches = []

    for job in jobs:
        try:
            # Create combined text for embedding
            job_text = f"{job['title']} at {job['company']}. {job['description']}"

            # Get embedding from cloud API
            job_embedding = await get_embedding(job_text)

            # Calculate similarity
            similarity = cosine_similarity(resume_embedding, job_embedding)

            matches.append(JobMatch(
                id=job["id"],
                title=job["title"],
                company=job["company"],
                location=job["location"],
                job_url=job["job_url"],
                description=job["description"][:500] + "..." if len(job["description"]) > 500 else job["description"],
                salary_min=job.get("min_amount"),
                salary_max=job.get("max_amount"),
                similarity_score=round(similarity, 4)
            ))

        except Exception as e:
            print(f"[Jobs] Failed to process job {job.get('id')}: {e}")
            continue

    # Sort by similarity score (highest first)
    matches.sort(key=lambda x: x.similarity_score, reverse=True)
    return matches


@router.post("/match", response_model=JobMatchResponse)
async def match_jobs(request: JobMatchRequest, db: Session = Depends(get_db)):
    """
    Find jobs that match a specific document using semantic similarity.

    1. Fetches the document's content and embedding from the database
    2. Extracts job keywords from CV using LLM (Groq)
    3. Searches for jobs via JobSpy library
    4. Generates embeddings for each job (Hugging Face)
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
        resume_embedding = [float(x) for x in resume_embedding.strip('[]').split(',')]

    # Extract job keywords from CV content using cloud LLM
    search_term = await extract_job_title(result.content or "")

    # Search for jobs using JobSpy
    jobs = await search_jobs_async(
        search_term=search_term,
        location=request.location or "Remote",
        results_wanted=request.results_wanted or 10,
        is_remote=request.is_remote if request.is_remote is not None else True
    )

    if not jobs:
        return JobMatchResponse(
            query=search_term,
            total_jobs_fetched=0,
            matches=[]
        )

    # Process jobs with embeddings
    matches = await process_jobs_with_embeddings(jobs, resume_embedding)

    return JobMatchResponse(
        query=search_term,
        total_jobs_fetched=len(jobs),
        matches=matches
    )


@router.get("/weekly-digest", response_model=WeeklyDigestResponse)
async def get_weekly_digest(
    top_n: int = 5,
    location: str = "Remote",
    is_remote: bool = True,
    db: Session = Depends(get_db)
):
    """
    Generate weekly job digest for all users with CVs.
    Called by n8n workflow to send weekly emails.

    Returns top job matches for each user's most recent document.
    """

    # Get all users with documents that have embeddings
    users_with_docs = db.execute(
        text("""
            SELECT DISTINCT ON (u.id)
                u.id as user_id,
                u.email,
                d.id as document_id,
                d.original_filename,
                d.content,
                d.embedding
            FROM users u
            JOIN documents d ON d.user_id = u.id
            WHERE d.embedding IS NOT NULL
            ORDER BY u.id, d.created_at DESC
        """)
    ).fetchall()

    if not users_with_docs:
        return WeeklyDigestResponse(total_users=0, digests=[])

    digests = []

    for row in users_with_docs:
        try:
            # Parse embedding
            resume_embedding = row.embedding
            if isinstance(resume_embedding, str):
                resume_embedding = [float(x) for x in resume_embedding.strip('[]').split(',')]

            # Extract job keywords from CV
            search_term = await extract_job_title(row.content or "")

            # Search for jobs
            jobs = await search_jobs_async(
                search_term=search_term,
                location=location,
                results_wanted=15,
                is_remote=is_remote
            )

            if not jobs:
                continue

            # Process jobs with embeddings
            matches = await process_jobs_with_embeddings(jobs, resume_embedding)
            top_matches = matches[:top_n]

            if top_matches:
                digests.append(UserDigest(
                    user_id=str(row.user_id),
                    email=row.email,
                    document_name=row.original_filename,
                    search_term=search_term,
                    top_matches=top_matches
                ))

            print(f"[WeeklyDigest] Processed user {row.email}: {len(top_matches)} matches for '{search_term}'")

        except Exception as e:
            print(f"[WeeklyDigest] Error processing user {row.email}: {e}")
            continue

    return WeeklyDigestResponse(
        total_users=len(digests),
        digests=digests
    )


@router.get("/search")
async def search_jobs(
    search_term: str = "software engineer",
    location: str = "Remote",
    results_wanted: int = 10,
    is_remote: bool = True
):
    """
    Search for jobs without matching (direct JobSpy search).
    """
    try:
        jobs = await search_jobs_async(
            search_term=search_term,
            location=location,
            results_wanted=results_wanted,
            is_remote=is_remote
        )

        return {
            "count": len(jobs),
            "jobs": jobs
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job search failed: {str(e)}")
