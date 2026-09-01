from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import ApiResponse
from app.services.job_service import JobService
from app.dependencies.auth import get_current_recruiter
from app.models.recruiter import Recruiter

router = APIRouter(prefix="/recruiter", tags=["Recruiter Dashboard"])

@router.get("/dashboard", response_model=ApiResponse[dict])
def get_dashboard_data(
    recruiter: Recruiter = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """Get dashboard summary metrics and company status for recruiter."""
    service = JobService(db)
    summary = service.get_dashboard_summary(recruiter.company_id)
    return ApiResponse(
        success=True,
        data={
            "recruiter": {
                "id": recruiter.id,
                "designation": recruiter.designation,
                "user_name": recruiter.user.full_name if recruiter.user else ""
            },
            "metrics": summary
        },
        message="Dashboard metrics loaded successfully."
    )
