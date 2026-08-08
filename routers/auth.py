from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserLogin
from auth_utils import hash_password, verify_password, create_access_token
from cache import get_cache, set_cache

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    cached = get_cache(f"user_exists:{user.username}")
    if cached:
        raise HTTPException(status_code=400, detail="Username already registered")

    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        set_cache(f"user_exists:{user.username}", True, expire=300)
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = User(
        username=user.username,
        password_hash=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "user_id": new_user.id}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"sub": str(db_user.id), "username": db_user.username})
    return {"access_token": token, "token_type": "bearer"}
