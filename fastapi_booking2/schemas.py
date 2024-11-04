from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class ReviewBase(BaseModel):
    content: str
    review_time: datetime = None

class ReviewCreate(ReviewBase):
    user_id: int
    room_id: int

class ReviewDisplay(ReviewBase):
    id: int
    user: 'UserBase'
    
    class Config:
        orm_mode = True
# because UserBase needed on RoomDisplay, so defined it here.      
class UserBase(BaseModel):
    username: str
    email: EmailStr

class RoomBase(BaseModel):
    type: str
    room_number: str
    availability: Optional[bool] = True

class RoomCreate(RoomBase):
    hotel_id: int

class RoomDisplay(RoomBase):
    id: int
    hotel_id: int
    reviews: List[ReviewDisplay] = []
    #user: 'UserBase'
    user: Optional[UserBase] = None  # Allow user to be None
    
    class Config:
        orm_mode = True



class UserCreate(UserBase):
    password: str

class UserDisplay(UserBase):
    id: int
    rooms: List[RoomDisplay] = []
    
    class Config:
        orm_mode = True

class HotelBase(BaseModel):
    name: str
    address: str

class HotelCreate(HotelBase):
    user_id: int

class HotelDisplay(HotelBase):
    id: int
    user: UserDisplay
    rooms: List[RoomDisplay] = []
    
    class Config:
        orm_mode = True

class BookingBase(BaseModel):
    check_in: datetime
    check_out: datetime

class BookingCreate(BookingBase):
    user_id: int
    room_id: int

class BookingDisplay(BookingBase):
    id: int
    user: UserDisplay
    room: RoomDisplay
    
    class Config:
        orm_mode = True
