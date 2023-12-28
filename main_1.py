from fastapi import FastAPI,Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
conn = sqlite3.connect('database.db')

def Questioncreater(tree_id,question,answer):
    cursor = conn.cursor()
    query = "INSERT INTO User_ID (TreeID, Question, Answer) VALUES (?, ?, ?)"
    cursor.execute(query, (tree_id,question,answer,))
    conn.commit()
    cursor.close()

def Delrecord(ID):
    cursor = conn.cursor()
    delete_query = "DELETE FROM User_ID WHERE ID = ?"  
    cursor.execute(delete_query, (ID,))
    conn.commit()
    cursor.close()

async def check_credentials(username, password):
    cursor = conn.cursor()
    query = "SELECT * FROM Logindetais WHERE UserName = ? AND UserPass = ?"
    cursor.execute(query, (username, password))
    result = cursor.fetchone() 
    cursor.close()
    return result is not None  

async def GetDataUser(TreeID):
    query = "SELECT ID, Question, Answer FROM User_ID WHERE TreeID = ?"
    cursor = conn.cursor()
    cursor.execute(query, (TreeID,))
    result = cursor.fetchall()
    if result:
        return result
    else :
        return []

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/")
async def logger(request: Request,TreeID :str = Form(...),TreePass: str = Form(...)):
    if (await check_credentials(TreeID,TreePass)):
        result = await GetDataUser(TreeID)
        return templates.TemplateResponse("content.html", {"request": request,"data":result,"ID":TreeID})
    return templates.TemplateResponse("index.html", {"request": request,"status":True})

@app.post("/create/{TreeID}")
async def createQuestion(TreeID,request: Request,Question :str = Form(...),Answer :str = Form(...)):
    Question=Question.strip().lower()
    Questioncreater(TreeID,Question,Answer)
    result = await GetDataUser(TreeID)
    return templates.TemplateResponse("content.html", {"request": request,"data":result,"ID":TreeID})


@app.get("/Delete/{Item_ID}/{TreeID}")
async def DeleteRec(Item_ID,TreeID,request: Request):
    Delrecord(Item_ID)
    result = await GetDataUser(TreeID)
    return templates.TemplateResponse("content.html", {"request": request,"data":result,"ID":TreeID})

@app.get("/update/{item_ID}/{TreeID}")
async def updateIndex(request: Request,item_ID,TreeID):
        cursor = conn.cursor()
        item_ID = int(item_ID)
        select_query = "SELECT Question, Answer FROM User_ID WHERE ID = ?"
        cursor.execute(select_query, (item_ID,))
        question_and_answer = cursor.fetchone()
        cursor.close()
        return templates.TemplateResponse("updated.html", {"request": request,"data":question_and_answer,"details":[TreeID,item_ID]})
@app.post("/update/{item_ID}/{Tree_ID}")
async def uptodate(item_ID,Tree_ID,request: Request,Question :str = Form(...),Answer :str = Form(...)):
    cursor = conn.cursor()
    update_query = "UPDATE User_ID SET Question = ?, Answer = ? WHERE ID = ?"
    cursor.execute(update_query, (Question, Answer, item_ID))
    conn.commit()
    cursor.close()
    result = await GetDataUser(Tree_ID)
    return templates.TemplateResponse("content.html", {"request": request,"data":result,"ID":Tree_ID})

if __name__=="__main__":
    uvicorn.run(app)