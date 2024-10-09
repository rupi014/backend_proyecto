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
from dotenv import load_dotenv
import os

load_dotenv()

# Configuración de seguridad
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(tags=["Users/Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str):
    user = users_crud.get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_acces_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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
    user = users_crud.get_user_by_username(db, username=username)
    if user is None:
        raise credenciales_exception
    return user

# Login

@router.post("/token")
async def access_token_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_acces_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Usuarios

@router.get("/users/me", response_model=UserData)
async def read_users_me(actual_user: UserData = Depends(get_current_user)):
    return actual_user

@router.post("/register", response_model=UserData)
async def register_user(user: UserData, db: Session = Depends(get_db)):
    db_user = users_crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está registrado")
    user.password = get_password_hash(user.password)
    return users_crud.create_user(db=db, user=user)

@router.get("/users", response_model=list[UserData])
async def read_users(db: Session = Depends(get_db), actual_user: UserData = Depends(get_current_user)):
    users = users_crud.get_users(db)
    if not users or actual_user.role != "admin":
        raise HTTPException(status_code=404, detail="No se encontraron usuarios")
    return users

@router.get("/users/{user_id}", response_model=UserData)
async def read_user_by_id(user_id: int, db: Session = Depends(get_db), actual_user: UserData = Depends(get_current_user)):
    user = users_crud.get_user(db, user_id)
    if not user or actual_user.role != "admin":
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int, db: Session = Depends(get_db), actual_user: UserData = Depends(get_current_user)):
    user = users_crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if actual_user.role != "admin":
        raise HTTPException(status_code=401, detail="No autorizado")
    users_crud.delete_user(db, user_id)
    return {"mensaje": f"Usuario con ID {user_id} eliminado exitosamente"}

@router.put("/users/{user_id}", response_model=UserData)
async def update_user(user_id: int, user: UserData, db: Session = Depends(get_db), actual_user: UserData = Depends(get_current_user)):
    user_exist = users_crud.get_user(db, user_id)
    if not user_exist or actual_user.role != "admin":
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user_updated = users_crud.update_user(db, user_id, user)
    if not user_updated:
        raise HTTPException(status_code=500, detail="Error al actualizar el usuario")
    
    return user_updated
