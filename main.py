from fastapi import FastAPI, UploadFile
import shutil
import os
from orchestrator import run_pipeline

app = FastAPI()

os.makedirs("uploads", exist_ok=True)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze(file: UploadFile):
    filepath = f"uploads/{file.filename}"
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        report = run_pipeline(filepath)
        return {"report": report}
    except Exception as e:
        return {"report": f"Sorry, this file couldn't be analyzed. Error: {str(e)}"}