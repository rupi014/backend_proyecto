from pydantic import BaseModel
from datetime import datetime

class UserData(BaseModel):
    id: int
    username: str
    email: str
    password: str
    telephone: str
    address: str
    role: str

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
    order_date: str
    total_price: float    
    status: str

class ProductOrderData(BaseModel):
    id: int
    product_id: int
    order_id: int
    quantity: int
    price: float
    total: float


