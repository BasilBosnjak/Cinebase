from pydantic import BaseModel, HttpUrl
from datetime import datetime
from uuid import UUID
from typing import Optional

class LinkBase(BaseModel):
    url: str
    title: Optional[str] = None

class LinkCreate(LinkBase):
    pass

class LinkUpdate(BaseModel):
    url: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None

class LinkResponse(LinkBase):
    id: UUID
    user_id: UUID
    content: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
