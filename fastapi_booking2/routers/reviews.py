from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import db_reviews
from db.database import get_db
from schemas import ReviewCreate, ReviewDisplay, ReviewUpdate
from typing import List
from auth.oauth2 import get_current_user
from schemas import UserAuth

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)

@router.post("/", response_model=ReviewDisplay)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    return db_reviews.create_review(db, review)

@router.get("/{review_id}", response_model=ReviewDisplay)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db_reviews.get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return review

@router.get("/", response_model=List[ReviewDisplay])
def get_all_reviews(db: Session = Depends(get_db)):
    return db_reviews.get_all_reviews(db)

@router.put("/{review_id}", response_model=ReviewDisplay)
def update_review(review_id: int, review: ReviewUpdate, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    updated_review = db_reviews.update_review(db, review_id, review)
    if not updated_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return updated_review 

@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    delete_review = db_reviews.delete_review(db, review_id)
    return {"detail": "Review deleted successfully"}

