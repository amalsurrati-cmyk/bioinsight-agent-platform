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

from fastapi import FastAPI, UploadFile
import shutil
import os
from orchestrator import run_pipeline
from database import init_db, save_report, get_all_reports, get_report_by_id
from agents.section1_intake import detect_file_type

app = FastAPI()

os.makedirs("uploads", exist_ok=True)
init_db()

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
        file_type = detect_file_type(filepath)
        save_report(file.filename, file_type, report)
        return {"report": report}
    except Exception as e:
        return {"report": f"Sorry, this file couldn't be analyzed. Error: {str(e)}"}

@app.get("/history")
def history():
    return {"reports": get_all_reports()}

@app.get("/report/{report_id}")
def report(report_id: int):
    text = get_report_by_id(report_id)
    if text is None:
        return {"error": "Report not found"}
    return {"report": text}