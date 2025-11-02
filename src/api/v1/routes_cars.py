from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from src.database import session_scope
from src.schemas import CarOut, SearchFilters, RecommendRequest
from src.crud import list_cars, create_search_log
from src.recommender import rank_cars
from src.utils import dedup_cars

router = APIRouter()

def get_db():
    with session_scope() as s:
        yield s

@router.get("/search", response_model=List[CarOut])
def search_cars(
    brand: str | None = None,
    transmission: str | None = None,
    fuel: str | None = None,
    min_year: int | None = None,
    max_year: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    max_mileage: float | None = None,
    # pagination + sorting
    limit: int = 20,
    offset: int = 0,
    sort: str = "year",   # year|price|mileage|brand|model
    order: str = "desc",  # asc|desc
    # NEW: optional dedup for search
    dedup: bool = False,
    db: Session = Depends(get_db),
):
    limit = max(1, min(limit, 100))
    offset = max(0, offset)
    if sort not in {"year","price","mileage","brand","model"}:
        sort = "year"
    if order.lower() not in {"asc","desc"}:
        order = "desc"

    filters = SearchFilters(
        brand=brand, transmission=transmission, fuel=fuel,
        min_year=min_year, max_year=max_year, min_price=min_price,
        max_price=max_price, max_mileage=max_mileage,
    )
    cars = list_cars(db, filters, sort_by=sort, order=order.lower(), limit=limit, offset=offset)
    if dedup:
        cars = dedup_cars(cars)
    create_search_log(db, query="/search", filters=filters.model_dump_json(), results_count=len(cars))
    return cars

@router.post("/recommend", response_model=List[CarOut])
def recommend(req: RecommendRequest, db: Session = Depends(get_db)):
    # Fetch ALL matches (no pagination), then dedup + rank
    cars = list_cars(db, req.filters, limit=None)
    cars = dedup_cars(cars)          # ensure duplicates collapsed
    ranked = rank_cars(cars, req.weights)
    topk = [c for _, c in ranked[: req.top_k]]
    create_search_log(db, query="/recommend", filters=req.model_dump_json(), results_count=len(topk))
    return topk
