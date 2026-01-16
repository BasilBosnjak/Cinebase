# Deploy n8n on Render - Quick Guide

## Step 1: Commit n8n Files (2 minutes)

```bash
cd /home/basil/repos/Cinebase
git add n8n/
git commit -m "Add n8n for Render deployment"
git push origin main
```

## Step 2: Create n8n Service on Render (3 minutes)

1. Go to https://dashboard.render.com
2. Click **New +** → **Web Service**
3. Connect your GitHub repository: `Cinebase`
4. Configure:
   - **Name:** `cinebase-n8n`
   - **Region:** Oregon (same as backend)
   - **Branch:** `main`
   - **Root Directory:** `n8n`
   - **Runtime:** Docker
   - **Instance Type:** Free (or Starter $7/month for better performance)

5. **Environment Variables** (click "Advanced"):
   ```
   N8N_BASIC_AUTH_ACTIVE=true
   N8N_BASIC_AUTH_USER=admin
   N8N_BASIC_AUTH_PASSWORD=<strong-password>
   N8N_ENCRYPTION_KEY=<generate-random-32-chars>
   N8N_HOST=0.0.0.0
   N8N_PORT=5678
   N8N_PROTOCOL=https
   WEBHOOK_URL=https://cinebase-n8n.onrender.com
   GENERIC_TIMEZONE=America/New_York
   DB_TYPE=sqlite
   ```

6. Click **Create Web Service**

## Step 3: Wait for Deployment (3-5 minutes)

- Watch the logs for: `Editor is now accessible via: https://cinebase-n8n.onrender.com`
- First deployment takes ~5 minutes

## Step 4: Access n8n UI

1. Open: `https://cinebase-n8n.onrender.com`
2. Login with credentials from environment variables
3. You should see the n8n editor

## Step 5: Import Cloud-Ready Workflow (5 minutes)

### A. Add Credentials

**Cohere API:**
1. Settings → Credentials → Add Credential
2. Search "HTTP Header Auth"
3. Name: `Cohere API`
4. Header Name: `Authorization`
5. Header Value: `Bearer YOUR_COHERE_API_KEY`
6. Save

**Groq API:**
1. Add another "HTTP Header Auth"
2. Name: `Groq API`
3. Header Name: `Authorization`
4. Header Value: `Bearer YOUR_GROQ_API_KEY`
5. Save

**PostgreSQL:**
1. Add "Postgres" credential
2. Fill Render PostgreSQL details:
   - Host: `<from-render-dashboard>.oregon-postgres.render.com`
   - Database: `cinebase`
   - User: `<from-render>`
   - Password: `<from-render>`
   - Port: `5432`
   - SSL: `true`
3. Test connection
4. Save as `Render PostgreSQL`

### B. Import Workflow

1. Workflows → Add Workflow → Import from File
2. Upload: `/home/basil/repos/Cinebase/n8n-rag-workflow-cloud-ready.json`
3. Click each node and select correct credential:
   - "Generate Query Embedding" → Cohere API
   - "Similarity Search" → Render PostgreSQL
   - "Generate Answer with Groq" → Groq API
4. Save workflow
5. **Activate** (toggle in top right)

## Step 6: Get Webhook URL

1. Click the "Webhook" node
2. Copy the **Production URL**
3. Format: `https://cinebase-n8n.onrender.com/webhook/rag-query-cloud`

## Step 7: Update FastAPI Backend (3 minutes)

Edit `backend/app/routers/rag.py`:

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import os

router = APIRouter(prefix="/rag", tags=["rag"])

class RAGQueryRequest(BaseModel):
    user_id: str
    query: str
    document_id: str = None

@router.post("/query")
async def query_rag(request: RAGQueryRequest):
    """Query RAG system via n8n workflow"""
    n8n_webhook_url = os.getenv(
        "N8N_WEBHOOK_URL",
        "https://cinebase-n8n.onrender.com/webhook/rag-query-cloud"
    )

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                n8n_webhook_url,
                json={
                    "user_id": request.user_id,
                    "query": request.query,
                    "document_id": request.document_id
                }
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG query failed: {str(e)}")
```

Commit and push:
```bash
git add backend/app/routers/rag.py
git commit -m "Connect RAG endpoint to n8n workflow"
git push origin main
```

Add environment variable on Render backend:
- Key: `N8N_WEBHOOK_URL`
- Value: `https://cinebase-n8n.onrender.com/webhook/rag-query-cloud`

## Step 8: Test End-to-End

```bash
# Test RAG via backend
curl -X POST https://cinebase-backend.onrender.com/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "YOUR_USER_UUID",
    "query": "What is this document about?"
  }'
```

Expected response:
```json
{
  "answer": "Based on the documents provided...",
  "query": "What is this document about?",
  "sources": [
    {"filename": "resume.pdf", "similarity": "91.2%"}
  ],
  "tokens_used": 234
}
```

## Troubleshooting

**n8n not starting:**
- Check Render logs for errors
- Verify environment variables are set
- Ensure port 5678 is exposed

**"Authentication failed":**
- Verify credentials have correct API keys
- Check Bearer prefix is included

**"Database connection failed":**
- Verify PostgreSQL SSL is enabled
- Check connection string format
- Test connection in n8n credential settings

**Render free tier limitations:**
- Sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds
- Consider Starter plan ($7/month) for always-on

## Cost Summary

- **n8n on Render Free:** $0 (sleeps after 15 min)
- **n8n on Render Starter:** $7/month (always-on)
- **Cohere API:** Free tier (1000 calls/month)
- **Groq API:** Free tier (rate-limited)
- **PostgreSQL:** $7/month (already have)

**Total: $0-7/month** (vs $20/month for n8n Cloud)
