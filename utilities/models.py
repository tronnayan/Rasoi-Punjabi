from typing import Text
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.sql.expression import column, null, true
from sqlalchemy.sql.schema import BLANK_SCHEMA
from sqlalchemy.sql.sqltypes import DateTime

from utilities.database import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String,default="")
    last_name = Column(String,default="")
    username = Column(String(200),unique=True)
    email = Column(String(200),unique=True)
    password = Column(String(200))

class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    description = Column(String)
    image_url = Column(String)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String, unique=True)
    category = Column(Integer, ForeignKey("category.id"))
    description = Column(String)
    in_stock = Column(Boolean,default=True)
    image_url = Column(String)
    quantity = Column(String)
    price = Column(Integer)