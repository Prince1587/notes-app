import os, secrets
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select
from .db import Base, engine, SessionLocal
from .models import Note
from .schemas import NoteCreate, NoteUpdate, NoteOut, PublicNoteOut

app = FastAPI(title="Notes API", version="1.0.0")

# CORS
allowed = os.getenv("ALLOWED_ORIGINS", "*")
origins = [o.strip() for o in allowed.split(",")] if allowed else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB init
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["health"])
def root():
    return {"ok": True, "service": "Notes API"}

@app.get("/health", tags=["health"])
def health():
    return {"status": "healthy"}

def build_share_url(request: Request, share_id: Optional[str]) -> Optional[str]:
    if not share_id:
        return None
    base = os.getenv("BASE_URL")
    if not base:
        base = str(request.base_url).rstrip("/")
    return f"{base}/share/{share_id}"

@app.get("/notes", response_model=List[NoteOut], tags=["notes"])
def list_notes(request: Request, db: Session = Depends(get_db)):
    notes = db.scalars(select(Note).order_by(Note.updated_at.desc())).all()
    out: List[NoteOut] = []
    for n in notes:
        out.append(NoteOut(
            id=n.id, title=n.title, content=n.content,
            created_at=n.created_at, updated_at=n.updated_at,
            share_url=build_share_url(request, n.share_id)
        ))
    return out

@app.post("/notes", response_model=NoteOut, tags=["notes"])
def create_note(payload: NoteCreate, request: Request, db: Session = Depends(get_db)):
    n = Note(title=payload.title, content=payload.content)
    db.add(n)
    db.commit()
    db.refresh(n)
    return NoteOut(
        id=n.id, title=n.title, content=n.content,
        created_at=n.created_at, updated_at=n.updated_at,
        share_url=build_share_url(request, n.share_id)
    )

@app.get("/notes/{note_id}", response_model=NoteOut, tags=["notes"])
def get_note(note_id: int, request: Request, db: Session = Depends(get_db)):
    n = db.get(Note, note_id)
    if not n:
        raise HTTPException(404, "Note not found")
    return NoteOut(
        id=n.id, title=n.title, content=n.content,
        created_at=n.created_at, updated_at=n.updated_at,
        share_url=build_share_url(request, n.share_id)
    )

@app.put("/notes/{note_id}", response_model=NoteOut, tags=["notes"])
def update_note(note_id: int, payload: NoteUpdate, request: Request, db: Session = Depends(get_db)):
    n = db.get(Note, note_id)
    if not n:
        raise HTTPException(404, "Note not found")
    if payload.title is not None:
        n.title = payload.title
    if payload.content is not None:
        n.content = payload.content
    n.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(n)
    return NoteOut(
        id=n.id, title=n.title, content=n.content,
        created_at=n.created_at, updated_at=n.updated_at,
        share_url=build_share_url(request, n.share_id)
    )

@app.delete("/notes/{note_id}", tags=["notes"])
def delete_note(note_id: int, db: Session = Depends(get_db)):
    n = db.get(Note, note_id)
    if not n:
        raise HTTPException(404, "Note not found")
    db.delete(n)
    db.commit()
    return {"deleted": True}

@app.post("/notes/{note_id}/share", response_model=NoteOut, tags=["share"])
def create_or_get_share_link(note_id: int, request: Request, db: Session = Depends(get_db)):
    n = db.get(Note, note_id)
    if not n:
        raise HTTPException(404, "Note not found")
    if not n.share_id:
        n.share_id = secrets.token_hex(8)  # 16-char slug
        n.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(n)
    return NoteOut(
        id=n.id, title=n.title, content=n.content,
        created_at=n.created_at, updated_at=n.updated_at,
        share_url=build_share_url(request, n.share_id)
    )

@app.get("/share/{share_id}", response_model=PublicNoteOut, tags=["share"])
def get_shared_note(share_id: str, db: Session = Depends(get_db)):
    stmt = select(Note).where(Note.share_id == share_id)
    n = db.scalars(stmt).first()
    if not n:
        raise HTTPException(404, "Shared link not found")
    return PublicNoteOut(
        title=n.title, content=n.content,
        created_at=n.created_at, updated_at=n.updated_at
    )

