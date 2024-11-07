from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import models, database
from schemas import UserCreate, UserDisplay
from db.hash import Hash
from db.models import User
#from auth.oauth2 import get_current_user
from typing import List
from db import db_users

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserDisplay)
def create_user(request: UserCreate, db: Session = Depends(database.get_db)):
    hashed_password = Hash.bcrypt(request.password)
    new_user = User(username=request.username, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=UserDisplay)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
