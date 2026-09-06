"""
database.py — SQLAlchemy engine + session factory + declarative Base.

All models import Base from here; database.py never imports from models
to keep the dependency graph acyclic.

SQLAlchemy version: 1.4.x (sync, no greenlet required on Windows)
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/careerpilot",
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,           # cheaply check connection health before use
    pool_size=10,
    max_overflow=20,
    echo=False,                    # set True for SQL query logging in dev
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    FastAPI dependency that yields a database session and guarantees closure.

    Usage:
        @router.get("/")
        def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    """
    Create all tables whose models are registered on Base.
    Called once at application startup (see main.py lifespan).
    Requires the uuid-ossp PostgreSQL extension for gen_random_uuid().
    """
    with engine.connect() as conn:
        # Enable uuid-ossp so PostgreSQL can generate UUIDs server-side.
        conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
        conn.commit()

    Base.metadata.create_all(bind=engine)
