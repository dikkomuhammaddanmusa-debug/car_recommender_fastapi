from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.models import Car
router = APIRouter(prefix="/api/v1/debug", tags=["debug"])
@router.get("/db")
def db_status(db: Session = Depends(get_db)):
    try:
        return {"ok": True, "cars": db.query(Car).count()}
    except Exception as e:
        return {"ok": False, "error": str(e)}
