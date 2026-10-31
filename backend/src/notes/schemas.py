from pydantic import BaseModel, Field, EmailStr
import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import ConfigDict

class Note(BaseModel):
    uid: uuid.UUID
    title: str
    content: str

    summary: str | None = None
    tags: list[str] | None = None
    ai_updated_at: datetime | None = None
    
    is_pinned: bool = Field(default=False)
    is_archived: bool = Field(default=False)

    folder_uid: uuid.UUID | None

    created_at: datetime
    updated_at: datetime

class NoteCreateModel(BaseModel):
    title: str
    content: str
    folder_uid: uuid.UUID | None = None

class NoteUpdateModel(BaseModel):
    title: str | None = None
    content: str | None = None

    folder_uid: uuid.UUID | None = None

    is_pinned: bool | None = None
    is_archived: bool | None = None

class NoteSummary(BaseModel):
    uid: uuid.UUID
    title: str
    is_pinned: bool
    folder_uid: uuid.UUID | None
    updated_at: datetime

class SemanticSearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    limit: int = Field(default=10, ge=1, le=50)
