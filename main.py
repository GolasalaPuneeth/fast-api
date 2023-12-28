from fastapi import FastAPI,Request, Form,Body
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sqlite3
import uvicorn
from genAI import intell

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
conn = sqlite3.connect('database.db')

class Taker(BaseModel):
    Question:str
    Answer : str

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request}),{"status":"running"}

@app.post("/")
async def MainRunner(user: Taker = Body(...)):
    print(user.Question)
    answer = await intell(user.Question)
    return {"Status":"Scuss",
           "recivedData":f"{answer}"}




if __name__=="__main__":
    uvicorn.run(app)