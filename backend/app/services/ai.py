"""
AI Service Module - Cloud API integrations for embeddings and LLM.

Uses:
- Hugging Face Inference API for embeddings (Qwen3-Embedding-0.6B)
- Groq for LLM (llama-3.1-8b-instant)

Environment variables required:
- HUGGINGFACE_API_KEY: Hugging Face API token
- GROQ_API_KEY: Groq API key
"""

import httpx
from typing import List
from ..config import settings

HUGGINGFACE_API_KEY = settings.huggingface_api_key or ""
GROQ_API_KEY = settings.groq_api_key or ""

# Embedding model - Qwen3-Embedding-0.6B supports 32-1024 dimensions
# Using 768 to match existing pgvector column
EMBEDDING_MODEL = "Qwen/Qwen3-Embedding-0.6B"
EMBEDDING_DIMENSIONS = 768

# LLM model
LLM_MODEL = "llama-3.1-8b-instant"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


async def get_embedding(text: str) -> List[float]:
    """
    Get embedding vector from Hugging Face Router API.
    Returns 768-dimensional vector (compatible with existing pgvector column).

    Uses the new router.huggingface.co endpoint (api-inference.huggingface.co is deprecated).
    """
    if not HUGGINGFACE_API_KEY:
        raise ValueError("HUGGINGFACE_API_KEY environment variable not set")

    # Correct URL format based on HuggingFace router API
    API_URL = f"https://router.huggingface.co/hf-inference/models/{EMBEDDING_MODEL}/pipeline/feature-extraction"

    print(f"[AI Service] Requesting embedding for text of length: {len(text)} chars")
    print(f"[AI Service] Using model: {EMBEDDING_MODEL}")
    print(f"[AI Service] API URL: {API_URL}")

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": text[:8000]  # Truncate to 8000 chars
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(API_URL, headers=headers, json=payload)

            print(f"[AI Service] Response status: {response.status_code}")

            if response.status_code != 200:
                error_text = response.text
                print(f"[AI Service] Error response: {error_text}")
                raise Exception(f"Embedding API error: {response.status_code} - {error_text}")

            result = response.json()
            print(f"[AI Service] Response type: {type(result)}")

            # Handle nested list response
            embedding = None
            if isinstance(result, list) and len(result) > 0:
                if isinstance(result[0], list):
                    embedding = result[0]  # Nested: [[0.1, 0.2, ...]]
                    print(f"[AI Service] Nested list format, dimensions: {len(embedding)}")
                else:
                    embedding = result  # Flat: [0.1, 0.2, ...]
                    print(f"[AI Service] Flat list format, dimensions: {len(embedding)}")

            if not embedding:
                print(f"[AI Service] Unexpected format - result: {str(result)[:200]}")
                raise Exception(f"Unexpected embedding response format: {type(result)}")

            print(f"[AI Service] Embedding dimensions: {len(embedding)}")

            # Truncate or pad to match expected dimensions (768)
            if len(embedding) > EMBEDDING_DIMENSIONS:
                print(f"[AI Service] Truncating from {len(embedding)} to {EMBEDDING_DIMENSIONS} dimensions")
                return embedding[:EMBEDDING_DIMENSIONS]
            elif len(embedding) < EMBEDDING_DIMENSIONS:
                print(f"[AI Service] Warning: Embedding has only {len(embedding)} dimensions, expected {EMBEDDING_DIMENSIONS}")
                # Pad with zeros if needed
                embedding.extend([0.0] * (EMBEDDING_DIMENSIONS - len(embedding)))
                return embedding

            print(f"[AI Service] Successfully generated embedding with {len(embedding)} dimensions")
            return embedding

    except httpx.TimeoutException as e:
        print(f"[AI Service] Timeout error: {e}")
        raise Exception(f"Embedding API timeout after 60s")
    except httpx.RequestError as e:
        print(f"[AI Service] Request error: {e}")
        raise Exception(f"Embedding API request failed: {str(e)}")
    except Exception as e:
        print(f"[AI Service] Error generating embedding: {type(e).__name__}: {e}")
        raise Exception(f"Embedding generation failed: {str(e)}")


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
