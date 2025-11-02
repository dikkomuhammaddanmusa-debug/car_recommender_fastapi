from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from src import models
from src.schemas import SearchFilters

def list_cars(
    db: Session,
    filters: SearchFilters,
    sort_by: str = "year",
    order: str = "desc",
    limit: int | None = None,
    offset: int = 0,
) -> List[models.Car]:
    stmt = select(models.Car)
    conds = []
    if filters.brand: conds.append(models.Car.brand.ilike(f"%{filters.brand}%"))
    if filters.transmission: conds.append(models.Car.transmission.ilike(f"%{filters.transmission}%"))
    if filters.fuel: conds.append(models.Car.fuel.ilike(f"%{filters.fuel}%"))
    if filters.min_year: conds.append(models.Car.year >= filters.min_year)
    if filters.max_year: conds.append(models.Car.year <= filters.max_year)
    if filters.min_price: conds.append(models.Car.price >= filters.min_price)
    if filters.max_price: conds.append(models.Car.price <= filters.max_price)
    if filters.max_mileage: conds.append(models.Car.mileage <= filters.max_mileage)
    if conds:
        stmt = stmt.where(and_(*conds))

    # Sorting
    sort_map = {
        "year": models.Car.year,
        "price": models.Car.price,
        "mileage": models.Car.mileage,
        "brand": models.Car.brand,
        "model": models.Car.model,
    }
    col = sort_map.get(sort_by, models.Car.year)
    stmt = stmt.order_by(col.asc() if str(order).lower() == "asc" else col.desc())

    # Pagination
    if limit is not None:
        stmt = stmt.offset(max(0, int(offset))).limit(max(1, int(limit)))

    return list(db.scalars(stmt))

def create_search_log(db: Session, query: str, filters: str, results_count: int) -> models.SearchLog:
    log = models.SearchLog(query=query, filters=filters, results_count=results_count)
    db.add(log)
    db.flush()
    return log
