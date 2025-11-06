from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import init_db, SessionLocal
from src.api.v1.cars import router as cars_router
from src.api.v1.recommend import router as recommend_router
from src.api.v1.debug import router as debug_router
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
            db.add_all(sample)
            db.commit()
    finally:
        db.close()

@app.get("/api/v1/health")
def health():
    return {"status": "ok"}

app.include_router(cars_router)
app.include_router(recommend_router)
app.include_router(debug_router)
