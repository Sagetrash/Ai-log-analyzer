from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel
import os, json
from datetime import datetime
from HistoryManager import appendHistory, displayHistory

load_dotenv()
client = genai.Client()
app = FastAPI()
historyname = "History.json"

class LogAnalysis(BaseModel):
    Brief: str
    solution: list[str]

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
        return response.parsed
    except HTTPException as e:
        
        raise e


@app.get("/getHistory")
async def getHistory():
    return await displayHistory(filename=historyname)











####### helper functions
async def toHistory(response:dict):
    metadata = {
        "timestamp":datetime.now().isoformat()
    }
    metadata.update(response)
    await appendHistory(metadata,filename=historyname)