# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import (
    auth,
    users,
    shop_owners,
    barbers,
    admin,
    appointments,
    queue,
    feedback,
    unregistered_users
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
import uvicorn
from dotenv import load_dotenv
import os

app = FastAPI(
    title="Barbershop Queue System API",
    description="API for the Barbershop Queue System",
    version="1.0.0"
)

load_dotenv()

# Create a list of allowed origins
origins = ["*"]

# Update the CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# database initialization
@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(shop_owners.router)
app.include_router(barbers.router)
app.include_router(admin.router)
app.include_router(appointments.router)
app.include_router(queue.router)
app.include_router(feedback.router)
app.include_router(unregistered_users.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Barbershop Queue System API"}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
