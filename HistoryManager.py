import os, json
from pathlib import Path
from fastapi import HTTPException

async def appendHistory(inDict: dict,filename: str):
    history = []
    if os.path.exists(filename):
        try:
            with open(filename,'r') as f:
                history = json.load(f)
        except json.JSONDecodeError:
            history = []

    history.append(inDict)

    with open(filename,'w') as f:
        json.dump(history,f,indent=4)

async def displayHistory(filename:str):
    if os.path.exists(filename):
        try:
            with open(filename,'r') as f:
                history = json.load(f)
        except json.JSONDecodeError:
            raise HTTPException(400,"file couldnt be opened")
    else:
        return []
    return history[::-1]


async def DeleteHistory(filename:str):
    if os.path.exists(filename):
        os.remove(filename)
        return "deleted history"
    else:
        raise HTTPException(404,"the file was not found, might already be deleted or was never found")
    