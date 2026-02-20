from fastapi import FastAPI, File, UploadFile, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import os

app = FastAPI()

# FIXED CORS - EXACT ASSIGNMENT REQUIREMENTS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_TOKEN = "db1o9jk20deqa1u9"

@app.get("/")
async def root():
    return {"message": "SecureUpload API ready"}

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    x_upload_token_3239: str = Header(...)
):
    if x_upload_token_3239 != SECRET_TOKEN:
        raise HTTPException(401, "Unauthorized")
    
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in {'.csv', '.json', '.txt'}:
        raise HTTPException(400, "Bad Request")
    
    contents = await file.read()
    if len(contents) > 56*1024:
        raise HTTPException(413, "Payload Too Large")
    
    if file_ext != '.csv':
        return {"message": "validated"}
    
    df = pd.read_csv(io.BytesIO(contents))
    return {
        "email": "24f1000749@ds.study.iitm.ac.in",
        "filename": file.filename,
        "rows": len(df),
        "columns": df.columns.tolist(),
        "totalValue": round(df['value'].sum(), 2),
        "categoryCounts": df['category'].value_counts().to_dict()
    }
