from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime


# Auth Schemas
class StudentRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    university: Optional[str] = "National Institute of Technology"
    major: Optional[str] = "Master of Computer Applications (MCA)"

class StudentLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True

# Profile Schemas
class StudentProfileResponse(BaseModel):
    id: int
    user_id: int
    headline: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    website: Optional[str] = None
    university: Optional[str] = None
    major: Optional[str] = None
    graduation_year: Optional[int] = 2026
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    career_readiness_score: int = 0
    applications_sent: int = 0
    active_opportunities: int = 0
    assessments_completed: int = 0
    verified_skills_count: int = 0
    skill_trust_meter: float = 0.0

    class Config:
        from_attributes = True

class StudentProfileUpdate(BaseModel):
    headline: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    website: Optional[str] = None
    university: Optional[str] = None
    major: Optional[str] = None
    graduation_year: Optional[int] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None

# Education Schemas
class StudentEducationCreate(BaseModel):
    degree: str
    institution: str
    start_year: int
    end_year: Optional[int] = None
    grade: Optional[str] = None
    details: Optional[str] = None

class StudentEducationUpdate(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    grade: Optional[str] = None
    details: Optional[str] = None

class StudentEducationResponse(BaseModel):
    id: int
    student_id: int
    degree: str
    institution: str
    start_year: int
    end_year: Optional[int] = None
    grade: Optional[str] = None
    details: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Skill Schemas
class StudentSkillCreate(BaseModel):
    skill_name: str
    category: Optional[str] = "Programming Languages"
    proficiency: Optional[str] = "Intermediate"
    is_verified: Optional[bool] = True

class StudentSkillUpdate(BaseModel):
    skill_name: Optional[str] = None
    category: Optional[str] = None
    proficiency: Optional[str] = None
    is_verified: Optional[bool] = None

class StudentSkillResponse(BaseModel):
    id: int
    student_id: int
    skill_name: str
    category: str
    proficiency: str
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Resume Schemas
class StudentResumeResponse(BaseModel):
    id: int
    student_id: int
    filename: str
    file_path: str
    file_type: str
    file_size: int
    summary: Optional[str] = None
    ats_score: int
    uploaded_at: datetime

    class Config:
        from_attributes = True

class ResumeUploadRequest(BaseModel):
    filename: str
    summary: Optional[str] = None
    parsed_skills: Optional[List[str]] = []

# Career Preference Schemas
class CareerPreferenceCreateOrUpdate(BaseModel):
    preferred_role: str
    preferred_industry: str
    preferred_location: str
    employment_type: Optional[str] = "Full-Time"
    work_mode: Optional[str] = "Hybrid"
    expected_salary: Optional[str] = "$85,000 - $120,000 / year"

class CareerPreferenceResponse(BaseModel):
    id: int
    student_id: int
    preferred_role: str
    preferred_industry: str
    preferred_location: str
    employment_type: str
    work_mode: str
    expected_salary: Optional[str] = None
    updated_at: datetime

    class Config:
        from_attributes = True

# Job & Recommendation Schemas
class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    industry: str
    location: str
    type: str
    required_skills: str
    min_education: str
    description: str
    salary_range: str
    deadline: str
    is_active: bool

    class Config:
        from_attributes = True

# Skill Gap Schemas
class SkillGapItem(BaseModel):
    target_role: str
    existing_skills: List[str]
    required_skills: List[str]
    missing_skills: List[str]
    match_percentage: int

class LearningResourceResponse(BaseModel):
    id: int
    skill_name: str
    topic: str
    title: str
    provider: str
    url: str
    difficulty: str

    class Config:
        from_attributes = True

# Job Application Schemas
class JobApplicationCreate(BaseModel):
    job_id: int
    notes: Optional[str] = None

class JobApplicationUpdateStatus(BaseModel):
    status: str # "Applied", "Under Review", "Interviewed", "Accepted", "Rejected"
    notes: Optional[str] = None

class JobApplicationResponse(BaseModel):
    id: int
    student_id: int
    job_id: int
    application_date: datetime
    status: str
    notes: Optional[str] = None
    job: JobResponse

    class Config:
        from_attributes = True

# Auth Response
class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    profile: StudentProfileResponse

# Dashboard Summary
class ApplicationStatusSummary(BaseModel):
    applied: int
    under_review: int
    interviewed: int
    accepted: int
    rejected: int

class StudentDashboardSummary(BaseModel):
    user: UserResponse
    profile: StudentProfileResponse
    completion_percentage: int
    education_count: int
    skills_count: int
    resumes_count: int
    career_preference: Optional[CareerPreferenceResponse] = None
    application_summary: ApplicationStatusSummary
    skill_gap_summary: SkillGapItem
    ai_recommendations: List[str]


# -------------------------------------------------------------
# SCHEMAS FOR THE 6 NEW FUNCTIONALITIES
# -------------------------------------------------------------

# 1. Smart Resume Version Manager Schemas
class StudentResumeVersionCreate(BaseModel):
    title: str
    filename: Optional[str] = "Generated_Resume.pdf"
    summary: Optional[str] = None
    content_json: Optional[str] = None

class StudentResumeVersionUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None

class StudentResumeVersionResponse(BaseModel):
    id: int
    student_id: int
    title: str
    filename: str
    file_path: str
    file_type: str
    file_size: int
    summary: Optional[str] = None
    content_json: Optional[str] = None
    ats_score: int
    is_active: bool
    status: str
    source: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 2. Certificate Management Schemas
class StudentCertificateCreate(BaseModel):
    title: str
    issuing_organization: str
    issue_date: str
    expiry_date: Optional[str] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None
    description: Optional[str] = None
    skills_tags: Optional[str] = None

class StudentCertificateUpdate(BaseModel):
    title: Optional[str] = None
    issuing_organization: Optional[str] = None
    issue_date: Optional[str] = None
    expiry_date: Optional[str] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None
    description: Optional[str] = None
    skills_tags: Optional[str] = None

class StudentCertificateResponse(BaseModel):
    id: int
    student_id: int
    title: str
    issuing_organization: str
    issue_date: str
    expiry_date: Optional[str] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None
    description: Optional[str] = None
    skills_tags: Optional[str] = None
    filename: Optional[str] = None
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


# 3. GitHub Integration Schemas
class GithubConnectRequest(BaseModel):
    username: str

class StudentGithubRepositoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    html_url: str
    language: Optional[str] = None
    stargazers_count: int
    forks_count: int
    is_fork: bool
    updated_at_remote: Optional[str] = None

    class Config:
        from_attributes = True

class StudentGithubProfileResponse(BaseModel):
    id: int
    student_id: int
    username: str
    name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    html_url: str
    public_repos: int
    followers: int
    following: int
    last_synced_at: datetime
    repositories: List[StudentGithubRepositoryResponse] = []

    class Config:
        from_attributes = True



# 4. Career Timeline Schemas
class StudentTimelineEventResponse(BaseModel):
    id: int
    student_id: int
    title: str
    description: Optional[str] = None
    category: str
    event_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True


# 5. Career Passport Schemas
class CareerPassportResponse(BaseModel):
    user: UserResponse
    profile: StudentProfileResponse
    educations: List[StudentEducationResponse]
    skills: List[StudentSkillResponse]
    active_resume: Optional[StudentResumeVersionResponse] = None
    certificates: List[StudentCertificateResponse]
    github_profile: Optional[StudentGithubProfileResponse] = None
    career_preference: Optional[CareerPreferenceResponse] = None
    recent_timeline: List[StudentTimelineEventResponse]


# 6. AI Resume Generator Schemas
class AIGeneratedResumeData(BaseModel):
    full_name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    professional_summary: str
    skills_grouped: Optional[List[Dict[str, Any]]] = []
    education: Optional[List[Dict[str, Any]]] = []
    certifications: Optional[List[Dict[str, Any]]] = []
    projects: Optional[List[Dict[str, Any]]] = []
    target_role: Optional[str] = None

class AISaveResumeRequest(BaseModel):
    title: str
    resume_data: AIGeneratedResumeData
    set_active: Optional[bool] = True



