from fastapi import Depends

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

from src.config import settings

DB_URL = settings.SQLALCHEMY_DATABASE_URL
engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db

    finally:
        db.close()


async def save(instance: object, db: SessionLocal = Depends(get_db)) -> None:
    db.add(instance)
    db.commit()
    db.refresh(instance)