from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import ApiResponse
from app.schemas.job import JobCreateRequest, JobUpdateRequest, JobResponse, JobListFilter
from app.models.job import JobStatus, EmploymentType, WorkMode
from app.services.job_service import JobService
from app.dependencies.auth import get_current_recruiter
from app.models.recruiter import Recruiter

router = APIRouter(prefix="/recruiter/jobs", tags=["Jobs Management"])

@router.get("", response_model=ApiResponse[dict])
def list_jobs(
    search: Optional[str] = Query(None, description="Search by title or description"),
    status: Optional[JobStatus] = Query(None, description="Filter by status"),
    employment_type: Optional[EmploymentType] = Query(None, description="Filter by employment type"),
    work_mode: Optional[WorkMode] = Query(None, description="Filter by work mode"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    recruiter: Recruiter = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """Retrieve recruiter's company jobs with search and filter parameters."""
    service = JobService(db)
    filter_params = JobListFilter(
        search=search,
        status=status,
        employment_type=employment_type,
        work_mode=work_mode,
        page=page,
        page_size=page_size
    )
    jobs, total = service.list_jobs(recruiter.company_id, filter_params)
    return ApiResponse(
        success=True,
        data={
            "jobs": [j.model_dump() for j in jobs],
            "pagination": {
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": (total + page_size - 1) // page_size if total > 0 else 0
            }
        },
        message="Jobs retrieved successfully."
    )

@router.post("", response_model=ApiResponse[JobResponse], status_code=status.HTTP_201_CREATED)
def create_job(
    req: JobCreateRequest,
    publish: bool = Query(False, description="Set to true to publish directly (requires verified company)"),
    recruiter: Recruiter = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """Create a new job posting for the recruiter's company."""
    service = JobService(db)
    created_job = service.create_job(recruiter.id, recruiter.company_id, req, publish_immediately=publish)
    status_msg = "published successfully." if publish else "saved as draft."
    return ApiResponse(
        success=True,
        data=created_job,
        message=f"Job '{created_job.title}' {status_msg}"
    )

@router.get("/{job_id}", response_model=ApiResponse[JobResponse])
def get_job_details(
    job_id: str,
    recruiter: Recruiter = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """Get full details of a specific job owned by recruiter's company."""
    service = JobService(db)
    job_details = service.get_job_details(job_id, recruiter.company_id)
    return ApiResponse(
        success=True,
        data=job_details,
        message="Job details retrieved."
    )

@router.put("/{job_id}", response_model=ApiResponse[JobResponse])
def update_job(
    job_id: str,
    req: JobUpdateRequest,
    recruiter: Recruiter = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """Update job posting details."""
    service = JobService(db)
    updated_job = service.update_job(job_id, recruiter.company_id, req)
    return ApiResponse(
        success=True,
        data=updated_job,
        message="Job updated successfully."
    )

@router.patch("/{job_id}/publish", response_model=ApiResponse[JobResponse])
def publish_job(
    job_id: str,
    recruiter: Recruiter = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """Publish a draft or paused job (Requires VERIFIED company status)."""
    service = JobService(db)
    published_job = service.publish_job(job_id, recruiter.company_id)
    return ApiResponse(
        success=True,
        data=published_job,
        message="Job published successfully."
    )

@router.patch("/{job_id}/pause", response_model=ApiResponse[JobResponse])
def pause_job(
    job_id: str,
    recruiter: Recruiter = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """Pause an active published job."""
    service = JobService(db)
    paused_job = service.pause_job(job_id, recruiter.company_id)
    return ApiResponse(
        success=True,
        data=paused_job,
        message="Job paused."
    )

@router.patch("/{job_id}/close", response_model=ApiResponse[JobResponse])
def close_job(
    job_id: str,
    recruiter: Recruiter = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """Close a job posting."""
    service = JobService(db)
    closed_job = service.close_job(job_id, recruiter.company_id)
    return ApiResponse(
        success=True,
        data=closed_job,
        message="Job closed."
    )

@router.delete("/{job_id}", response_model=ApiResponse[dict])
def delete_job(
    job_id: str,
    recruiter: Recruiter = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """Delete a DRAFT job posting."""
    service = JobService(db)
    service.delete_job(job_id, recruiter.company_id)
    return ApiResponse(
        success=True,
        data={"id": job_id},
        message="Job deleted successfully."
    )
