from sqlalchemy import Column, Integer, String
from db import Base

class CarModel(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    license_plate = Column(String, unique=True)
    model = Column(String)
    km = Column(Integer)

    driver = Column(String, nullable=True)      # ← חדש
    status = Column(String, default="Active")   # ← חדש
    category = Column(String, nullable=True)
    maintenance_last_km = Column(Integer, nullable=True)
    maintenance_interval_km = Column(Integer, nullable=True)
    maintenance_last_date = Column(String, nullable=True)
    maintenance_interval_days = Column(Integer, nullable=True)
