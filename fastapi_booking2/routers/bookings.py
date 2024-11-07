from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import db_bookings
from db.database import get_db
from schemas import BookingCreate, BookingDisplay
from typing import List

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)

@router.post("/", response_model=BookingDisplay)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    return db_bookings.create_booking(db, booking)

@router.get("/{booking_id}", response_model=BookingDisplay)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db_bookings.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    return booking

@router.get("/", response_model=List[BookingDisplay])
def get_all_bookings(db: Session = Depends(get_db)):
    return db_bookings.get_all_bookings(db)

@router.delete("/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    db_bookings.delete_booking(db, booking_id)
    return {"detail": "Booking deleted successfully"}
