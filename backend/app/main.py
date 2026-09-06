"""
main.py — FastAPI application entry point for CareerPilot-AI backend.

Branch: feature/sid-recruiter-payments
Scope:  Recruiter Module + Payment & Subscription Module
        (currently: Notification Management + User Management)

Run in development:
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Swagger UI: http://localhost:8000/docs
ReDoc:      http://localhost:8000/redoc

Stack: FastAPI 0.103.x, SQLAlchemy 1.4.x, Pydantic 1.10.x
"""

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# Import models so that Base.metadata is populated before create_tables().
import app.models  # noqa: F401, E402  (side-effect import)

from app.database import create_tables  # noqa: E402
from app.routes import notifications, users  # noqa: E402


# ---------------------------------------------------------------------------
# Lifespan — runs once on startup and once on shutdown
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on startup (idempotent via CREATE IF NOT EXISTS)."""
    create_tables()
    yield
    # Clean-up logic can go here (e.g. flush caches, close connections).


# ---------------------------------------------------------------------------
# App instance
# ---------------------------------------------------------------------------
app = FastAPI(
    title="CareerPilot-AI API",
    description=(
        "Backend API for the CareerPilot-AI platform. "
        "This service owns the Recruiter Module and Payment & Subscription Module."
    ),
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# ---------------------------------------------------------------------------
# CORS — allow the Vue dev server (and future production origins)
# ---------------------------------------------------------------------------
raw_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173")
allowed_origins: list = [o.strip() for o in raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(notifications.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")


# ---------------------------------------------------------------------------
# Health-check
# ---------------------------------------------------------------------------
@app.get("/health", tags=["Health"])
def health_check() -> dict:
    """Simple liveness probe used by load balancers and monitoring."""
    return {"status": "ok", "service": "careerpilot-ai-backend"}
