from sqlalchemy.orm import Session
from models import *
from schemas import *

# Funciones para la tabla Users

def get_users(db: Session):
    return db.query(Users).all()

def get_user(db: Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(Users).filter(Users.username == username).first()

def create_user(db: Session, user: UserData):
    db_user = Users(username=user.username, email=user.email, password=user.password, telephone=user.telephone, address=user.address, role=user.role)
    db.add(db_user)
    db.commit()
    db.flush(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(Users).filter(Users.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

# Funciones para la tabla Staff

