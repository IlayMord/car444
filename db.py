import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "fleet.db")
engine = create_engine(
    f"sqlite:///{DB_PATH}",
    echo=True,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
