from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_admin = Column(Boolean)
    
    reviews = relationship("Review", back_populates="user")
    bookings = relationship("Booking", back_populates="user")
    hotels = relationship("Hotel", back_populates="user")

class Hotel(Base):
    __tablename__ = 'hotels'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String)
    address = Column(String)
    
    user = relationship("User", back_populates="hotels")
    rooms = relationship("Room", back_populates="hotel")

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    room_type = Column(String)
    room_number = Column(String, unique=True)
    availability = Column(Boolean, default=True)
    
    hotel = relationship("Hotel", back_populates="rooms")
    reviews = relationship("Review", back_populates="room")
    bookings = relationship("Booking", back_populates="room")

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String)
    review_time = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reviews")
    room = relationship("Room", back_populates="reviews")

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    room_id = Column(Integer, ForeignKey('rooms.id'))
    check_in = Column(DateTime)
    check_out = Column(DateTime)
    
    user = relationship("User", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")


# مدل Wishlist
class Wishlist(Base):
    __tablename__ = 'wishlist'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    hotel_id = Column(Integer, ForeignKey('hotels.id'), nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="wishlist")
    hotel = relationship("Hotel", back_populates="wishlist_entries")
