from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class DocumentBase(BaseModel):
    title: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    content: Optional[str] = None

class DocumentResponse(DocumentBase):
    id: UUID
    user_id: UUID
    file_path: str
    original_filename: str
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    content: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class DocumentUploadResult(BaseModel):
    """Result for a single document upload in batch operation"""
    success: bool
    document: Optional[DocumentResponse] = None
    filename: str
    error: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class BatchUploadResponse(BaseModel):
    """Response for batch document upload"""
    total_files: int
    successful: int
    failed: int
    results: List[DocumentUploadResult]
