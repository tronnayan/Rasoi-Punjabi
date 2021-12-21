from pydantic import BaseModel
from utilities.database import Base

from utilities.models import Category

class Product(BaseModel):
    title : str 
    category : int 
    description : str 
    price : int 

class Category(BaseModel):
    title : str 
    description : str
    image_url : str 
