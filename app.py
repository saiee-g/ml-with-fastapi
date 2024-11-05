from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from demo.config import get_titanic, engine
from demo import crud, model, ml


app = FastAPI()

app.mount("/static", StaticFiles(directory="demo/static"), name="static")
templates = Jinja2Templates(directory="demo/templates")

model.Base.metadata.create_all(bind=engine)



@app.get("/", response_class=HTMLResponse)
def welcome(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@app.get("/users/")
def show_users(titanic: Session = Depends(get_titanic)):
    users = crud.get_user(titanic)
    return users

@app.post("/users/")
def create_user(request: Request, name: str = Form(...), gender: str = Form(...), age:int = Form(...), fare:float = Form(...), pclass:int = Form(...), titanic: Session = Depends(get_titanic)):
    titanic_user = crud.add_user(titanic, name, gender, age, fare, pclass)
    return titanic_user

@app.get("/users/{id}/")
def find_user(request: Request, id:int, titanic: Session = Depends(get_titanic)):
    found_user = crud.get_user_id(titanic, id)
    if not found_user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return found_user

@app.put("/users/{id}/")
def update_user(request: Request, id:int, name: str, gender: str, age:int, fare:float, pclass:int, titanic: Session = Depends(get_titanic)):
    updated_user = crud.update_user(titanic, id, name, gender, age, fare, pclass)
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

@app.get("/predict/", response_class=HTMLResponse)
def titanic_pred_home(request: Request):
     return templates.TemplateResponse(
        request=request, name="prediction.html"
    )

@app.post("/predict/", response_class=HTMLResponse)
def titanic_prediction(request: Request, gender: str = Form(...), age: int = Form(...), fare: float = Form(...), pclass: int = Form(...)):
    titanic_survival = ml.predict_survival(pclass, gender, age, fare)
    #print(f"Prediction result: {titanic_survival}")  # Debugging line
    return templates.TemplateResponse("result.html", {"request": request, "result": titanic_survival})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
