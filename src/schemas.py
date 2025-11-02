from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class CarBase(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    price: Optional[float] = None
    mileage: Optional[float] = None
    transmission: Optional[str] = None
    fuel: Optional[str] = None
    image_url: Optional[str] = None

class CarOut(CarBase):
    id: int
    class Config:
        from_attributes = True

class SearchFilters(BaseModel):
    brand: Optional[str] = None
    transmission: Optional[str] = None
    fuel: Optional[str] = None
    min_year: Optional[int] = None
    max_year: Optional[int] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    max_mileage: Optional[float] = None

class RecommendRequest(BaseModel):
    filters: SearchFilters = Field(default_factory=SearchFilters)
    top_k: int = 10
    weights: Dict[str, float] = Field(default_factory=lambda: {
        "year": 0.4,    # higher better
        "price": 0.3,   # lower better
        "mileage": 0.3  # lower better
    })

class UploadOut(BaseModel):
    id: int
    filename: str
    stored_path: str
    class Config:
        from_attributes = True
