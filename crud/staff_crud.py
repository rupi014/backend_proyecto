from sqlalchemy.orm import Session
from models import *
from schemas import *

# Funciones para la gestion de staff
def get_staff(db: Session):
    return db.query(Staff).all()

def get_staff_by_id(db: Session, staff_id: int):
    return db.query(Staff).filter(Staff.id == staff_id).first()

def create_staff(db: Session, staff: StaffData):
    db_staff = Staff(name=staff.name, role=staff.role, bio=staff.bio, image=staff.image, twitter=staff.twitter)
    db.add(db_staff)
    db.commit()
    db.flush(db_staff)
    return db_staff

def delete_staff(db: Session, staff_id: int):
    db_staff = db.query(Staff).filter(Staff.id == staff_id).first() 
    if db_staff:
        db.delete(db_staff)
        db.commit()
        return True
    return False

def update_staff(db: Session, staff_id: int, staff: StaffData):
    db_staff = db.query(Staff).filter(Staff.id == staff_id).first() 
    if db_staff:
        db_staff.name = staff.name
        db_staff.role = staff.role
        db_staff.bio = staff.bio
        db_staff.image = staff.image
        db_staff.twitter = staff.twitter
        db.commit() 
        db.flush(db_staff)
        return db_staff
    return False