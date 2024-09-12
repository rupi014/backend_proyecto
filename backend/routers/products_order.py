from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import ProductOrderData
import crud.products_order_crud as products_order_crud
from database import engine, SessionLocal
from models import Base

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
            db.close()

router = APIRouter(prefix="/products_order", tags=["Products Order"], responses={404: {"description": "No encontrado"}})  

Base.metadata.create_all(bind=engine)

# Ruta para agregar un producto a un pedido
@router.post("/", response_model=ProductOrderData)
async def add_product_to_order(product_order: ProductOrderData, db: Session = Depends(get_db)):
    return products_order_crud.add_product_to_order(db=db, product_order=product_order)

# Ruta para obtener todos los productos de un pedido
@router.get("/{product_order_id}", response_model=list[ProductOrderData])
async def get_products_order(product_order_id: int, db: Session = Depends(get_db)):
    return products_order_crud.get_products_order_by_id(db=db, products_order_id=product_order_id)

# Ruta para eliminar un producto de un pedido
@router.delete("/{order_id}/{product_id}", response_model=dict)
async def delete_product_from_order(order_id: int, product_id: int, db: Session = Depends(get_db)):
    return products_order_crud.delete_product_from_order(db=db, order_id=order_id, product_id=product_id)

# Ruta para actualizar un producto de un pedido
@router.put("/{order_id}/{product_id}", response_model=ProductOrderData)
async def update_product_from_order(order_id: int, product_id: int, product_order: ProductOrderData, db: Session = Depends(get_db)):
    return products_order_crud.update_product_from_order(db=db, order_id=order_id, product_id=product_id, product_order=product_order)
