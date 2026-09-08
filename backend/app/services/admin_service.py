from typing import List, Tuple
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import UserRole
from app.models.company import VerificationStatus
from app.models.job import ModerationStatus
from app.models.admin import FlagStatus
from app.repositories.admin_repository import AdminRepository
from app.schemas.company import CompanyResponse
from app.schemas.job import JobResponse
from app.schemas.admin import (
    AdminDashboardMetrics, CompanyVerifyRequest, CompanyRejectRequest, JobModerateRequest,
    UserManagementResponse, UserStatusUpdateRequest, UserRoleUpdateRequest,
    FlaggedActivityResponse, FlagResolveRequest, AnalyticsOverviewResponse
)

class AdminService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = AdminRepository(db)

    # --- FEATURE 36: USER MANAGEMENT ---
    def get_users(self, role: UserRole = None, is_active: bool = None, search: str = None, page: int = 1, page_size: int = 20) -> Tuple[List[UserManagementResponse], int]:
        users, total = self.repo.get_users(role=role, is_active=is_active, search=search, page=page, page_size=page_size)
        return [UserManagementResponse.model_validate(u) for u in users], total

    def update_user_status(self, admin_id: str, user_id: str, req: UserStatusUpdateRequest) -> UserManagementResponse:
        updated = self.repo.update_user_status(user_id=user_id, is_active=req.is_active, admin_id=admin_id, notes=req.notes)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User account not found.")
        return UserManagementResponse.model_validate(updated)

    def update_user_role(self, admin_id: str, user_id: str, req: UserRoleUpdateRequest) -> UserManagementResponse:
        updated = self.repo.update_user_role(user_id=user_id, role=req.role, admin_id=admin_id)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User account not found.")
        return UserManagementResponse.model_validate(updated)

    # --- FEATURE 37 & 38: VERIFICATION & MODERATION ---
    def get_pending_companies(self, page: int = 1, page_size: int = 20) -> Tuple[List[CompanyResponse], int]:
        companies, total = self.repo.get_companies(status=VerificationStatus.PENDING, page=page, page_size=page_size)
        return [CompanyResponse.model_validate(c) for c in companies], total

    def get_all_companies(self, status: VerificationStatus = None, search: str = None, page: int = 1, page_size: int = 20) -> Tuple[List[CompanyResponse], int]:
        companies, total = self.repo.get_companies(status=status, search=search, page=page, page_size=page_size)
        return [CompanyResponse.model_validate(c) for c in companies], total

    def verify_company(self, company_id: str, req: CompanyVerifyRequest) -> CompanyResponse:
        company = self.repo.update_company_status(
            company_id=company_id,
            status=VerificationStatus.VERIFIED,
            notes=req.verification_notes
        )
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found.")
        return CompanyResponse.model_validate(company)

    def reject_company(self, company_id: str, req: CompanyRejectRequest) -> CompanyResponse:
        company = self.repo.update_company_status(
            company_id=company_id,
            status=VerificationStatus.REJECTED,
            notes=req.verification_notes
        )
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found.")
        return CompanyResponse.model_validate(company)

    def get_jobs_for_moderation(self, status: ModerationStatus = None, search: str = None, page: int = 1, page_size: int = 20) -> Tuple[List[JobResponse], int]:
        jobs, total = self.repo.get_jobs_for_moderation(moderation_status=status, search=search, page=page, page_size=page_size)
        return [JobResponse.model_validate(j) for j in jobs], total

    def moderate_job(self, job_id: str, req: JobModerateRequest) -> JobResponse:
        job = self.repo.update_job_moderation(
            job_id=job_id,
            moderation_status=req.moderation_status,
            notes=req.moderation_notes
        )
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")
        return JobResponse.model_validate(job)

    # --- FEATURE 41: FLAGGED QUEUE ---
    def get_flagged_activities(self, status_enum: FlagStatus = None, page: int = 1, page_size: int = 20) -> Tuple[List[FlaggedActivityResponse], int]:
        flags, total = self.repo.get_flagged_activities(status=status_enum, page=page, page_size=page_size)
        resp_list = []
        for f in flags:
            resp_list.append(
                FlaggedActivityResponse(
                    id=f.id,
                    reporter_id=f.reporter_id,
                    reporter_name=f.reporter.full_name if f.reporter else "System Flag",
                    target_type=f.target_type,
                    target_id=f.target_id,
                    reason=f.reason,
                    risk_score=f.risk_score,
                    status=f.status,
                    resolution_notes=f.resolution_notes,
                    created_at=f.created_at
                )
            )
        return resp_list, total

    def resolve_flagged_activity(self, admin_id: str, flag_id: str, req: FlagResolveRequest) -> FlaggedActivityResponse:
        resolved = self.repo.resolve_flagged_activity(flag_id=flag_id, status=req.status, admin_id=admin_id, notes=req.resolution_notes)
        if not resolved:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flagged activity report not found.")
        return FlaggedActivityResponse(
            id=resolved.id,
            reporter_id=resolved.reporter_id,
            reporter_name=resolved.reporter.full_name if resolved.reporter else "System Flag",
            target_type=resolved.target_type,
            target_id=resolved.target_id,
            reason=resolved.reason,
            risk_score=resolved.risk_score,
            status=resolved.status,
            resolution_notes=resolved.resolution_notes,
            created_at=resolved.created_at
        )

    # --- FEATURE 40: TELEMETRY & ANALYTICS ---
    def get_dashboard_metrics(self) -> AdminDashboardMetrics:
        metrics = self.repo.get_metrics()
        return AdminDashboardMetrics(**metrics)

    def get_analytics_overview(self) -> AnalyticsOverviewResponse:
        m = self.repo.get_metrics()
        return AnalyticsOverviewResponse(
            active_students=m["active_students"],
            active_recruiters=m["active_recruiters"],
            total_jobs=m["total_jobs"],
            verified_companies=m["verified_companies"],
            pending_verifications=m["pending_verifications"],
            flagged_activities_count=m["flagged_activities_pending"],
            skill_taxonomy_count=m["total_skills"],
            total_projects=m["total_projects"],
            sandbox_challenges_count=m["sandbox_challenges_count"]
        )
