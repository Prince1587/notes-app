import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Prefer a provided DB_PATH (for Render disk), else local sqlite file.
    db_path = os.getenv("DB_PATH", os.path.join(os.path.dirname(__file__), "data", "notes.db"))
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    DATABASE_URL = f"sqlite:///{db_path}"

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, echo=False, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)

class Base(DeclarativeBase):
    pass