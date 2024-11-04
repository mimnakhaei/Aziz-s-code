from fastapi import FastAPI
from db.database import engine, Base
from routers import users, hotels, rooms, reviews, bookings


app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(hotels.router)
app.include_router(rooms.router)
app.include_router(reviews.router)
app.include_router(bookings.router)


########

@app.get("/hello")
def index():
    return {"Message": "Hello world"}

###########