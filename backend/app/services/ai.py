"""
AI Service Module - Cloud API integrations for embeddings and LLM.

Uses:
- Cohere API for embeddings (embed-english-v3.0)
- Groq for LLM (llama-3.1-8b-instant)

Environment variables required:
- COHERE_API_KEY: Cohere API token
- GROQ_API_KEY: Groq API key
"""

import httpx
import cohere
from typing import List
from ..config import settings

COHERE_API_KEY = settings.cohere_api_key or ""
GROQ_API_KEY = settings.groq_api_key or ""

# Embedding model - Cohere embed-english-v3.0 (1024 dimensions, truncated to 768)
EMBEDDING_MODEL = "embed-english-v3.0"
EMBEDDING_DIMENSIONS = 768

# LLM model
LLM_MODEL = "llama-3.1-8b-instant"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


async def get_embedding(text: str) -> List[float]:
    """
    Get embedding vector from Cohere API.
    Returns 768-dimensional vector (compatible with existing pgvector column).

    Uses Cohere embed-english-v3.0 (1024 dims) and truncates to 768.
    """
    if not COHERE_API_KEY:
        raise ValueError("COHERE_API_KEY environment variable not set")

    print(f"[AI Service] Requesting embedding for text of length: {len(text)} chars")
    print(f"[AI Service] Using Cohere model: {EMBEDDING_MODEL}")

    try:
        # Initialize Cohere client
        co = cohere.Client(api_key=COHERE_API_KEY)

        # Get embedding
        # Cohere's embed method returns embeddings for a list of texts
        response = co.embed(
            texts=[text[:8000]],  # Truncate to 8000 chars
            model=EMBEDDING_MODEL,
            input_type="search_document",  # For document embeddings (vs "search_query")
            embedding_types=["float"]
        )

        # Extract the embedding from the response
        embedding = response.embeddings.float[0]  # Get first (and only) embedding

        print(f"[AI Service] Cohere returned embedding with {len(embedding)} dimensions")

        # Truncate to 768 dimensions (Cohere returns 1024)
        if len(embedding) > EMBEDDING_DIMENSIONS:
            print(f"[AI Service] Truncating from {len(embedding)} to {EMBEDDING_DIMENSIONS} dimensions")
            embedding = embedding[:EMBEDDING_DIMENSIONS]
        elif len(embedding) < EMBEDDING_DIMENSIONS:
            print(f"[AI Service] Warning: Embedding has only {len(embedding)} dimensions, expected {EMBEDDING_DIMENSIONS}")
            # Pad with zeros if needed
            embedding.extend([0.0] * (EMBEDDING_DIMENSIONS - len(embedding)))

        print(f"[AI Service] Successfully generated {len(embedding)}-dimensional embedding")
        return embedding

    except Exception as e:
        print(f"[AI Service] Error generating embedding: {type(e).__name__}: {e}")
        raise Exception(f"Cohere embedding generation failed: {str(e)}")


async def generate_text(prompt: str, max_tokens: int = 100, temperature: float = 0.1) -> str:
    """
    Generate text using Groq LLM API.
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY environment variable not set")

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": LLM_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temperature
            }
        )

        if response.status_code != 200:
            raise Exception(f"Groq API error: {response.status_code} - {response.text}")

        result = response.json()
        return result["choices"][0]["message"]["content"].strip()


async def extract_job_title(cv_content: str) -> str:
    """
    Extract the most relevant job title from CV content using LLM.
    """
    prompt = f"""Based on this CV/resume content, what is the most relevant job title this person should search for?
Return ONLY the job title (2-4 words max), nothing else. For example: "Software Engineer" or "Data Analyst" or "Product Manager" or "Marketing Specialist".

CV Content:
{cv_content[:3000]}

Job title:"""

    try:
        answer = await generate_text(prompt, max_tokens=20, temperature=0.1)

        # Clean up response
        answer = answer.split('\n')[0].strip('"\'').strip()

        # Remove common prefixes
        if answer.lower().startswith(("based on", "the ", "a ")):
            parts = answer.split(":")
            if len(parts) > 1:
                answer = parts[-1].strip()

        print(f"[AI Service] Extracted job title: '{answer}'")
        return answer if answer and len(answer) < 50 else "general"

    except Exception as e:
        print(f"[AI Service] Failed to extract job title: {e}")
        return "general"
