from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

print({settings.database_user})
SQL_ALCHEMY_DATABASE_URL = f'postgresql://{settings.database_user}:{settings.database_pass}@{settings.database_host}:{settings.database_port}/{settings.database_name}'
print(f"Database URL: {SQL_ALCHEMY_DATABASE_URL}")
engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
        print("connected")
    finally:
        db.close()
        print("Disconnected")