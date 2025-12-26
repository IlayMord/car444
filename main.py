import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import text
from db import SessionLocal, engine
from models import Base, CarModel

app = FastAPI()

# Ensure tables exist on startup (avoids missing table errors)
Base.metadata.create_all(bind=engine)

def ensure_columns():
    with engine.connect() as conn:
        result = conn.execute(text("PRAGMA table_info(cars)")).mappings().all()
        existing = {row["name"] for row in result}
        columns = {
            "category": "TEXT",
            "maintenance_last_km": "INTEGER",
            "maintenance_interval_km": "INTEGER",
            "maintenance_last_date": "TEXT",
            "maintenance_interval_days": "INTEGER",
        }
        for name, col_type in columns.items():
            if name not in existing:
                conn.execute(text(f"ALTER TABLE cars ADD COLUMN {name} {col_type}"))
        conn.commit()

ensure_columns()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fronted")
app.mount("/app", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

@app.get("/")
def root():
    return RedirectResponse(url="/app/")

class Car(BaseModel):
    license_plate: str
    model: str
    km: int
    driver: Optional[str] = None
    status: str = "Active"
    category: Optional[str] = None
    maintenance_last_km: Optional[int] = None
    maintenance_interval_km: Optional[int] = None
    maintenance_last_date: Optional[str] = None
    maintenance_interval_days: Optional[int] = None

class MaintenanceUpdate(BaseModel):
    maintenance_last_km: Optional[int] = None
    maintenance_interval_km: Optional[int] = None
    maintenance_last_date: Optional[str] = None
    maintenance_interval_days: Optional[int] = None


@app.get("/cars")
def get_cars():
    db = SessionLocal()
    cars = db.query(CarModel).all()
    return [
        {
            "license_plate": c.license_plate,
            "model": c.model,
            "km": c.km,
            "driver": c.driver,
            "status": c.status,
            "category": c.category,
            "maintenance_last_km": c.maintenance_last_km,
            "maintenance_interval_km": c.maintenance_interval_km,
            "maintenance_last_date": c.maintenance_last_date,
            "maintenance_interval_days": c.maintenance_interval_days,
        }
        for c in cars
    ]


@app.post("/cars")
def add_car(car: Car):
    db = SessionLocal()

    new_car = CarModel(
        license_plate=car.license_plate,
        model=car.model,
        km=car.km,
        driver=car.driver,
        status=car.status,
        category=car.category,
        maintenance_last_km=car.maintenance_last_km,
        maintenance_interval_km=car.maintenance_interval_km,
        maintenance_last_date=car.maintenance_last_date,
        maintenance_interval_days=car.maintenance_interval_days,
    )

    db.add(new_car)
    db.commit()
    return {"status": "saved"}



@app.put("/cars/{license_plate}")
def update_km(license_plate: str, km: int):
    db = SessionLocal()
    car = db.query(CarModel).filter_by(license_plate=license_plate).first()

    if not car:
        raise HTTPException(404, "הרכב לא נמצא")

    if km < car.km:
        raise HTTPException(400, "אי אפשר להחזיר ק״מ אחורה")

    car.km = km
    db.commit()
    return {"status": "updated"}

@app.put("/cars/{license_plate}/driver")
def update_driver(license_plate: str, driver: str):
    db = SessionLocal()
    car = db.query(CarModel).filter_by(license_plate=license_plate).first()

    if not car:
        raise HTTPException(404, "הרכב לא נמצא")

    car.driver = driver
    db.commit()
    return {"status": "updated"}


@app.put("/cars/{license_plate}/status")
def update_status(license_plate: str, status: str):
    db = SessionLocal()
    car = db.query(CarModel).filter_by(license_plate=license_plate).first()

    if not car:
        raise HTTPException(404, "הרכב לא נמצא")

    car.status = status
    db.commit()
    return {"status": "updated"}

@app.put("/cars/{license_plate}/category")
def update_category(license_plate: str, category: str):
    db = SessionLocal()
    car = db.query(CarModel).filter_by(license_plate=license_plate).first()

    if not car:
        raise HTTPException(404, "הרכב לא נמצא")

    car.category = category
    db.commit()
    return {"status": "updated"}


@app.put("/cars/{license_plate}/maintenance")
def update_maintenance(license_plate: str, payload: MaintenanceUpdate):
    db = SessionLocal()
    car = db.query(CarModel).filter_by(license_plate=license_plate).first()

    if not car:
        raise HTTPException(404, "הרכב לא נמצא")

    car.maintenance_last_km = payload.maintenance_last_km
    car.maintenance_interval_km = payload.maintenance_interval_km
    car.maintenance_last_date = payload.maintenance_last_date
    car.maintenance_interval_days = payload.maintenance_interval_days
    db.commit()
    return {"status": "updated"}


@app.delete("/cars/{license_plate}")
def delete_car(license_plate: str):
    db = SessionLocal()
    car = db.query(CarModel).filter_by(license_plate=license_plate).first()

    if not car:
        raise HTTPException(404, "הרכב לא נמצא")

    db.delete(car)
    db.commit()
    return {"status": "deleted"}
