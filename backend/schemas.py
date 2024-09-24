from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import Numeric
from typing import Optional


class UserData(BaseModel):
    username: str
    email: Optional[str] = ""
    password: str
    telephone: Optional[str] = ""
    address: Optional[str] = ""
    role: Optional[str] = "user"

class StaffData(BaseModel):
    id: int
    name: str
    role: str
    bio: str
    image: str
    twitter: str

class PlayerData(BaseModel):
    id: int
    name: str
    role: str
    bio: str
    image: str
    twitter: str

class BlogData(BaseModel):
    id: int
    title: str
    content: str
    image: str
    date: datetime
    author_id: int

class ProductData(BaseModel):
    id: int
    name: str
    description: str
    price: float    
    image: str
    category: str
    stock: int      

class OrdersData(BaseModel):
    id: int
    user_id: int
    order_date: datetime
    total_price: float    
    status: str

class ProductOrderData(BaseModel):
    id: int
    product_id: int
    order_id: int
    quantity: int
    price: float
    total: float


