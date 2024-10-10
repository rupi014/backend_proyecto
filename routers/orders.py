from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import OrdersData, UserData    
from routers.auth import get_current_user
import crud.orders_crud as orders_crud
from database import engine, SessionLocal
from models import Base

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
            db.close()

router = APIRouter(prefix="/orders", tags=["Orders"], responses={404: {"description": "No encontrado"}})  

Base.metadata.create_all(bind=engine)

# Funciones para la gestion de pedidos

@router.post("/", response_model=OrdersData)
async def create_order(order: OrdersData, db: Session = Depends(get_db), actual_user: UserData = Depends(get_current_user)):
    if not actual_user:
        raise HTTPException(status_code=401, detail="No autorizado")    
    return orders_crud.create_order(db=db, order=order)

@router.get("/", response_model=list[OrdersData])
async def get_orders(db: Session = Depends(get_db), actual_user: UserData = Depends(get_current_user)):
    if not actual_user:
        raise HTTPException(status_code=401, detail="No autorizado")    
    return orders_crud.get_orders(db)

@router.get("/{order_id}", response_model=OrdersData)
async def get_order_by_id(order_id: int, db: Session = Depends(get_db), actual_user: UserData = Depends(get_current_user)):
    if not actual_user:
        raise HTTPException(status_code=401, detail="No autorizado")    
    return orders_crud.get_order_by_id(db=db, order_id=order_id)

@router.get("/user/{user_id}", response_model=list[OrdersData])
async def get_orders_by_user_id(user_id: int, db: Session = Depends(get_db), actual_user: UserData = Depends(get_current_user)):
    if not actual_user:
        raise HTTPException(status_code=401, detail="No autorizado")    
    return orders_crud.get_orders_by_user_id(db=db, user_id=user_id)

@router.delete("/{order_id}", response_model=dict)
async def delete_order(order_id: int, db: Session = Depends(get_db), actual_user: UserData = Depends(get_current_user) ):
    if not actual_user or actual_user.role != "admin":
        raise HTTPException(status_code=401, detail="No autorizado")    
    success = orders_crud.delete_order(db=db, order_id=order_id) 
    if not success:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return {"message": f"Pedido con ID {order_id} eliminado correctamente"}

@router.put("/{order_id}", response_model=OrdersData)
async def update_order(order_id: int, order: OrdersData, db: Session = Depends(get_db), actual_user: UserData = Depends(get_current_user)):
    if not actual_user or actual_user.role != "admin":
        raise HTTPException(status_code=401, detail="No autorizado")    
    return orders_crud.update_order(db=db, order_id=order_id, order=order)

