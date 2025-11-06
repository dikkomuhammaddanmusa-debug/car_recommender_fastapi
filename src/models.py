from sqlalchemy import Column, Integer, String, Float
from src.database import Base

class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, index=True)
    model = Column(String, index=True)
    year = Column(Integer, index=True)
    price = Column(Float, index=True)
    mileage = Column(Integer, index=True)
    fuel = Column(String)
    transmission = Column(String)
    display_name = Column(String, index=True)
    image_url = Column(String, nullable=True)
