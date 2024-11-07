from sqlalchemy.orm import Session
from db import models
from schemas import ReviewCreate
from datetime import datetime

def create_review(db: Session, review: ReviewCreate):
    db_review = models.Review(content=review.content, review_time=review.review_time or datetime.utcnow(), user_id=review.user_id, room_id=review.room_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_review(db: Session, review_id: int):
    return db.query(models.Review).filter(models.Review.id == review_id).first()

def get_all_reviews(db: Session):
    return db.query(models.Review).all()

def delete_review(db: Session, review_id: int):
    db_review = get_review(db, review_id)
    if db_review:
        db.delete(db_review)
        db.commit()
