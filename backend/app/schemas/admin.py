from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.models.job import ModerationStatus
from app.models.user import UserRole
from app.models.admin import FlagTargetType, FlagStatus

class CompanyVerifyRequest(BaseModel):
    verification_notes: Optional[str] = "Company information verified by platform administrator."

class CompanyRejectRequest(BaseModel):
    verification_notes: str = Field(..., min_length=5, description="Mandatory explanation for verification rejection")

class JobModerateRequest(BaseModel):
    moderation_status: ModerationStatus
    moderation_notes: Optional[str] = None

class UserManagementResponse(BaseModel):
    id: str
    email: str
    full_name: str
    phone: Optional[str] = None
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserStatusUpdateRequest(BaseModel):
    is_active: bool
    notes: Optional[str] = None

class UserRoleUpdateRequest(BaseModel):
    role: UserRole

class FlagResolveRequest(BaseModel):
    status: FlagStatus
    resolution_notes: Optional[str] = "Resolved by administrator."

class FlaggedActivityResponse(BaseModel):
    id: str
    reporter_id: Optional[str] = None
    reporter_name: Optional[str] = "System"
    target_type: FlagTargetType
    target_id: str
    reason: str
    risk_score: float
    status: FlagStatus
    resolution_notes: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AdminDashboardMetrics(BaseModel):
    pending_verifications: int
    verified_companies: int
    rejected_companies: int
    total_companies: int
    total_jobs: int
    flagged_jobs: int
    total_skills: int
    total_users: int = 0
    active_students: int = 0
    active_recruiters: int = 0
    flagged_activities_pending: int = 0

class AnalyticsOverviewResponse(BaseModel):
    active_students: int
    active_recruiters: int
    total_jobs: int
    verified_companies: int
    pending_verifications: int
    flagged_activities_count: int
    skill_taxonomy_count: int
    total_projects: int = 0
    sandbox_challenges_count: int = 0
