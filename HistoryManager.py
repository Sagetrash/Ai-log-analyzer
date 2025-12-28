import os, json
from pathlib import Path
from json import JSONDecodeError

async def appendHistory(inDict: dict,filename: str):
    history = []
    if os.path.exists(filename):
        try:
            with open(filename,'r') as f:
                history = json.load(f)
        except JSONDecodeError:
            history = []

    history.append(inDict)

    with open(filename,'w') as f:
        json.dump(history,f,indent=4)

async def displayHistory(filename:str):
    if os.path.exists(filename):
        try:
            with open(filename,'r') as f:
                history = json.load(f)
        except JSONDecodeError:
            print(f"error opening file {filename}")
        except FileNotFoundError:
            print(f"couldnt find the file {filename}")
    return history