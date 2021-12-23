from pydantic import BaseModel
from utilities.database import Base
from fastapi import UploadFile, File

from utilities.models import Category

class Product(BaseModel):
    title : str 
    category : int 
    description : str 
    price : int 
    image : UploadFile = File(...)
    quantity : str

class Category(BaseModel):
    title : str 
    description : str
    image_url : str 

class Image(BaseModel):
    file : UploadFile = File(...)
    product : int 
