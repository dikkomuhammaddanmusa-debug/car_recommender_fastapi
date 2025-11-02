import os
import math
import pandas as pd
from src.database import Base, engine, session_scope
from src.models import Car

Base.metadata.create_all(bind=engine)

csv_path = os.path.join("data", "cars_enhanced.csv")
if not os.path.exists(csv_path):
    print("No CSV found at data/cars_enhanced.csv. Skipping seed.")
    raise SystemExit(0)

df = pd.read_csv(csv_path)

def coalesce_price(row):
    for k in ("price_usd_final", "price_usd_est", "price_model", "price"):
        v = row.get(k)
        if pd.notna(v):
            try:
                return float(v)
            except Exception:
                try:
                    return float(str(v).replace(",", "").strip())
                except Exception:
                    continue
    return None

def norm_trans(x):
    if pd.isna(x): return None
    s = str(x).strip().lower()
    if s in {"a", "auto", "automatic", "at"}: return "Automatic"
    if s in {"m", "man", "manual", "mt"}: return "Manual"
    if "auto" in s: return "Automatic"
    if "man" in s: return "Manual"
    return str(x)

def derive_model(row):
    if pd.notna(row.get("name")) and str(row["name"]).strip():
        return str(row["name"]).strip()
    if pd.notna(row.get("car_type")) and str(row["car_type"]).strip():
        return str(row["car_type"]).strip()
    return None

norm = pd.DataFrame()
norm["brand"]        = df.get("brand")
norm["model"]        = df.apply(derive_model, axis=1)
norm["year"]         = df.get("year")
norm["price"]        = df.apply(coalesce_price, axis=1)
norm["mileage"]      = df.get("mileage")
norm["transmission"] = df.get("trans").map(norm_trans) if "trans" in df.columns else df.get("transmission")
norm["fuel"]         = df.get("fuel")
norm["image_url"]    = None  # not present in CSV

norm = norm[norm["brand"].notna() & norm["year"].notna()].copy()

with session_scope() as db:
    if db.query(Car).count() == 0:
        rows = []
        for rec in norm.to_dict(orient="records"):
            clean = {k: (None if (isinstance(v, float) and math.isnan(v)) else v) for k, v in rec.items()}
            rows.append(Car(**clean))
        db.add_all(rows)
        print(f"Seeded {len(rows)} cars (normalized).")
    else:
        print("Cars table already has data; skipping seed.")
