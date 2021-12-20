from fastapi import Depends, HTTPException, Request, APIRouter
from accounts import schemas
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

@router.post("/api/register")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    '''Function to Create a New User'''
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    else:
        hashed_pass = Hash.bcrypt(user.password)
        db_user = models.User(username=user.username,email=user.email, password=hashed_pass)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        temp = db_user.__dict__
        temp.pop("password")
        return db_user
        

@router.post("/api/login")
def login_user(user: schemas.Login, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == user.username).first():
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        if not Hash.verify(db_user.password,user.password):
            return HTTPException(status_code=400,detail="Wrong Password")
        access_token = create_access_token(data={"sub": db_user.email })
        db_user.password = "Hidden"
        return {"token": access_token}
    else:
        return {"status":"User not registered"}

@router.get("/api/user_detail")
def get_user(req: Request, db: Session = Depends(get_db)):
    token = req.headers["Authorization"]
    user = verify_token(token,credentials_exception="404")
    db_user = db.query(models.User).filter(models.User.email == user).first()
    db_user = db_user.__dict__
    db_user.pop("password")
    return db_user