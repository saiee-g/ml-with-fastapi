from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://postgres:Saiee%40123@localhost:5432/titanic"

engine = create_engine(DATABASE_URL)

SessionLocal  = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_titanic():
    titanic = SessionLocal()
    try:
        yield titanic
    finally:
        titanic.close()
    
