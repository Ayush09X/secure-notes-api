from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Note
from schemas import NoteCreate, NoteUpdate, NoteResponse
from auth_utils import decode_token
from cache import get_cache, set_cache, delete_cache
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {"id": int(payload["sub"]), "username": payload["username"]}

@router.post("/", response_model=NoteResponse)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    new_note = Note(
        title=note.title,
        content=note.content,
        owner_id=current_user["id"]
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    delete_cache(f"notes_list:{current_user['id']}")
    return new_note

@router.get("/", response_model=List[NoteResponse])
def get_notes(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    cache_key = f"notes_list:{current_user['id']}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    notes = db.query(Note).filter(Note.owner_id == current_user["id"]).all()
    notes_data = [NoteResponse.from_orm(n).dict() for n in notes]
    set_cache(cache_key, notes_data, expire=60)
    return notes

@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    cache_key = f"note:{note_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == current_user["id"]).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note_data = NoteResponse.from_orm(note).dict()
    set_cache(cache_key, note_data, expire=120)
    return note

@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note_update: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == current_user["id"]).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note_update.title is not None:
        note.title = note_update.title
    if note_update.content is not None:
        note.content = note_update.content

    db.commit()
    db.refresh(note)
    delete_cache(f"note:{note_id}")
    delete_cache(f"notes_list:{current_user['id']}")
    return note

@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == current_user["id"]).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()
    delete_cache(f"note:{note_id}")
    delete_cache(f"notes_list:{current_user['id']}")
    return {"message": "Note deleted successfully"}
