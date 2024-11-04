# db/db_users.py
from sqlalchemy.orm import Session
from db import models
from schemas import UserCreate, UserDisplay
from db.hash import Hash

def create_user(db: Session, user: UserCreate):
     
    #db_user = models.User(username=user.username, email=user.email, hashed_password=user.password)
    hashed_password = Hash.bcrypt(user.password)  # Hashing the password
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> UserDisplay:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> UserDisplay:
    return db.query(models.User).filter(models.User.username == username).first()

def get_all_users(db: Session):
    return db.query(models.User).all()

def update_user(db: Session, user_id: int, user: UserCreate):
    db_user = get_user(db, user_id)
    if db_user:
        db_user.username = user.username
        db_user.email = user.email
        db_user.hashed_password = user.password  # Ideally, hash the password before saving
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()

# Additional utility functions can be added as needed
