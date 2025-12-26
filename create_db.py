from db import Base, engine
from models import CarModel

Base.metadata.create_all(engine)
