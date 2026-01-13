from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx

router = APIRouter(prefix="/rag", tags=["rag"])

class RAGQueryRequest(BaseModel):
    user_id: str
    query: str

@router.post("/query")
async def query_rag(request: RAGQueryRequest):
    """Forward RAG query to n8n workflow"""
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "http://localhost:5678/webhook/rag-query",
                json={"user_id": request.user_id, "query": request.query}
            )
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG query failed: {str(e)}")
