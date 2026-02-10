from fastapi import FastAPI, UploadFile, File, HTTPException, Request, status
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel
import os, json
from datetime import datetime
from HistoryManager import appendHistory, displayHistory, DeleteHistory
from fastapi.templating import Jinja2Templates 
from fastapi.responses import HTMLResponse, RedirectResponse

templates = Jinja2Templates(directory="templates")

load_dotenv()
client = genai.Client()
app = FastAPI()
historyname = "History.json"

class LogAnalysis(BaseModel): # pydantic object to provide gemini with a response schema
    Brief: str
    solution: list[str]


@app.get("/", response_class=HTMLResponse)
async def readRoot(request: Request):
    history = await displayHistory(filename=historyname)
    return templates.TemplateResponse("index.html", {"request": request, "history":history})


@app.post("/analyseLog")
async def analyseLog(file: UploadFile = File(...)):
    if not file.filename.endswith((".log",".txt")):
        raise HTTPException(400,"file format not supported")
    
    if not file:
        raise HTTPException(400,"upload a file first")
    
    try:
        raw_data = await file.read()
        content = raw_data.decode("utf-8")

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents="""
            read the below given log and return a 2step solution in the format {"Breif":"error brief in one line","solution":2-step solution}, reply wiht only the dict format and nothing else"""+ content,
            config={
                "response_mime_type":"application/json",
                "response_schema":LogAnalysis
            }
        )
        await toHistory(response.parsed.model_dump())
        return RedirectResponse("/",200)
    except HTTPException as e:
        
        raise e

@app.post("/uploadText")
async def analyseText(txt: str = ...):
    try:
        content = txt
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents="""
            read the below given log and return a 2step solution in the format {"Breif":"error brief in one line","solution":2-step solution}, reply wiht only the dict format and nothing else"""+ content,
            config={
                "response_mime_type":"application/json",
                "response_schema":LogAnalysis
            }
        )
        await toHistory(response.parsed.model_dump())
        return RedirectResponse("/",200)
    except HTTPException as e:
        raise e


@app.get("/getHistory")
async def getHistory():
    return await displayHistory(filename=historyname)

@app.delete("/clearlogs")
async def clearlogs():
    return await DeleteHistory(historyname)



####### helper functions
async def toHistory(response:dict):
    metadata = {
        "timestamp":datetime.now().isoformat()
    }
    metadata.update(response)
    await appendHistory(metadata,filename=historyname)
