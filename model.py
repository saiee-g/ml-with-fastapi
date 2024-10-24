from sqlalchemy import Column, Integer, String
from demo.config import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(50))
    gender = Column(String(1))
    age = Column(Integer)

