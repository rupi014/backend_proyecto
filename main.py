from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal
from schemas import *
from models import Base
from routers import staff, players, blog, products, orders, products_order, auth 


Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuracion de CORS

origins = [
    "http://localhost:3000",
    "https://vikingsdb.up.railway.app",
    "https://vikingsapi.netlify.app",
    "https://vikingsoftherift.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routas de la API

app.include_router(auth.router)
app.include_router(staff.router)
app.include_router(players.router)
app.include_router(blog.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(products_order.router)

# Ruta principal de la API

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de gestión de Vikings"}

# Ejecutar la API

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

