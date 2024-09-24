from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal
from schemas import *
from models import Base
from routers import staff, players, blog, products, orders, products_order, auth 


Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configurar CORS
origins = [
    "http://localhost:3000",
    "http://localhost:3000/status",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers

app.include_router(auth.router)
app.include_router(staff.router)
app.include_router(players.router)
app.include_router(blog.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(products_order.router)


@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de gestión de Vikings"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

