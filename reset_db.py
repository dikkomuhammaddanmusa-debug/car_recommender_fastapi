from src.database import Base, engine
from src.models import Car, Upload, SearchLog
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print("Dropped and recreated tables.")
