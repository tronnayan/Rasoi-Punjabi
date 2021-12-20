from fastapi.exceptions import HTTPException
from jose.jws import verify
from passlib.utils import accepts_keyword
from sqlalchemy.orm import Session
from utilities.hashing import Hash
from utilities.jwttoken import create_access_token,verify_token
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,Request
from accounts import schemas
from utilities import models
import random
import string
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# def get_id_by_token(req: Request,db: Session):
#     token = req.headers["Authorization"]
#     user = verify_token(token,credentials_exception="404")
#     uid = db.query(models.User).filter(models.User.email==user).first()
#     return uid.id



# def login_user(db: Session, user: schemas.Login):
#     '''Login Function , verify user credentials'''
#     db_user = get_user_by_email(db,email=user.email)
#     if not Hash.verify(db_user.password,user.password):
#         return HTTPException(status_code=400,detail="Wrong Password")
#     access_token = create_access_token(data={"sub": user.email })
#     db_user.password = "Hidden"
#     return {"status": "Login Successful" , "access_token": access_token,"user": db_user}


# def reset_pass(db:Session,user: schemas.Reset,token):
#     '''Reset Pass Utility'''
#     users = verify_token(token,credentials_exception="404")
#     if user:
#         db_user = get_user_by_email(db,email=users)
#         hashed_pass = Hash.bcrypt(user.new_password)
#         if Hash.verify(db_user.password,user.old_password):
#             db_user.password = hashed_pass
#             db.add(db_user)
#             db.commit()
#             return {"status":"Password Changed Successfully"} 
#         else:
#             return {"status":"Incorrect Password"} 
#     else:
#         raise HTTPException(status_code=401, detail="Unauthorized User")


# def get_current_user(req: Request):
#     '''This function extracts the current user_id from the JWT token'''
#     token = req.headers["Authorization"]
#     user = verify_token(token,credentials_exception="404")
#     return user

# def get_random_string():
#     result_str = ''.join(random.choice(string.ascii_letters) for i in range(8))
#     return(result_str)
