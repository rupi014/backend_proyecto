from sqlalchemy.orm import Session
from models import *
from schemas import *
from fastapi import HTTPException

# Funciones para la gestion de pedidos
def get_orders(db: Session):
    return db.query(Orders).all()

def get_order_by_id(db: Session, order_id: int):
    return db.query(Orders).filter(Orders.id == order_id).first()

def get_orders_by_user_id(db: Session, user_id: int):
    user = db.query(Users).filter(Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")    
    orders = db.query(Orders).filter(Orders.user_id == user_id).all()
    if not orders:
        raise HTTPException(status_code=404, detail="El usuario no tiene pedidos")    
    return orders

def create_order(db: Session, order: OrdersData):
    user = db.query(Users).filter(Users.id == order.user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db_order = Orders(user_id=order.user_id, order_date=order.order_date, total_price=order.total_price, status=order.status)
    db.add(db_order)
    db.commit()
    db.flush(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = db.query(Orders).filter(Orders.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    db.delete(db_order)
    db.commit()
    return db_order

def update_order(db: Session, order_id: int, order: OrdersData):
    db_order = db.query(Orders).filter(Orders.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    db_order.user_id = order.user_id
    db_order.order_date = order.order_date
    db_order.total_price = order.total_price
    db_order.status = order.status
    db.commit()
    return db_order
