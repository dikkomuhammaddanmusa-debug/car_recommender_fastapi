from sqlalchemy import Column, Integer, String, Float
from src.database import Base

class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, index=True)
    model = Column(String, index=True)
    year = Column(Integer, index=True)
    price = Column(Float, index=True)
    mileage = Column(Float, index=True)
    transmission = Column(String, index=True)
    fuel = Column(String, index=True)
    image_url = Column(String, nullable=True)

class Upload(Base):
    __tablename__ = "uploads"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    stored_path = Column(String)

class SearchLog(Base):
    __tablename__ = "search_logs"
    id = Column(Integer, primary_key=True, index=True)
    query = Column(String)
    filters = Column(String)
    results_count = Column(Integer)
