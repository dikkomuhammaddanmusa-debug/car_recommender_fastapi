from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.database import get_db
from src.models import Car

router = APIRouter(prefix="/api/v1", tags=["recommend"])

@router.get("/recommend")
def recommend(limit: int = 20, db: Session = Depends(get_db)):
    q = db.query(Car).order_by(Car.year.desc(), Car.price.asc())
    cars = q.limit(min(limit, 100)).all()
    return [
        {
            "id": c.id,
            "brand": c.brand,
            "model": c.model,
            "year": c.year,
            "price": c.price,
            "mileage": c.mileage,
            "display_name": c.display_name,
            "image_url": getattr(c, "image_url", None),
        }
        for c in cars
    ]
