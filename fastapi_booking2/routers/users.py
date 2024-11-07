from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from schemas import UserCreate, UserDisplay
from db.hash import Hash
from db.models import User
#from auth.oauth2 import get_current_user
from typing import List
from db import db_users

router = APIRouter(prefix="/users", tags=["Users"])

# Create user
@router.post("/", response_model=UserDisplay)
def create_user(request: UserCreate, db: Session = Depends(get_db)):
    hashed_password = Hash.bcrypt(request.password)
    new_user = User(username=request.username, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get a user
@router.get("/{id}", response_model=UserDisplay)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Get all users
@router.get("/", response_model=List[UserDisplay])
def get_all_users(db: Session = Depends(get_db)):
    return db_users.get_all_users(db)

# Update user
@router.put("/{user_id}", response_model=UserDisplay)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    return db_users.update_user(db, user_id, user)
    #return {"detail": "User updated successfully"}

# Delete user
@router.delete("/{user_id}")
def delete_hotel(user_id: int, db: Session = Depends(get_db)):
    db_users.delete_user(db, user_id)
    return {"detail": "User deleted successfully"}