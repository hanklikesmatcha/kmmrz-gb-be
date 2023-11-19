from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

db_name = settings.db_name
db_username = settings.db_username
db_password = settings.db_password
db_host = settings.db_host

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_username}:{db_password}@{db_host}:5432/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
