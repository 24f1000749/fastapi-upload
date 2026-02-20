from fastapi import FastAPI, File, UploadFile, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import csv
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

VALID_TOKEN = "db1o9jk20deqa1u9"
VALID_EXTENSIONS = {".csv", ".json", ".txt"}
MAX_SIZE = 56 * 1024  # 56KB
EMAIL = "24f1000749@ds.study.iitm.ac.in"


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    x_upload_token_3239: str = Header(default=None),
):
    # Authentication
    if x_upload_token_3239 != VALID_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # File type check
    filename = file.filename or ""
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in VALID_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Bad Request: invalid file type")

    # Read content
    content = await file.read()

    # File size check
    if len(content) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="Payload Too Large")

    # Parse CSV
    if ext == ".csv":
        text = content.decode("utf-8")
        reader = csv.DictReader(io.StringIO(text))
        rows = list(reader)
        columns = reader.fieldnames or []
        total_value = round(sum(float(r["value"]) for r in rows), 2)
        category_counts = {}
        for r in rows:
            cat = r["category"]
            category_counts[cat] = category_counts.get(cat, 0) + 1

        return {
            "email": EMAIL,
            "filename": filename,
            "rows": len(rows),
            "columns": list(columns),
            "totalValue": total_value,
            "categoryCounts": category_counts,
        }

    return {"email": EMAIL, "filename": filename}
