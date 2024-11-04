from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import db_rooms
from db.database import get_db
from schemas import RoomCreate, RoomDisplay
from typing import List

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)

@router.post("/", response_model=RoomDisplay)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    return db_rooms.create_room(db, room)

@router.get("/{room_id}", response_model=RoomDisplay)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db_rooms.get_room(db, room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return room

@router.get("/", response_model=List[RoomDisplay])
def get_all_rooms(db: Session = Depends(get_db)):
    return db_rooms.get_all_rooms(db)

@router.put("/{room_id}", response_model=RoomDisplay)
def update_room(room_id: int, room: RoomCreate, db: Session = Depends(get_db)):
    return db_rooms.update_room(db, room_id, room)

@router.delete("/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    db_rooms.delete_room(db, room_id)
    return {"detail": "Room deleted successfully"}
