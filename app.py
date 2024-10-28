from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from demo.config import get_titanic, engine
from demo import crud, model


app = FastAPI()
model.Base.metadata.create_all(bind=engine)

@app.get("/")
def welcome():
    return {"Message" : "Welcome to our Ship"}

@app.get("/users/")
def show_user(titanic: Session = Depends(get_titanic)):
    users = crud.get_user(titanic)
    return users

@app.post("/users/")
def create_user(name: str, gender: str, age:int, titanic: Session = Depends(get_titanic)):
    titanic_user = crud.add_user(titanic, name, gender, age)
    return titanic_user

@app.put("/users/{id}")
def update_user(id:int, name: str, gender: str, age:int, titanic: Session = Depends(get_titanic)):
    updated_user = crud.update_user(titanic, id, name, gender, age)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return updated_user

@app.delete("/users/{id}/")
def delete_user(id: int, titanic: Session = Depends(get_titanic)):
    existing_user = crud.get_user_id(titanic, id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not Found")
    
    deleted_user = crud.delete_user(titanic, id)
    if not deleted_user:
        raise HTTPException(status_code=400, detail="Error Deleting User")
    return {"message" : "User info deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
