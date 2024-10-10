from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import StaffData, UserData
from routers.auth import get_current_user
import crud.staff_crud as staff_crud
from database import engine, SessionLocal
from models import Base


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


router = APIRouter(prefix="/staff", tags=["Staff"], responses={404: {"description": "No encontrado"}})

Base.metadata.create_all(bind=engine)

# Rutas para la gestion de staff

@router.post("/", response_model=StaffData)
async def create_staff(staff: StaffData, db: Session = Depends(get_db), actual_user: UserData = Depends(get_current_user)):
    if not actual_user:
        raise HTTPException(status_code=401, detail="No autorizado")
    check_staff = staff_crud.get_staff_by_id(db, staff_id=staff.id)
    if check_staff:
        raise HTTPException(status_code=400, detail="El miembro del staff ya existe")
    return staff_crud.create_staff(db=db, staff=staff)

@router.get("/", response_model=list[StaffData])
async def get_staff(db: Session = Depends(get_db)):
    staff = staff_crud.get_staff(db)
    if not staff:
        raise HTTPException(status_code=404, detail="No se encontraron miembros del staff")
    return staff

@router.get("/{staff_id}", response_model=StaffData)
async def get_staff_by_id(staff_id: int, db: Session = Depends(get_db)):
    staff = staff_crud.get_staff_by_id(db, staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Miembro del staff no encontrado")
    return staff

@router.delete("/{staff_id}", response_model=dict)
async def delete_staff(staff_id: int, db: Session = Depends(get_db), actual_user: UserData = Depends(get_current_user)):
    if not actual_user:
        raise HTTPException(status_code=401, detail="No autorizado")
    staff = staff_crud.get_staff_by_id(db, staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Miembro del staff no encontrado")
    staff_crud.delete_staff(db, staff_id)
    return {"mensaje": f"Miembro del staff con ID {staff_id} eliminado exitosamente"}

@router.put("/{staff_id}", response_model=StaffData)
async def update_staff(staff_id: int, staff: StaffData, db: Session = Depends(get_db), actual_user: UserData = Depends(get_current_user)):
    if not actual_user:
        raise HTTPException(status_code=401, detail="No autorizado")
    updated_staff = staff_crud.update_staff(db, staff_id, staff)
    if not updated_staff:
        raise HTTPException(status_code=404, detail="Miembro del staff no encontrado")
    return updated_staff        



