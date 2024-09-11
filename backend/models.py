from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DECIMAL, DateTime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    telephone = Column(String)
    address = Column(String)
    role = Column(String)

class Staff(Base):
    __tablename__ = "staff"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String)
    bio = Column(String)
    image = Column(String)
    twitter = Column(String)

class Players(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String)
    bio = Column(String)
    image = Column(String)
    twitter = Column(String)

class Blog(Base):
    __tablename__ = "blog"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    image = Column(String)
    date = Column(String)
    author = Column(String, ForeignKey("users.id")) 

class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(DECIMAL)
    image = Column(String)
    category = Column(String)
    stock = Column(Integer)

class Orders(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    order_date = Column(DateTime)
    total_price = Column(DECIMAL)
    status = Column(String)

class ProductOrder(Base):
    __tablename__ = "product_order"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
    quantity = Column(Integer)
    price = Column(DECIMAL)
    total = Column(DECIMAL)


    
    