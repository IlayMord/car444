from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}

class Driver:
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return f"Driver: {self.name}"


class Car:
    def __init__(self, license_plate, model, km, status="Active", driver=None):
        self.license_plate = license_plate
        self.model = model
        self.km = km
        self.status = status
        self.driver = driver   # Driver object or None

    def update_km(self, km):
        if km < self.km:
            raise ValueError("km cannot decrease")
        if km <= 0:
            raise ValueError("km must be positive")
        self.km = km
    
    def mark_in_repair(self):
        self.status = "In Repair"

    def mark_active(self):
        self.status = "Active"

    def assign_driver(self, driver):
        """Assign a driver object"""
        self.driver = driver

    def remove_driver(self):
        self.driver = None

    def __str__(self):
        driver_name = self.driver.name if self.driver else "No driver assigned"
        return f"{self.model} ({self.license_plate}) - {driver_name}"


class Fleet:
    def __init__(self):
        self.cars = []

    def add_car(self, car):
        self.cars.append(car)
    
    def remove_car(self, license_plate):
        self.cars = [c for c in self.cars if c.license_plate != license_plate]

    def find_car(self, license_plate):
        for car in self.cars:
            if car.license_plate == license_plate:
                return car
        return None
    
    def list_cars(self):
        return self.cars
