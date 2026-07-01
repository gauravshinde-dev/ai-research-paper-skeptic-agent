from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pdf_utils import extract_text
from skeptic_agent import analyze_paper
import shutil, json, datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    with open("temp.pdf", "wb") as f:
        shutil.copyfileobj(file.file, f)
    text = extract_text("temp.pdf")
    result = analyze_paper(text)
    log_entry = {"timestamp": str(datetime.datetime.now()), "filename": file.filename, "result": result}
    with open("logs.json", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    return result
