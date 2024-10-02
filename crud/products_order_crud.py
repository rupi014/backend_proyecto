from sqlalchemy.orm import Session
from models import *
from schemas import *
from fastapi import HTTPException

# Funcion para obtener todos los productos de un pedido
def get_products_order(db: Session):
    return db.query(ProductOrder).all()

# Funcion para obtener un producto de un pedido por id
def get_products_order_by_id(db: Session, products_order_id: int):
    order = db.query(Orders).filter(Orders.id == products_order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return db.query(ProductOrder).filter(ProductOrder.order_id == products_order_id).all()

# Funcion para agregar un producto a un pedido
def add_product_to_order(db: Session, product_order: ProductOrder):
    db_product_order = ProductOrder(product_id=product_order.product_id, order_id=product_order.order_id, quantity=product_order.quantity, price=product_order.price, total=product_order.total, size=product_order.size)
    db.add(db_product_order)
    db.commit()
    db.flush(db_product_order)
    return db_product_order

# Funcion para eliminar un producto de un pedido
def delete_product_from_order(db: Session, order_id: int, product_id: int):
    product_order = db.query(ProductOrder).filter(ProductOrder.order_id == order_id, ProductOrder.product_id == product_id).first()
    if not product_order:
        raise HTTPException(status_code=404, detail="Producto no encontrado en el pedido")
    
    db.delete(product_order)
    db.commit()
    return {"message": "Producto eliminado del pedido"}

# Funcion para actualizar un producto de un pedido
def update_product_from_order(db: Session, order_id: int, product_id: int, product_order: ProductOrder):
    db_product_order = db.query(ProductOrder).filter(ProductOrder.order_id == order_id, ProductOrder.product_id == product_id).first()
    if db_product_order is None:
        raise HTTPException(status_code=404, detail="Producto de pedido no encontrado")
    db_product_order.product_id = product_order.product_id
    db_product_order.order_id = product_order.order_id
    db_product_order.quantity = product_order.quantity
    db_product_order.price = product_order.price
    db_product_order.total = product_order.total
    db_product_order.size = product_order.size
    db.commit()
    return db_product_order