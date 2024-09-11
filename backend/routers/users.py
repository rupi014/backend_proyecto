from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import UserData
import crud.users_crud as users_crud
from database import engine, SessionLocal
from models import Base


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close


router = APIRouter(prefix="/users", tags=["Users"], responses={404: {"description": "No encontrado"}})

Base.metadata.create_all(bind=engine)


@router.post("/", response_model=UserData)
async def create_user(user: UserData, db: Session = Depends(get_db)):
    check_user = users_crud.get_user_by_username(db, username=user.username)
    if check_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    return users_crud.create_user(db=db, user=user)

@router.get("/", response_model=list[UserData])
async def get_users(db: Session = Depends(get_db)):
    usuarios = users_crud.get_users(db)
    if not usuarios:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios")
    return usuarios

@router.get("/{user_id}", response_model=UserData)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    usuario = users_crud.get_user(db, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    usuario = users_crud.get_user(db, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    users_crud.delete_user(db, user_id)
    return {"mensaje": f"Usuario con ID {user_id} eliminado exitosamente"}

@router.put("/{user_id}", response_model=UserData)
async def update_user(user_id: int, user: UserData, db: Session = Depends(get_db)):
    usuario_existente = users_crud.get_user(db, user_id)
    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario_actualizado = users_crud.update_user(db, user_id, user)
    if not usuario_actualizado:
        raise HTTPException(status_code=500, detail="Error al actualizar el usuario")
    
    return usuario_actualizado
