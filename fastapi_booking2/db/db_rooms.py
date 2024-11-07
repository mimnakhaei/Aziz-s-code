from sqlalchemy.orm import Session
from db import models
from schemas import RoomCreate

def create_room(db: Session, room: RoomCreate):
    db_room = models.Room(room_type=room.room_type, room_number=room.room_number, availability=room.availability, hotel_id=room.hotel_id)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def get_room(db: Session, room_id: int):
    return db.query(models.Room).filter(models.Room.id == room_id).first()

def get_all_rooms(db: Session):
    return db.query(models.Room).all()

def update_room(db: Session, room_id: int, room: RoomCreate):
    db_room = get_room(db, room_id)
    if db_room:
        db_room.room_type = room.room_type
        db_room.room_number = room.room_number
        db_room.availability = room.availability
        db.commit()
        db.refresh(db_room)
    return db_room

def delete_room(db: Session, room_id: int):
    db_room = get_room(db, room_id)
    if db_room:
        db.delete(db_room)
        db.commit()
