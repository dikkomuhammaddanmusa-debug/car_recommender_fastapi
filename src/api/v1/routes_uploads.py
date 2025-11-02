import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from uuid import uuid4
from src.database import session_scope
from src.models import Upload

router = APIRouter()

UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in {".jpg", ".jpeg", ".png"}:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    fname = f"{uuid4().hex}{ext}"
    fpath = os.path.join(UPLOAD_DIR, fname)
    content = await file.read()
    with open(fpath, "wb") as f:
        f.write(content)

    with session_scope() as db:
        up = Upload(filename=file.filename, stored_path=fpath)
        db.add(up)
        db.flush()
        return {"id": up.id, "filename": up.filename, "stored_path": up.stored_path}
