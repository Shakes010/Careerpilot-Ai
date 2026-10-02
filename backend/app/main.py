from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

# Import Routers
from app.routers import (
    auth_router,
    profile_router,
    skills_router,
    assessments_router,
    opportunities_router,
    projects_router,
    admin_router,
    recruiter_router,
    payments_router
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="CareerPilot AI Full-Stack Platform API",
    version="1.0.0"
)

# CORS setup for Vue dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_router.router)
app.include_router(profile_router.router)
app.include_router(skills_router.router)
app.include_router(assessments_router.router)
app.include_router(opportunities_router.router)
app.include_router(projects_router.router)
app.include_router(admin_router.router)
app.include_router(recruiter_router.router)
app.include_router(payments_router.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to CareerPilot AI Platform API",
        "status": "online",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
