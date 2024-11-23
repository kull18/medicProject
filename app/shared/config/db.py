from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from sqlalchemy.pool import QueuePool


load_dotenv()

URL = os.getenv("URL")

SQLALCHEMY_DATABASE_URL = URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,  
    max_overflow=30,  
    pool_timeout=30    
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()