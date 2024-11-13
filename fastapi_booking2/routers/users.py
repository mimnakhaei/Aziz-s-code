from auth.oauth2 import get_current_user
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from schemas import UserCreate, UserDisplay, UserUpdate
from db.hash import Hash
from db.models import User
from typing import List
from db import db_users
from schemas import UserAuth

router = APIRouter(prefix="/users", tags=["Users"])

# Create user
@router.post("/", response_model=UserDisplay)
def create_user(request: UserCreate, db: Session = Depends(get_db)):
    hashed_password = Hash.bcrypt(request.password)
    new_user = User(username=request.username, email=request.email, password=hashed_password, is_admin=request.is_admin)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get a user
@router.get("/{id}", response_model=UserDisplay)
def get_user(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):

    """_summary_
    Stimulates retrieving a comment of a blog
    
    - **id** Mandatory path parameter
    - **current_user** for authentication check
    """

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
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    currentlyStored = db_users.get_by_id(db, user_id)

    if not currentlyStored:
        raise HTTPException(404, "User not found")
    
    # Check if is_admin status can be changed
    if(currentlyStored.is_admin != user.is_admin):
        if not current_user.is_admin:
            raise HTTPException(403, "You're not an admin so you are not allowed to change the is_admin status")
        if not user.is_admin and db_users.get_admin_count() < 2:
            raise HTTPException(409, "You're the only admin so you cannot revoke your own admin status")
        
     # Ensure that only the user themselves or an admin can update
    # if user_id is not currentlyStored.user_id or not current_user.is_admin:
    #     raise HTTPException(403, 'Not allowed')
    
    # return db_users.update_user(db, user_id, user)
    if user_id != currentlyStored.id and not current_user.is_admin:
        raise HTTPException(403, 'Not allowed')
    
    return db_users.update_user(db, user_id, user)
    

# Delete user
@router.delete("/{user_id}")
def delete_hotel(user_id: int, db: Session = Depends(get_db)):
    db_users.delete_user(db, user_id)
    return {"detail": "User deleted successfully"}