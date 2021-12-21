from sys import modules
from fastapi import Depends, HTTPException, Request, APIRouter
from products import schemas
from utilities import crud ,models
from utilities.jwttoken import *
from utilities.hashing import *
from utilities.database import SessionLocal
from sqlalchemy.orm import Session

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


@router.get("/api/product/{product_id}")
def get_product(product_id, req: Request, db: Session = Depends(get_db)):
    token = req.headers["Authorization"]
    if crud.verify_token(token,credentials_exception="404"):
        product_data = db.query(models.Product).filter(models.Product.id == product_id).first()
        temp = product_data.__dict__
        temp["images"]  = db.query(models.Image).filter(models.Image.product == product_data.id).all()
        return temp
    else:
        return HTTPException(status_code=404,detail="User not registered")


@router.post("/api/add-category")
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
def add_image(req: Request,data: schemas.Image, db: Session = Depends(get_db)):
    token = req.headers["Authorization"]
    if crud.verify_token(token,credentials_exception="404"):
        new_image = models.Image(url = data.url, product = data.product)
        db.add(new_image)
        db.commit()
        db.refresh(new_image)
        return new_image