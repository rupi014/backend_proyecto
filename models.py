from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, DECIMAL
from database import Base
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    telephone = Column(String(15))
    address = Column(String(255))
    role = Column(String(50))

    blogs = relationship("Blog", back_populates="author_user")
    orders = relationship("Orders", back_populates="user")  

class Staff(Base):
    __tablename__ = "staff"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    role = Column(String(50))
    bio = Column(String(255))
    image = Column(String(255))
    twitter = Column(String(50))

class Players(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    role = Column(String(50))
    bio = Column(String(255))
    image = Column(String(255))
    twitter = Column(String(50))

class Blog(Base):
    __tablename__ = "blog"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    content = Column(Text)
    image = Column(String(255))
    date = Column(DateTime)
    author_id = Column(Integer, ForeignKey("users.id"))  

    author_user = relationship("Users", back_populates="blogs")

class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(String(255))
    price = Column(DECIMAL(10, 2))
    image = Column(String(255))
    category = Column(String(50))
    stock = Column(Integer)
    size = Column(String(50))   

    product_order = relationship("ProductOrder", back_populates="product")

class Orders(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    order_date = Column(DateTime)
    total_price = Column(DECIMAL(10, 2))
    status = Column(String(50))

    user = relationship("Users", back_populates="orders")
    product_order = relationship("ProductOrder", back_populates="order")

class ProductOrder(Base):
    __tablename__ = "product_order"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
    quantity = Column(Integer)
    price = Column(DECIMAL(10, 2))
    total = Column(DECIMAL(10, 2))
    size = Column(String(50))
    
    product = relationship("Products", back_populates="product_order")
    order = relationship("Orders", back_populates="product_order")


    
    