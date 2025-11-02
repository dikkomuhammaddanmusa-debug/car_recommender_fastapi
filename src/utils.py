import unicodedata
import re
from typing import Iterable, List, Tuple
from src.models import Car

def _normalize_model(name: str | None) -> str:
    if not name:
        return ""
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    s = s.lower().strip()
    s = re.sub(r"\s+", " ", s)
    return s

def dedup_cars(cars: Iterable[Car]) -> List[Car]:
    """
    Keep a single best Car per (brand, normalized_model, year), preferring lower mileage.
    """
    best: dict[Tuple[str, str, int], Car] = {}
    for c in cars:
        key = ((c.brand or "").lower(), _normalize_model(c.model), int(c.year or 0))
        if key not in best:
            best[key] = c
        else:
            cur = best[key]
            cur_m = float("inf") if cur.mileage is None else cur.mileage
            new_m = float("inf") if c.mileage is None else c.mileage
            if new_m < cur_m:
                best[key] = c
    return list(best.values())
