from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import ApiResponse, RecruiterLoginRequest, TokenResponse
from app.schemas.company import CompanyResponse
from app.schemas.job import JobResponse
from app.schemas.skill import SkillCreateRequest, SkillUpdateRequest, SkillResponse
from app.schemas.admin import (
    AdminDashboardMetrics, CompanyVerifyRequest, CompanyRejectRequest, JobModerateRequest,
    UserManagementResponse, UserStatusUpdateRequest, UserRoleUpdateRequest,
    FlaggedActivityResponse, FlagResolveRequest, AnalyticsOverviewResponse
)
from app.models.company import VerificationStatus
from app.models.job import ModerationStatus
from app.models.user import User, UserRole
from app.models.admin import FlagStatus
from app.services.admin_service import AdminService
from app.services.skill_service import SkillService
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token
from app.dependencies.auth import get_current_admin

router = APIRouter(prefix="/admin", tags=["Admin Module"])

# Admin Auth Endpoint
@router.post("/auth/login", response_model=ApiResponse[TokenResponse])
def admin_login(req: RecruiterLoginRequest, db: Session = Depends(get_db)):
    """Authenticate administrator account."""
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(req.email)
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials."
        )
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Only Administrator accounts can log in here."
        )
    token = create_access_token(data={"sub": user.id, "role": user.role.value})
    return ApiResponse(
        success=True,
        data=TokenResponse(
            access_token=token,
            user_id=user.id,
            email=user.email,
            full_name=user.full_name,
            role=user.role.value,
            company_id="",
            company_name="Platform Administration",
            company_verification_status="VERIFIED"
        ),
        message="Admin login successful."
    )

