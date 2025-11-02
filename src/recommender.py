from typing import List, Dict
from src.models import Car

def _minmax(values):
    vmin, vmax = min(values), max(values)
    if vmax == vmin:
        return [0.5 for _ in values]
    return [(v - vmin) / (vmax - vmin) for v in values]

def rank_cars(cars: List[Car], weights: Dict[str, float]):
    if not cars:
        return []
    years = [c.year or 0 for c in cars]
    prices = [c.price or 0 for c in cars]
    mileages = [c.mileage or 0 for c in cars]

    y_norm = _minmax(years)      # higher better
    p_norm = _minmax(prices)     # lower better -> invert
    m_norm = _minmax(mileages)   # lower better -> invert

    inv = lambda xs: [1.0 - x for x in xs]
    p_norm = inv(p_norm)
    m_norm = inv(m_norm)

    w_year = float(weights.get("year", 0.4))
    w_price = float(weights.get("price", 0.3))
    w_mileage = float(weights.get("mileage", 0.3))

    scored = []
    for i, c in enumerate(cars):
        score = y_norm[i]*w_year + p_norm[i]*w_price + m_norm[i]*w_mileage
        scored.append((score, c))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored
