from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from src.database import init_db, SessionLocal
from src.models import Car

app = FastAPI(title="Car Recommender API")

origins = [
    "http://localhost:19006",
    "http://localhost:8081",
    "exp://", "exps://",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    init_db()
    db = SessionLocal()
    try:
        if db.query(Car).count() == 0:
            sample = [
                Car(brand="Mercedes-Benz", model="E350", year=2014, price=14500, mileage=98000, fuel="Petrol", transmission="Automatic", display_name="2014 Mercedes E350"),
                Car(brand="Toyota", model="Corolla", year=2016, price=9000, mileage=110000, fuel="Petrol", transmission="Automatic", display_name="2016 Toyota Corolla"),
                Car(brand="Honda", model="Civic", year=2018, price=12000, mileage=60000, fuel="Petrol", transmission="Automatic", display_name="2018 Honda Civic"),
            ]
            db.add_all(sample); db.commit()
    finally:
        db.close()

@app.get("/api/v1/health")
def health():
    return {"status": "ok"}

@app.get("/api/v1/debug/db")
def debug_db(db: Session = Depends(get_db)):
    try:
        count = db.query(Car).count()
        return {"ok": True, "cars": count}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.get("/api/v1/cars/search")
def search_cars(
    brand: str | None = Query(None),
    model: str | None = Query(None),
    year_min: int | None = Query(None, alias="yearMin"),
    year_max: int | None = Query(None, alias="yearMax"),
    limit: int = 50,
    db: Session = Depends(get_db),
):
    try:
        q = db.query(Car)
        if brand: q = q.filter(Car.brand.ilike(f"%{brand}%"))
        if model: q = q.filter(Car.model.ilike(f"%{model}%"))
        if year_min is not None: q = q.filter(Car.year >= year_min)
        if year_max is not None: q = q.filter(Car.year <= year_max)
        cars = q.limit(min(limit, 200)).all()
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
            } for c in cars
        ]
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/v1/recommend")
def recommend(limit: int = 20, db: Session = Depends(get_db)):
    try:
        cars = db.query(Car).order_by(Car.year.desc(), Car.price.asc()).limit(min(limit, 100)).all()
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
            } for c in cars
        ]
    except Exception as e:
        return {"error": str(e)}
