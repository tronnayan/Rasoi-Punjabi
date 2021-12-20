from typing import Text
from decouple import Choices
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
    first_name = Column(String,default=None)
    last_name = Column(String,default=None)
    username = Column(String(200),unique=True)
    email = Column(String(200),unique=True)
    password = Column(String(200))