# Dashboard Metrics
@router.get("/dashboard", response_model=ApiResponse[AdminDashboardMetrics])
def get_dashboard_metrics(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Retrieve platform-wide administration metrics."""
    service = AdminService(db)
    metrics = service.get_dashboard_metrics()
    return ApiResponse(success=True, data=metrics, message="Metrics loaded.")

# --- FEATURE 36: USER MANAGEMENT ---
@router.get("/users", response_model=ApiResponse[dict])
def list_users(
    role: Optional[UserRole] = Query(None),
    is_active: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """List platform user accounts with role & active status filters."""
    service = AdminService(db)
    users, total = service.get_users(role=role, is_active=is_active, search=search, page=page, page_size=page_size)
    return ApiResponse(
        success=True,
        data={
            "users": [u.model_dump() for u in users],
            "pagination": {"total": total, "page": page, "page_size": page_size}
        },
        message="Users list loaded."
    )

@router.patch("/users/{user_id}/status", response_model=ApiResponse[UserManagementResponse])
def update_user_status(
    user_id: str,
    req: UserStatusUpdateRequest,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Activate or suspend a user account."""
    service = AdminService(db)
    updated = service.update_user_status(admin.id, user_id, req)
    action_text = "activated" if req.is_active else "suspended"
    return ApiResponse(
        success=True,
        data=updated,
        message=f"User account '{updated.email}' has been {action_text}."
    )

@router.patch("/users/{user_id}/role", response_model=ApiResponse[UserManagementResponse])
def update_user_role(
    user_id: str,
    req: UserRoleUpdateRequest,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update user role (STUDENT, RECRUITER, ADMIN)."""
    service = AdminService(db)
    updated = service.update_user_role(admin.id, user_id, req)
    return ApiResponse(
        success=True,
        data=updated,
        message=f"User '{updated.email}' role updated to {req.role.value}."
    )

# --- FEATURE 37: RECRUITER VERIFICATION ---
@router.get("/companies/pending", response_model=ApiResponse[dict])
def get_pending_verifications(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """List all recruiter company registrations pending verification."""
    service = AdminService(db)
    companies, total = service.get_pending_companies(page=page, page_size=page_size)
    return ApiResponse(
        success=True,
        data={
            "companies": [c.model_dump() for c in companies],
            "pagination": {"total": total, "page": page, "page_size": page_size}
        },
        message="Pending company verifications loaded."
    )

@router.get("/companies", response_model=ApiResponse[dict])
def get_all_companies(
    status: Optional[VerificationStatus] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """List all platform companies with status filter & search."""
    service = AdminService(db)
    companies, total = service.get_all_companies(status=status, search=search, page=page, page_size=page_size)
    return ApiResponse(
        success=True,
        data={
            "companies": [c.model_dump() for c in companies],
            "pagination": {"total": total, "page": page, "page_size": page_size}
        },
        message="Companies retrieved."
    )

@router.patch("/companies/{company_id}/verify", response_model=ApiResponse[CompanyResponse])
def verify_company(
    company_id: str,
    req: CompanyVerifyRequest,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Approve recruiter company verification request (Status -> VERIFIED)."""
    service = AdminService(db)
    verified = service.verify_company(company_id, req)
    return ApiResponse(
        success=True,
        data=verified,
        message=f"Company '{verified.name}' has been officially verified."
    )

@router.patch("/companies/{company_id}/reject", response_model=ApiResponse[CompanyResponse])
def reject_company(
    company_id: str,
    req: CompanyRejectRequest,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Reject recruiter company verification request with feedback notes."""
    service = AdminService(db)
    rejected = service.reject_company(company_id, req)
    return ApiResponse(
        success=True,
        data=rejected,
        message="Company verification request rejected."
    )

# --- FEATURE 38: JOB MODERATION ---
@router.get("/jobs/moderation", response_model=ApiResponse[dict])
def get_jobs_for_moderation(
    status: Optional[ModerationStatus] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Retrieve job postings for admin moderation and policy inspection."""
    service = AdminService(db)
    jobs, total = service.get_jobs_for_moderation(status=status, search=search, page=page, page_size=page_size)
    return ApiResponse(
        success=True,
        data={
            "jobs": [j.model_dump() for j in jobs],
            "pagination": {"total": total, "page": page, "page_size": page_size}
        },
        message="Jobs moderation queue loaded."
    )

@router.patch("/jobs/{job_id}/moderate", response_model=ApiResponse[JobResponse])
def moderate_job(
    job_id: str,
    req: JobModerateRequest,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Moderate job requisition (Approve, Flag for Revision, or Take Down)."""
    service = AdminService(db)
    job = service.moderate_job(job_id, req)
    return ApiResponse(
        success=True,
        data=job,
        message=f"Job moderation status updated to '{job.moderation_status.value}'."
    )

# --- FEATURE 39: SKILL LIBRARY MANAGEMENT ---
@router.get("/skills", response_model=ApiResponse[dict])
def list_skills(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """List skills in the centralized Skill Library taxonomy (Public / Admin)."""
    service = SkillService(db)
    skills, total = service.list_skills(search=search, category=category, page=page, page_size=page_size)
    return ApiResponse(
        success=True,
        data={
            "skills": [s.model_dump() for s in skills],
            "pagination": {"total": total, "page": page, "page_size": page_size}
        },
        message="Skills library retrieved."
    )

@router.post("/skills", response_model=ApiResponse[SkillResponse], status_code=status.HTTP_201_CREATED)
def create_skill(
    req: SkillCreateRequest,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Add a new skill to the central Skill Library."""
    service = SkillService(db)
    skill = service.create_skill(req)
    return ApiResponse(
        success=True,
        data=skill,
        message=f"Skill '{skill.name}' added to library."
    )

@router.put("/skills/{skill_id}", response_model=ApiResponse[SkillResponse])
def update_skill(
    skill_id: str,
    req: SkillUpdateRequest,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update skill taxonomy details."""
    service = SkillService(db)
    skill = service.update_skill(skill_id, req)
    return ApiResponse(
        success=True,
        data=skill,
        message=f"Skill '{skill.name}' updated."
    )

@router.delete("/skills/{skill_id}", response_model=ApiResponse[dict])
def delete_skill(
    skill_id: str,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete a skill from the Skill Library."""
    service = SkillService(db)
    service.delete_skill(skill_id)
    return ApiResponse(
        success=True,
        data={"id": skill_id},
        message="Skill deleted from library."
    )

# --- FEATURE 40: PLATFORM ANALYTICS ---
@router.get("/analytics/overview", response_model=ApiResponse[AnalyticsOverviewResponse])
def get_analytics_overview(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Retrieve executive platform analytics telemetry metrics."""
    service = AdminService(db)
    analytics = service.get_analytics_overview()
    return ApiResponse(
        success=True,
        data=analytics,
        message="Analytics telemetry overview loaded."
    )

# --- FEATURE 41: FLAGGED ACTIVITY QUEUE ---
@router.get("/flagged-queue", response_model=ApiResponse[dict])
def get_flagged_activities(
    status: Optional[FlagStatus] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Retrieve flagged activity reports queue."""
    service = AdminService(db)
    flags, total = service.get_flagged_activities(status_enum=status, page=page, page_size=page_size)
    return ApiResponse(
        success=True,
        data={
            "flagged_activities": [f.model_dump() for f in flags],
            "pagination": {"total": total, "page": page, "page_size": page_size}
        },
        message="Flagged activity queue loaded."
    )

@router.patch("/flagged-queue/{flag_id}/resolve", response_model=ApiResponse[FlaggedActivityResponse])
def resolve_flagged_activity(
    flag_id: str,
    req: FlagResolveRequest,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Resolve flagged activity report (Warning Issued, Suspended, or Dismissed)."""
    service = AdminService(db)
    resolved = service.resolve_flagged_activity(admin.id, flag_id, req)
    return ApiResponse(
        success=True,
        data=resolved,
        message=f"Flagged activity report status updated to '{resolved.status.value}'."
    )
