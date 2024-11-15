from fastapi import FastAPI
from auth import authentication
from db.database import engine, Base
from routers import users, hotels, rooms, reviews, bookings, wishlist



app = FastAPI()

app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(hotels.router)
app.include_router(rooms.router)
app.include_router(reviews.router)
app.include_router(bookings.router)
app.include_router(wishlist.router)


Base.metadata.create_all(bind=engine)