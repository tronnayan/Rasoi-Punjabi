from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore
from decouple import config

SQLALCHEMY_DATABASE_URI = f"{config('dbtype')}://{config('user')}:{config('password') }@{config('host')}:{config('port')}/{config('db')}"
engine = create_engine(
    SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
