from fastapi import FastAPI, UploadFile, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
import shutil
import os
import re
from orchestrator import run_pipeline
from database import init_db, save_report, get_all_reports, get_report_by_id
from agents.section1_intake import detect_file_type

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(status_code=429, content={"report": "Too many requests. Please wait a moment and try again."})

os.makedirs("uploads", exist_ok=True)
init_db()

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

def sanitize_filename(filename):
    filename = os.path.basename(filename)
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    return filename

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
@limiter.limit("5/minute")
async def analyze(request: Request, file: UploadFile):
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        return {"report": "File too large. Maximum size is 10MB."}

    safe_filename = sanitize_filename(file.filename)
    filepath = f"uploads/{safe_filename}"
    with open(filepath, "wb") as buffer:
        buffer.write(contents)

    try:
        report = run_pipeline(filepath)
        file_type = detect_file_type(filepath)
        save_report(safe_filename, file_type, report)
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