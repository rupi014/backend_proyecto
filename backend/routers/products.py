from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import ProductData, UserData
from routers.auth import get_current_user
import crud.products_crud as products_crud
from database import engine, SessionLocal
from models import Base

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
            db.close()

router = APIRouter(prefix="/products", tags=["Products"], responses={404: {"description": "No encontrado"}})  

Base.metadata.create_all(bind=engine)

@router.post("/", response_model=ProductData)
async def create_product(product: ProductData, db: Session = Depends(get_db), usuario_actual: UserData = Depends(get_current_user)):
    # Verificar si el usuario actual está autenticado
    if not usuario_actual:
        raise HTTPException(status_code=401, detail="No autorizado")
    check_product = products_crud.get_product_by_id(db, product_id=product.id)
    if check_product:
        raise HTTPException(status_code=400, detail="El producto ya existe")
    return products_crud.create_product(db=db, product=product)

@router.get("/", response_model=list[ProductData])
async def get_products(db: Session = Depends(get_db)):
    products = products_crud.get_products(db)
    if not products:
        raise HTTPException(status_code=404, detail="No se encontraron productos")
    return products

@router.get("/{product_id}", response_model=ProductData)
async def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = products_crud.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.get("/category/{category}", response_model=list[ProductData])
async def get_products_by_category(category: str, db: Session = Depends(get_db)):
    products = products_crud.get_products_by_category(db, category)
    if not products:
        raise HTTPException(status_code=404, detail="No se encontraron productos en esa categoría")
    return products

@router.delete("/{product_id}", response_model=dict)
async def delete_product(product_id: int, db: Session = Depends(get_db), usuario_actual: UserData = Depends(get_current_user)):
    # Verificar si el usuario actual está autenticado
    if not usuario_actual:
        raise HTTPException(status_code=401, detail="No autorizado")
    success  = products_crud.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": f"Producto con ID {product_id} eliminado correctamente"}

@router.put("/{product_id}", response_model=ProductData)
async def update_product(product_id: int, product: ProductData, db: Session = Depends(get_db), usuario_actual: UserData = Depends(get_current_user)):
    # Verificar si el usuario actual está autenticado
    if not usuario_actual:
        raise HTTPException(status_code=401, detail="No autorizado")
    product = products_crud.update_product(db, product_id, product)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

