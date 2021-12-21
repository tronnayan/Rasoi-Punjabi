from sys import modules
from fastapi import Depends, Request, Form, File, UploadFile , APIRouter, HTTPException
from products import schemas
from utilities import crud ,models
from utilities.jwttoken import *
from utilities.hashing import *
from utilities.database import SessionLocal
from sqlalchemy.orm import Session
import boto3
from botocore.exceptions import NoCredentialsError
from decouple import config
import uuid
from cloudinary.utils import cloudinary_url
from cloudinary.uploader import upload
import cloudinary.api

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/api/add-product")
def add_product(req: Request, data: schemas.Product, db: Session = Depends(get_db)):
    token = req.headers["Authorization"]
    if crud.verify_token(token,credentials_exception="404"):
        if db.query(models.Product).filter(models.Product.title == data.title).first():
            return "Product name taken"
        new_product = models.Product(title = data.title, category = data.category, description = data.description, price = data.price)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        temp = new_product.__dict__
        temp["images"]  = db.query(models.Image).filter(models.Image.product == new_product.id).all()
        return temp
    else:
        return HTTPException(status_code=404,detail="User not registered")


@router.get("/api/products")
def get_product(req: Request, db: Session = Depends(get_db)):
    token = req.headers["Authorization"]
    if crud.verify_token(token,credentials_exception="404"):
        product_data = db.query(models.Product).all()
        for p in product_data:
            temp = p.__dict__
            temp["images"]  = db.query(models.Image).filter(models.Image.product == p.id).all()
        return product_data
    else:
        return HTTPException(status_code=404,detail="User not registered")


@router.post("/api/category")
def add_category(req: Request, data: schemas.Category, db: Session = Depends(get_db)):
    token = req.headers["Authorization"]
    if crud.verify_token(token,credentials_exception="404"):
        if db.query(models.Category).filter(models.Category.title == data.title).first():
            return "Category name taken"
        new_category = models.Category(title = data.title, description = data.description, image_url = data.image_url)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    else:
        return HTTPException(status_code=404,detail="User not registered")


@router.post("/api/add-image")
def add_image(req: Request,file : UploadFile = File(...), product: int = Form(...), db: Session = Depends(get_db)):
    token = req.headers["Authorization"]
    if crud.verify_token(token,credentials_exception="404"):
        file_url = ''
        data = file.file._file
        cloudinary.config(cloud_name = config('CLOUD_NAME'), api_key=config('API_KEY'), 
        api_secret=config('API_SECRET'))
        upload_result = cloudinary.uploader.upload(data)
        file_url = upload_result['secure_url']
        new_image = models.Image(url = file_url, product = product)
        db.add(new_image)
        db.commit()
        db.refresh(new_image)
        return new_image
    
@router.get("/api/category")
def show_category(req:Request, db: Session = Depends(get_db)):
    token = req.headers["Authorization"]
    if crud.verify_token(token,credentials_exception="404"):
        return db.query(models.Category).all()