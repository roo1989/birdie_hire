import os
from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


def get_engine():
    """
    Creates and returns a sync SQLAlchemy engine for the Postgres database.
    """
    database_url = os.getenv(
        "DATABASE_URL", "postgresql://user:password@localhost:5432/db"
    )

    engine = create_engine(database_url, pool_pre_ping=True)
    return engine

_engine = get_engine()
SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False)

def get_db() -> Generator[Session, Any, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
