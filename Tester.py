from typing import Union
from fastapi import FastAPI,Request,Form
import uvicorn
from Modals import DatabaseManager
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

db=DatabaseManager("database.db")

@app.get("/content")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/content")
async def logger(request: Request,TreeID :str = Form(...),TreePass: str = Form(...)):
    if (await db.check_credentials(TreeID,TreePass)):
        result = await db.get_data_user(TreeID)
        return templates.TemplateResponse("content.html", {"request": request,"data":result,"ID":TreeID})
    return templates.TemplateResponse("index.html", {"request": request,"status":True})

@app.post("/create/{TreeID}")
async def createQuestion(TreeID,request: Request,Question :str = Form(...),Answer :str = Form(...)):
    Question=Question.strip().lower().replace(",","")
    await db.ContentCreaterUser(TreeID,Question,Answer)
    result = await db.get_data_user(TreeID)
    return templates.TemplateResponse("content.html", {"request": request,"data":result,"ID":TreeID})


@app.get("/Delete/{Item_ID}/{TreeID}")
async def DeleteRec(Item_ID,TreeID,request: Request):
    await db.del_record(Item_ID)
    result = await db.get_data_user(TreeID)
    return templates.TemplateResponse("content.html", {"request": request,"data":result,"ID":TreeID})

@app.get("/update/{item_ID}/{TreeID}")
async def updateIndex(request: Request,item_ID,TreeID):
        question_and_answer = await db.updateIndex(record_id=item_ID)
        return templates.TemplateResponse("updated.html", {"request": request,"data":question_and_answer,"details":[TreeID,item_ID]})

@app.post("/update/{item_ID}/{Tree_ID}")
async def uptodate(item_ID,Tree_ID,request: Request,Question :str = Form(...),Answer :str = Form(...)):
    await db.update(record_id=item_ID,question=Question,answer=Answer)
    result = await db.get_data_user(Tree_ID)
    return templates.TemplateResponse("content.html", {"request": request,"data":result,"ID":Tree_ID})

if __name__=="__main__":
    uvicorn.run(app)