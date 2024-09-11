from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from schemas import *
import crud
from models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close


# Rutas para la tabla Users 

@app.post("/users", response_model=UserData)
async def create_user(user: UserData, db: Session = Depends(get_db)):
    check_user = crud.get_user_by_username(db, username=user.username)
    if check_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    return crud.create_user(db=db, user=user)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users", response_model=list[UserData])
async def get_users(db: Session = Depends(get_db)):
    usuarios = crud.get_users(db)
    if not usuarios:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios")
    return usuarios

@app.get("/users/{user_id}", response_model=UserData)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    usuario = crud.get_user(db, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    usuario = crud.get_user(db, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    crud.delete_user(db, user_id)
    return {"mensaje": f"Usuario con ID {user_id} eliminado exitosamente"}


