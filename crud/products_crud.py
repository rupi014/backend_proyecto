from sqlalchemy.orm import Session
from models import *
from schemas import *
from fastapi import HTTPException

# Funciones para la gestion de productos
def get_products(db: Session):
    return db.query(Products).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(Products).filter(Products.id == product_id).first()

def get_products_by_category(db: Session, category: str):
    return db.query(Products).filter(Products.category == category).all()

def create_product(db: Session, product: ProductData):
    db_product = Products(
        name=product.name,
        description=product.description,
        price=product.price,
        image=product.image,
        category=product.category,
        stock=product.stock,
        product_size=product.product_size
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(Products).filter(Products.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False

def update_product(db: Session, product_id: int, product: ProductData):
    db_product = db.query(Products).filter(Products.id == product_id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.image = product.image
        db_product.category = product.category
        db_product.stock = product.stock
        db_product.product_size = product.product_size
        db.commit()
        db.refresh(db_product)
        return db_product
    return False

