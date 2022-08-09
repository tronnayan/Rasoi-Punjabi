from sys import modules
from fastapi import Depends, Request, Form, File, UploadFile , APIRouter, HTTPException
from sqlalchemy.orm.session import SessionTransaction
from sqlalchemy.sql.functions import mode
from products import schemas
from utilities import crud ,models
from utilities.jwttoken import *
from utilities.hashing import *
from utilities.database import SessionLocal
from sqlalchemy.orm import Session
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
def add_product(req: Request, image : UploadFile = File(...), title: str = Form(...),category: int = Form(...),description: str = Form(...), price: str = Form(...), quantity: str = Form(...),db: Session = Depends(get_db)):
    token = req.headers["Authorization"]
    if crud.verify_token(token,credentials_exception="404"):
        if db.query(models.Product).filter(models.Product.title == title).first():
            return "Product name taken"

        file_url = ''
        data = image.file._file
        cloudinary.config(cloud_name = config('CLOUD_NAME'), api_key=config('API_KEY'), 
        api_secret=config('API_SECRET'))
        upload_result = cloudinary.uploader.upload(data)
        file_url = upload_result['secure_url']
        new_product = models.Product(title = title, category = category, description = description, price = price, quantity = quantity, image_url = file_url)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    else:
        return HTTPException(status_code=404,detail="User not registered")


@router.get("/api/products")
def get_product(req: Request, db: Session = Depends(get_db)):
    token = req.headers["Authorization"]
    if crud.verify_token(token,credentials_exception="404"):
        product_data = db.query(models.Product).all()
        return product_data
    else:
        return HTTPException(status_code=404,detail="User not registered")

@router.put("/api/products/{product_id}")
def update_image(product_id, req: Request, image : UploadFile = File(...), title: str = Form(...),category: int = Form(...),description: str = Form(...), price: str = Form(...), quantity: str = Form(...),db: Session = Depends(get_db)):
    token = req.headers["Authorization"]
    if crud.verify_token(token,credentials_exception="404"):
        file_url = ''
        data = image.file._file
        cloudinary.config(cloud_name = config('CLOUD_NAME'), api_key=config('API_KEY'), 
        api_secret=config('API_SECRET'))
        upload_result = cloudinary.uploader.upload(data)
        file_url = upload_result['secure_url']
        db.query(models.Product).filter(models.Product.id == product_id).update({models.Product.title:title, models.Product.description:description,models.Product.price:price, models.Product.image_url:file_url,models.Product.category:category,models.Product.quantity:quantity})
        db.commit()
        return db.query(models.Product).filter(models.Product.id == product_id).first()
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

@router.get("/api/category")
def show_category(req:Request, db: Session = Depends(get_db)):
    token = req.headers["Authorization"]
    if crud.verify_token(token,credentials_exception="404"):
        return db.query(models.Category).all()


@router.get("/api/category/{category_id}")
def get_category(category_id, req:Request, db: Session = Depends(get_db)):
    token = req.headers["Authorization"]
    if crud.verify_token(token,credentials_exception="404"):
        data =  db.query(models.Product).filter(models.Product.category == category_id).all()
        return data


@router.get("/api/dashboard")
def fetch_all(req:Request, db: Session = Depends(get_db)):
    token = req.headers["Authorization"]
    if crud.verify_token(token, credentials_exception="404"):
        obj = dict()
        obj["category"] = db.query(models.Category).all()
        obj["products"] = db.query(models.Product).all()
        obj["feature"] = db.query(models.FeatureProduct).all()
        return obj


@router.post("/api/feature-product")
def add_feature_product(req:Request,image : UploadFile = File(...), product : int = Form(...), db:Session = Depends(get_db)):
    token = req.headers["Authorization"]
    if crud.verify_token(token,credentials_exception="404"):
        file_url = ''
        data = image.file._file
        cloudinary.config(cloud_name = config('CLOUD_NAME'), api_key=config('API_KEY'), 
        api_secret=config('API_SECRET'))
        upload_result = cloudinary.uploader.upload(data)
        file_url = upload_result['secure_url']
        new_fproduct = models.FeatureProduct(product = product, image_url = file_url)
        db.add(new_fproduct)
        db.commit()
        db.refresh(new_fproduct)
        return new_fproduct
    else:
        return HTTPException(status_code=404,detail="User not registered")

