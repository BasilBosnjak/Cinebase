from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
import cohere

from ..database import get_db
from ..services.ai import COHERE_API_KEY, GROQ_API_KEY, GROQ_URL
import httpx

router = APIRouter(prefix="/rag", tags=["rag"])

class RAGQueryRequest(BaseModel):
    user_id: str
    query: str
    document_id: Optional[str] = None  # Optional: query specific document
    top_k: int = 5  # Number of documents to retrieve

class DocumentSource(BaseModel):
    filename: str
    similarity: str

class RAGQueryResponse(BaseModel):
    answer: str
    query: str
    sources: List[DocumentSource]
    tokens_used: int

@router.post("/query", response_model=RAGQueryResponse)
async def query_rag(request: RAGQueryRequest, db: Session = Depends(get_db)):
    """
    Query RAG system using semantic search + LLM generation.

    Flow:
    1. Generate query embedding (Cohere)
    2. Similarity search in PostgreSQL (pgvector)
    3. Build context from retrieved documents
    4. Generate answer using LLM (Groq)
    """
    try:
        print(f"[RAG] Processing query: '{request.query}' for user: {request.user_id}")

        # Step 1: Generate query embedding
        if not COHERE_API_KEY:
            raise HTTPException(status_code=500, detail="COHERE_API_KEY not configured")

        print(f"[RAG] Generating query embedding...")
        co = cohere.Client(api_key=COHERE_API_KEY)
        embed_response = co.embed(
            texts=[request.query],
            model="embed-english-v3.0",
            input_type="search_query",  # Important: use search_query for queries
            embedding_types=["float"]
        )
        query_embedding = embed_response.embeddings.float[0][:768]  # Truncate to 768
        print(f"[RAG] Query embedding generated: {len(query_embedding)} dimensions")

        # Format embedding as PostgreSQL vector string
        embedding_str = "[" + ",".join(str(x) for x in query_embedding) + "]"

        # Step 2: Similarity search
        print(f"[RAG] Searching for similar documents...")

        # Build SQL query with optional document_id filter
        if request.document_id:
            sql_query = text("""
                SELECT
                    id,
                    user_id,
                    content,
                    original_filename,
                    1 - (embedding <=> CAST(:embedding AS vector)) as similarity_score
                FROM documents
                WHERE id = CAST(:document_id AS uuid)
                    AND content IS NOT NULL
                    AND embedding IS NOT NULL
                ORDER BY embedding <=> CAST(:embedding AS vector)
                LIMIT :top_k
            """)
            result = db.execute(
                sql_query,
                {
                    "embedding": embedding_str,
                    "document_id": request.document_id,
                    "top_k": request.top_k
                }
            )
        else:
            sql_query = text("""
                SELECT
                    id,
                    user_id,
                    content,
                    original_filename,
                    1 - (embedding <=> CAST(:embedding AS vector)) as similarity_score
                FROM documents
                WHERE user_id = CAST(:user_id AS uuid)
                    AND content IS NOT NULL
                    AND embedding IS NOT NULL
                ORDER BY embedding <=> CAST(:embedding AS vector)
                LIMIT :top_k
            """)
            result = db.execute(
                sql_query,
                {
                    "embedding": embedding_str,
                    "user_id": request.user_id,
                    "top_k": request.top_k
                }
            )

        documents = result.fetchall()

        if not documents:
            raise HTTPException(
                status_code=404,
                detail="No documents found. Please upload a document first."
            )

        print(f"[RAG] Found {len(documents)} relevant documents")

        # Step 3: Build context from retrieved documents
        context_parts = []
        sources = []

        for doc in documents:
            similarity_pct = f"{doc.similarity_score * 100:.1f}%"
            context_parts.append(
                f"[{similarity_pct} relevant] Document: {doc.original_filename}\n"
                f"Content: {doc.content[:1500]}"  # Limit content per doc
            )
            sources.append(DocumentSource(
                filename=doc.original_filename,
                similarity=similarity_pct
            ))

        context = "\n\n---\n\n".join(context_parts)
        print(f"[RAG] Built context from {len(documents)} documents, total length: {len(context)} chars")

        # Step 4: Generate answer using Groq
        if not GROQ_API_KEY:
            raise HTTPException(status_code=500, detail="GROQ_API_KEY not configured")

        print(f"[RAG] Generating answer with Groq...")

        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions based on provided documents. "
                          "Only use information from the documents provided. "
                          "If the answer is not in the documents, say so clearly. "
                          "Be concise but thorough."
            },
            {
                "role": "user",
                "content": f"Documents:\n{context[:6000]}\n\nQuestion: {request.query}\n\nAnswer:"
            }
        ]

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                GROQ_URL,
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": messages,
                    "temperature": 0.3,
                    "max_tokens": 1000
                }
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=500,
                    detail=f"Groq API error: {response.status_code} - {response.text}"
                )

            result = response.json()
            answer = result["choices"][0]["message"]["content"].strip()
            tokens_used = result["usage"]["total_tokens"]

        print(f"[RAG] Answer generated successfully, tokens used: {tokens_used}")

        return RAGQueryResponse(
            answer=answer,
            query=request.query,
            sources=sources,
            tokens_used=tokens_used
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"[RAG] Error: {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=f"RAG query failed: {str(e)}")
