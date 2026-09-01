from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import ApiResponse
from app.schemas.company import CompanyResponse, CompanyUpdateRequest
from app.services.company_service import CompanyService
from app.dependencies.auth import get_current_recruiter
from app.models.recruiter import Recruiter

router = APIRouter(prefix="/recruiter/company", tags=["Company Profile"])

@router.get("", response_model=ApiResponse[CompanyResponse])
def get_company_profile(
    recruiter: Recruiter = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """Get the authenticated recruiter's company profile."""
    service = CompanyService(db)
    company_data = service.get_company(recruiter.company_id)
    return ApiResponse(
        success=True,
        data=company_data,
        message="Company profile retrieved."
    )

@router.put("", response_model=ApiResponse[CompanyResponse])
def update_company_profile(
    req: CompanyUpdateRequest,
    recruiter: Recruiter = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """Update the authenticated recruiter's company profile details."""
    service = CompanyService(db)
    updated_company = service.update_company(recruiter.company_id, req)
    return ApiResponse(
        success=True,
        data=updated_company,
        message="Company profile updated successfully."
    )
