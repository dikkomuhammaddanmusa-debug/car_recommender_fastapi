from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.database import get_db
from src.models import Car

router = APIRouter(prefix="/api/v1/cars", tags=["cars"])

@router.get("/search")
def search_cars(
    brand: str | None = Query(None),
    model: str | None = Query(None),
    year_min: int | None = Query(None, alias="yearMin"),
    year_max: int | None = Query(None, alias="yearMax"),
    limit: int = 50,
    db: Session = Depends(get_db),
):
    q = db.query(Car)
    if brand:
        q = q.filter(Car.brand.ilike(f"%{brand}%"))
    if model:
        q = q.filter(Car.model.ilike(f"%{model}%"))
    if year_min is not None:
        q = q.filter(Car.year >= year_min)
    if year_max is not None:
        q = q.filter(Car.year <= year_max)
    return [ 
        {
            "id": c.id,
            "brand": c.brand,
            "model": c.model,
            "year": c.year,
            "price": c.price,
            "mileage": c.mileage,
            "fuel": c.fuel,
            "transmission": c.transmission,
            "display_name": c.display_name,
            "image_url": getattr(c, "image_url", None),
        }
        for c in q.limit(min(limit, 200)).all()
    ]
