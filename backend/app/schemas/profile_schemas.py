from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from app.models import UserRole, CertificateStatus, PortfolioItemType, BadgeTier

# Auth
class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.student
    full_name: str
    phone: Optional[str] = None
    degree: Optional[str] = None # e.g. B.Tech Computer Science, BCA, MCA
    graduation_year: Optional[int] = None # e.g. 2025
    college_name: Optional[str] = None

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    role: str
    full_name: Optional[str] = None
    email: str
    is_eligible: bool = True
    is_premium: bool = False

class UserOut(BaseModel):
    id: UUID
    email: str
    role: UserRole
    full_name: Optional[str] = None
    profile_photo_url: Optional[str] = None
    is_verified: bool
    phone: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Student Profile
class StudentProfileUpdate(BaseModel):
    phone: Optional[str] = None
    location: Optional[str] = None
    college_name: Optional[str] = None
    degree: Optional[str] = None
    graduation_year: Optional[int] = None
    cgpa: Optional[float] = None
    career_goal: Optional[str] = None
    bio: Optional[str] = None

class StudentProfileOut(BaseModel):
    id: UUID
    user_id: UUID
    phone: Optional[str] = None
    location: Optional[str] = None
    college_name: Optional[str] = None
    degree: Optional[str] = None
    graduation_year: Optional[int] = None
    cgpa: Optional[float] = None
    career_goal: Optional[str] = None
    bio: Optional[str] = None
    profile_completion_pct: int
    is_eligible: bool
    is_premium: Optional[bool] = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Resumes
class ResumeCreate(BaseModel):
    resume_label: str
    target_role: Optional[str] = "Software Engineer"
    content_json: Optional[Dict[str, Any]] = None

class ResumeVersionOut(BaseModel):
    id: UUID
    resume_id: UUID
    version_number: int
    file_url: Optional[str] = None
    content_json: Optional[Dict[str, Any]] = None
    change_summary: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ResumeOut(BaseModel):
    id: UUID
    user_id: UUID
    resume_label: Optional[str] = None
    target_role: Optional[str] = None
    current_version_id: Optional[UUID] = None
    created_at: datetime
    versions: List[ResumeVersionOut] = []

    class Config:
        from_attributes = True

# Certificates
class CertificateCreate(BaseModel):
    title: str
    issuer: Optional[str] = None
    file_url: Optional[str] = None
    issue_date: Optional[datetime] = None

class CertificateOut(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    issuer: Optional[str] = None
    file_url: Optional[str] = None
    issue_date: Optional[datetime] = None
    verification_status: CertificateStatus
    created_at: datetime

    class Config:
        from_attributes = True

# Portfolio Items
class PortfolioItemCreate(BaseModel):
    item_type: PortfolioItemType
    source_ref_id: Optional[UUID] = None
    title: str
    thumbnail_url: Optional[str] = None
    display_order: Optional[int] = 0

class PortfolioItemOut(BaseModel):
    id: UUID
    user_id: UUID
    item_type: PortfolioItemType
    source_ref_id: Optional[UUID] = None
    title: str
    thumbnail_url: Optional[str] = None
    display_order: int
    auto_added_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True

# GitHub & LinkedIn
class GithubSyncRequest(BaseModel):
    github_username: str

class GithubLinkOut(BaseModel):
    id: UUID
    user_id: UUID
    github_username: str
    public_repos: int
    total_commits: int
    top_languages: Optional[Dict[str, Any]] = None
    last_synced_at: datetime

    class Config:
        from_attributes = True

class LinkedinLinkCreate(BaseModel):
    profile_url: str
    headline: Optional[str] = None

class LinkedinLinkOut(BaseModel):
    id: UUID
    user_id: UUID
    profile_url: str
    headline: Optional[str] = None
    last_synced_at: datetime

    class Config:
        from_attributes = True
