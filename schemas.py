from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import Numeric
from typing import Optional


class UserData(BaseModel):
    id: Optional[int] = None 
    username: str
    email: Optional[str] = ""
    password: str
    telephone: Optional[str] = ""
    address: Optional[str] = ""
    role: Optional[str] = "user"

class StaffData(BaseModel):
    id: Optional[int] = None 
    name: str
    role: str
    bio: str
    image: str
    twitter: str

class PlayerData(BaseModel):
    id: Optional[int] = None  
    name: str
    role: str
    bio: str
    image: str
    twitter: str

class BlogData(BaseModel):
    id: Optional[int] = None 
    title: str
    content: str
    image: str
    date: datetime
    author_id: int

class ProductData(BaseModel):
    id: Optional[int] = None  
    name: str
    description: str
    price: float    
    image: str
    category: str
    stock: int      
    size: Optional[str] = None

class OrdersData(BaseModel):
    id: Optional[int] = None  
    user_id: int
    order_date: datetime
    total_price: float    
    status: str

class ProductOrderData(BaseModel):
    id: Optional[int] = None  
    product_id: int
    order_id: int
    quantity: int
    price: float
    total: float
    size: Optional[str] = None

