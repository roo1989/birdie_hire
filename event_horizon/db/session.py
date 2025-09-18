import os

from sqlalchemy import create_engine


def get_engine():
    """
    Creates and returns a sync SQLAlchemy engine for the Postgres database.
    """
    database_url = os.getenv(
        "DATABASE_URL", "postgresql://user:password@localhost:5432/db"
    )

    engine = create_engine(database_url, pool_pre_ping=True)
    return engine
