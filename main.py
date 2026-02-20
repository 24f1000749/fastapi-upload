from fastapi import FastAPI, File, UploadFile, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import os

app = FastAPI(title="SecureUpload Data Processor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # ← CHANGED
    allow_methods=["*"],      # ← CHANGED (was ["POST", "GET"])
    allow_headers=["*"],
)


SECRET_TOKEN = "db1o9jk20deqa1u9"

@app.get("/")
async def root():
    return {"message": "SecureUpload API - POST to /upload with file field"}

@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    x_upload_token_3239: str = Header(None)
):
    if not x_upload_token_3239 or x_upload_token_3239 != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized - Invalid token")
    
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in {'.csv', '.json', '.txt'}:
        raise HTTPException(status_code=400, detail="Bad Request - Invalid file type")
    
    contents = await file.read()
    if len(contents) > 56 * 1024:
        raise HTTPException(status_code=413, detail="Payload Too Large")
    
    file.file.seek(0)
    
    if file_ext != '.csv':
        return {"message": f"File '{file.filename}' validated (non-CSV)"}
    
    df = pd.read_csv(io.BytesIO(contents))
    
    return {
        "email": "24f1000749@ds.study.iitm.ac.in",
        "filename": file.filename,
        "rows": len(df),
        "columns": df.columns.tolist(),
        "totalValue": round(float(df['value'].sum()), 2),
        "categoryCounts": df['category'].value_counts().to_dict()
    }
