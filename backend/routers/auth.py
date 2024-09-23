from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from database import SessionLocal
import crud.users_crud as users_crud
from schemas import UserData

# Configuración de seguridad
SECRET_KEY = "tu_clave_secreta_aquí"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verificar_contraseña(contraseña_plana, contraseña_hash):
    return pwd_context.verify(contraseña_plana, contraseña_hash)

def obtener_hash_contraseña(contraseña):
    return pwd_context.hash(contraseña)

def autenticar_usuario(db: Session, username: str, password: str):
    usuario = users_crud.get_user_by_username(db, username)
    if not usuario:
        return False
    if not verificar_contraseña(password, usuario.password):
        return False
    return usuario

def crear_token_acceso(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def obtener_usuario_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credenciales_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credenciales_exception
    except JWTError:
        raise credenciales_exception
    usuario = users_crud.get_user_by_username(db, username=username)
    if usuario is None:
        raise credenciales_exception
    return usuario

@router.post("/token")
async def login_para_token_acceso(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = autenticar_usuario(db, form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crear_token_acceso(
        data={"sub": usuario.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/usuarios/yo", response_model=UserData)
async def leer_usuarios_yo(usuario_actual: UserData = Depends(obtener_usuario_actual)):
    return usuario_actual

@router.post("/registro", response_model=UserData)
async def registrar_usuario(usuario: UserData, db: Session = Depends(get_db)):
    db_usuario = users_crud.get_user_by_username(db, username=usuario.username)
    if db_usuario:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está registrado")
    usuario.password = obtener_hash_contraseña(usuario.password)
    return users_crud.create_user(db=db, user=usuario)

@router.get("/usuarios", response_model=list[UserData])
async def obtener_usuarios(db: Session = Depends(get_db), usuario_actual: UserData = Depends(obtener_usuario_actual)):
    usuarios = users_crud.get_users(db)
    if not usuarios:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios")
    return usuarios

@router.get("/usuarios/{user_id}", response_model=UserData)
async def obtener_usuario_por_id(user_id: int, db: Session = Depends(get_db), usuario_actual: UserData = Depends(obtener_usuario_actual)):
    usuario = users_crud.get_user(db, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.delete("/usuarios/{user_id}", response_model=dict)
async def eliminar_usuario(user_id: int, db: Session = Depends(get_db), usuario_actual: UserData = Depends(obtener_usuario_actual)):
    usuario = users_crud.get_user(db, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    users_crud.delete_user(db, user_id)
    return {"mensaje": f"Usuario con ID {user_id} eliminado exitosamente"}

@router.put("/usuarios/{user_id}", response_model=UserData)
async def actualizar_usuario(user_id: int, usuario: UserData, db: Session = Depends(get_db), usuario_actual: UserData = Depends(obtener_usuario_actual)):
    usuario_existente = users_crud.get_user(db, user_id)
    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario_actualizado = users_crud.update_user(db, user_id, usuario)
    if not usuario_actualizado:
        raise HTTPException(status_code=500, detail="Error al actualizar el usuario")
    
    return usuario_actualizado
