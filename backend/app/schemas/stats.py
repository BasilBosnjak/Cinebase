from pydantic import BaseModel
from typing import Dict

class StatsResponse(BaseModel):
    total_documents: int
    documents_by_status: Dict[str, int]
    recent_documents_count: int
