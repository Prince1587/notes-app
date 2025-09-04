from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class NoteCreate(BaseModel):
    title: str = Field(default="Untitled", max_length=200)
    content: str = ""

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=200)
    content: Optional[str] = None

class NoteOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    share_url: Optional[str] = None

    class Config:
        from_attributes = True

class PublicNoteOut(BaseModel):
    title: str
    content: str
    created_at: datetime
    updated_at: datetime