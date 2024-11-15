from auth.oauth2 import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import db_hotels
from db.database import get_db
from schemas import HotelCreate, HotelDisplay
from typing import List, Optional

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"]
)

@router.post("/", response_model=HotelDisplay)
def create_hotel(hotel: HotelCreate, db: Session = Depends(get_db)):
    return db_hotels.create_hotel(db, hotel)


@router.get("/{hotel_id}", response_model=HotelDisplay)
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = db_hotels.get_hotel(db, hotel_id)
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    return hotel

# there is one function i need to implement Jurgen showd it for filtering
@router.get("/", response_model=List[HotelDisplay])
def get_all_hotels(is_booked_by_user_id: Optional[int] = None, db: Session = Depends(get_db)):
    return db_hotels.get_all_hotels(db)

@router.put("/{hotel_id}", response_model=HotelDisplay)
def update_hotel(hotel_id: int, hotel: HotelCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(403, "You're not allowed to do this")
    
    return db_hotels.update_hotel(db, hotel_id, hotel)

@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(403, "You're not allowed to do this")
    db_hotels.delete_hotel(db, hotel_id)
    return {"detail": "Hotel deleted successfully"}
