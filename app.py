from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from demo.config import get_titanic, engine
from demo import crud, model


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
def show_user(titanic: Session = Depends(get_titanic)):
    users = crud.get_user(titanic)
    return users

@app.post("/users/")
def create_user(request: Request, name: str = Form(...), gender: str = Form(...), age:int = Form(...), titanic: Session = Depends(get_titanic)):
    titanic_user = crud.add_user(titanic, name, gender, age)
    return titanic_user

@app.put("/users/{id}")
def update_user(id:int, name: str, gender: str, age:int, titanic: Session = Depends(get_titanic)):
    updated_user = crud.update_user(titanic, id, name, gender, age)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return updated_user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)