from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil, platform
app = FastAPI(title="Log Analysis Using GROK")

WrongFileException = HTTPException(status_code=400,detail="wrong file format: use only .txt or .log")

@app.get("/")
async def healthCheck():
    return {"Status":"Running", "Message":"Backend is running"}

@app.post("/upload")
async def upload_log(file: UploadFile = File(...)):
    if not file.filename.endswith(('.log','.txt')):
        raise WrongFileException
    
    try:
        content = await file.read()
        log_text = content.decode('utf-8')

        return{
            "filename":file.filename,
            "content_type":file.content_type,
            "size_bytes": len(content),
            "lines_count": len(log_text.splitlines()),
            "preview": log_text[:100]+"..."
        }
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"error reading file: {str(e)}")


@app.post("/clean_logs")
async def clean_log(file: UploadFile = File(...)):
    if not file.filename.endswith((".log",'.txt')):
        raise WrongFileException
    
    try:
        content = await file.read()
        log_text = content.decode('utf-8')
        lines = log_text.splitlines()
        errors = []
        for line in lines:
            if "ERROR" in line.upper():
                errors.append(line)

        return {
            "Content": errors
        }


    except Exception as e:
        raise HTTPException(status_code=500,detail=f"error reading file: {str(e)}")

@app.get('/system_check')
async def systemCheck():

    return {
        "os":platform.system(),
        "kernel version":platform.release(),
        "Architecture":platform.machine(),
        "network name":platform.node()
    }