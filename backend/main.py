from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from schemas import *
from models import Base
from routers import users, staff, players, blog, products


Base.metadata.create_all(bind=engine)

app = FastAPI()

# Routers

app.include_router(users.router)
app.include_router(staff.router)
app.include_router(players.router)
app.include_router(blog.router)
app.include_router(products.router)


@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de gestión de Vikings"}




