from sqlalchemy.orm import Session
from demo.model import User


def get_user(titanic:Session):
    return titanic.query(User).all()

def add_user(titanic:Session, name:str, gender:str, age:int):
    titanic_user = User(name=name, gender=gender, age=age)
    titanic.add(titanic_user)
    titanic.commit()
    titanic.refresh(titanic_user)
    return titanic_user

def update_user(titanic:Session, id: int, name:str, gender:str, age:int):
    user_to_update = titanic.query(User).where(User.id == id).first()
    if user_to_update:
        user_to_update.name = name
        user_to_update.gender = gender
        user_to_update.age = age
        titanic.commit()
        titanic.refresh(user_to_update)
        return True
    return None