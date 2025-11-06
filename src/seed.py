import os, csv
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src import models

CSV_PATHS = [
    os.path.join(os.path.dirname(__file__), "..", "data", "cars_enhanced.csv"),
    os.path.join(os.path.dirname(__file__), "data", "cars_enhanced.csv"),
]

def maybe_seed(max_rows=1000):
    db: Session = SessionLocal()
    try:
        if db.query(models.Car).count() > 0:
            return
        csv_path = next((p for p in CSV_PATHS if os.path.exists(p)), None)
        if not csv_path:
            return
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            batch = []
            for i, r in enumerate(reader):
                car = models.Car(
                    brand=r.get("brand"),
                    model=r.get("model"),
                    year=int(r.get("year", 0) or 0),
                    price=float(r.get("price", 0) or 0),
                    mileage=int(r.get("mileage", 0) or 0),
                    fuel=r.get("fuel"),
                    transmission=r.get("transmission"),
                    display_name=r.get("display_name"),
                    image_url=r.get("image_url"),
                )
                batch.append(car)
                if len(batch) >= 1000:
                    db.add_all(batch); db.commit(); batch.clear()
                if i + 1 >= max_rows:
                    break
            if batch:
                db.add_all(batch); db.commit()
    finally:
        db.close()
