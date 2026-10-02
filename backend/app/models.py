import uuid
from datetime import datetime, timezone
import enum
from sqlalchemy import (
    Column, String, Text, Boolean, Integer, SmallInteger, Numeric, Date, DateTime, ForeignKey, Enum as SQLEnum
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database import Base

def utc_now():
    return datetime.now(timezone.utc)

# Enums
class UserRole(str, enum.Enum):
    student = "student"
    recruiter = "recruiter"
    admin = "admin"

class CertificateStatus(str, enum.Enum):
    pending = "pending"
    verified = "verified"
    rejected = "rejected"

class PortfolioItemType(str, enum.Enum):
    project = "project"
    certificate = "certificate"
    assessment = "assessment"
    badge = "badge"

class BadgeTier(str, enum.Enum):
    declared = "declared"
    verified = "verified"

class EvidenceType(str, enum.Enum):
    project = "project"
    certificate = "certificate"
    assessment = "assessment"
    github = "github"

class AssessmentType(str, enum.Enum):
    programming = "programming"
    aptitude = "aptitude"
    domain = "domain"

class AttemptStatus(str, enum.Enum):
    in_progress = "in_progress"
    passed = "passed"
    failed = "failed"
    flagged_pending = "flagged_pending"
    flagged_rejected = "flagged_rejected"

class ReviewActionEnum(str, enum.Enum):
    approved = "approved"
    rejected = "rejected"

class OpportunityType(str, enum.Enum):
    job = "job"
    hackathon = "hackathon"
    research = "research"
    competition = "competition"

class ApplicationStatus(str, enum.Enum):
    applied = "applied"
    shortlisted = "shortlisted"

class ProjectStatus(str, enum.Enum):
    in_progress = "in_progress"
    completed = "completed"
    verified = "verified"

class TaskStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class CompletionStatus(str, enum.Enum):
    pending = "pending"
    verified = "verified"

class CompanyVerificationStatus(str, enum.Enum):
    pending = "pending"
    verified = "verified"
    rejected = "rejected"

class EmploymentType(str, enum.Enum):
    full_time = "full_time"
    part_time = "part_time"
    internship = "internship"
    contract = "contract"

class WorkMode(str, enum.Enum):
    remote = "remote"
    hybrid = "hybrid"
    onsite = "onsite"

class JobStatus(str, enum.Enum):
    draft = "draft"
    published = "published"
    paused = "paused"
    closed = "closed"
    expired = "expired"

class CandidateRating(str, enum.Enum):
    excellent = "excellent"
    good = "good"
    average = "average"
    weak = "weak"

class CategoryType(str, enum.Enum):
    skill = "skill"
    opportunity = "opportunity"

class PlanTier(str, enum.Enum):
    free = "free"
    basic = "basic"
    premium = "premium"

class SubscriptionStatus(str, enum.Enum):
    active = "active"
    cancelled = "cancelled"
    expired = "expired"

class TransactionStatus(str, enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"

# --- Models ---

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole, name="user_role_enum"), nullable=False)
    full_name = Column(String(150), nullable=True)
    profile_photo_url = Column(Text, nullable=True)
    is_verified = Column(Boolean, default=False)
    phone = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    student_profile = relationship("StudentProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    certificates = relationship("Certificate", back_populates="user", cascade="all, delete-orphan")
    portfolio_items = relationship("PortfolioItem", back_populates="user", cascade="all, delete-orphan")
    github_link = relationship("GithubLink", back_populates="user", uselist=False, cascade="all, delete-orphan")
    linkedin_link = relationship("LinkedinLink", back_populates="user", uselist=False, cascade="all, delete-orphan")
    student_skills = relationship("StudentSkill", back_populates="user", cascade="all, delete-orphan")
    recruiter_profile = relationship("Recruiter", back_populates="user", uselist=False, cascade="all, delete-orphan")


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=False, nullable=False)
    phone = Column(String(50), nullable=True)
    location = Column(String(100), nullable=True)
    college_name = Column(String(200), nullable=True)
    degree = Column(String(100), nullable=True)
    graduation_year = Column(Integer, nullable=True)
    cgpa = Column(Numeric(3, 2), nullable=True)
    career_goal = Column(Text, nullable=True)
    bio = Column(Text, nullable=True)
    profile_completion_pct = Column(Integer, default=0)
    is_eligible = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    user = relationship("User", back_populates="student_profile")


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    resume_label = Column(String(100), nullable=True)
    target_role = Column(String(100), nullable=True)
    current_version_id = Column(UUID(as_uuid=True), ForeignKey("resume_versions.id", use_alter=True, name="fk_resumes_current_version"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    user = relationship("User", back_populates="resumes")
    versions = relationship("ResumeVersion", back_populates="resume", foreign_keys="ResumeVersion.resume_id", cascade="all, delete-orphan")


class ResumeVersion(Base):
    __tablename__ = "resume_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id"), nullable=False)
    version_number = Column(Integer, nullable=False, default=1)
    file_url = Column(Text, nullable=True)
    content_json = Column(JSONB, nullable=True)
    change_summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    resume = relationship("Resume", back_populates="versions", foreign_keys=[resume_id])


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    issuer = Column(String(200), nullable=True)
    file_url = Column(Text, nullable=True)
    issue_date = Column(DateTime(timezone=True), nullable=True)
    verification_status = Column(SQLEnum(CertificateStatus, name="certificate_status_enum"), default=CertificateStatus.pending)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    user = relationship("User", back_populates="certificates")


class PortfolioItem(Base):
    __tablename__ = "portfolio_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    item_type = Column(SQLEnum(PortfolioItemType, name="portfolio_item_type_enum"), nullable=False)
    source_ref_id = Column(UUID(as_uuid=True), nullable=True)
    title = Column(String(200), nullable=False)
    thumbnail_url = Column(Text, nullable=True)
    display_order = Column(Integer, default=0)
    auto_added_at = Column(DateTime(timezone=True), default=utc_now)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    user = relationship("User", back_populates="portfolio_items")


class GithubLink(Base):
    __tablename__ = "github_links"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    github_username = Column(String(100), nullable=False)
    access_token = Column(Text, nullable=True)
    public_repos = Column(Integer, default=0)
    total_commits = Column(Integer, default=0)
    top_languages = Column(JSONB, nullable=True)
    last_synced_at = Column(DateTime(timezone=True), default=utc_now)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    user = relationship("User", back_populates="github_link")


class LinkedinLink(Base):
    __tablename__ = "linkedin_links"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    profile_url = Column(Text, nullable=False)
    headline = Column(Text, nullable=True)
    last_synced_at = Column(DateTime(timezone=True), default=utc_now)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    user = relationship("User", back_populates="linkedin_link")


# --- SKILLS & TRUST ---

class Skill(Base):
    __tablename__ = "skills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill_name = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)


class StudentSkill(Base):
    __tablename__ = "student_skills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id"), nullable=False)
    self_rating = Column(SmallInteger, default=3) # 1-5
    trust_score = Column(SmallInteger, default=20) # 0-100
    badge_tier = Column(SQLEnum(BadgeTier, name="badge_tier_enum"), default=BadgeTier.declared)
    last_computed_at = Column(DateTime(timezone=True), default=utc_now)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    user = relationship("User", back_populates="student_skills")
    skill = relationship("Skill")
    evidences = relationship("SkillEvidence", back_populates="student_skill", cascade="all, delete-orphan")


class SkillEvidence(Base):
    __tablename__ = "skill_evidence"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_skill_id = Column(UUID(as_uuid=True), ForeignKey("student_skills.id"), nullable=False)
    evidence_type = Column(SQLEnum(EvidenceType, name="evidence_type_enum"), nullable=False)
    evidence_ref_id = Column(UUID(as_uuid=True), nullable=True)
    weight = Column(Numeric(3, 2), nullable=False)
    verified_at = Column(DateTime(timezone=True), default=utc_now)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    student_skill = relationship("StudentSkill", back_populates="evidences")


class LearningResource(Base):
    __tablename__ = "learning_resources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id"), nullable=False)
    title = Column(String(200), nullable=False)
    url = Column(Text, nullable=False)
    source = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    skill = relationship("Skill")


# --- ASSESSMENTS ---

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_name = Column(String(200), nullable=False)
    assessment_type = Column(SQLEnum(AssessmentType, name="assessment_type_enum"), nullable=False)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id"), nullable=True)
    is_language_flexible = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    checkpoints = relationship("AssessmentCheckpoint", back_populates="assessment", cascade="all, delete-orphan")
    skill = relationship("Skill")


class AssessmentCheckpoint(Base):
    __tablename__ = "assessment_checkpoints"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.id"), nullable=False)
    sequence_order = Column(SmallInteger, nullable=False)
    title = Column(String(200), nullable=False)
    instructions = Column(Text, nullable=False)
    validation_test = Column(Text, nullable=True) # Text or JSON string for language-agnostic test cases
    created_at = Column(DateTime(timezone=True), default=utc_now)

    assessment = relationship("Assessment", back_populates="checkpoints")


class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.id"), nullable=False)
    status = Column(SQLEnum(AttemptStatus, name="attempt_status_enum"), default=AttemptStatus.in_progress)
    score_pct = Column(Numeric(5, 2), default=0.0)
    is_flagged = Column(Boolean, default=False)
    flag_reason = Column(Text, nullable=True)
    taken_at = Column(DateTime(timezone=True), default=utc_now)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    assessment = relationship("Assessment")
    user = relationship("User")
    submissions = relationship("CheckpointSubmission", back_populates="attempt", cascade="all, delete-orphan")
    review_action = relationship("ReviewAction", back_populates="attempt", uselist=False, cascade="all, delete-orphan")


class CheckpointSubmission(Base):
    __tablename__ = "checkpoint_submissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    attempt_id = Column(UUID(as_uuid=True), ForeignKey("assessment_attempts.id"), nullable=False)
    checkpoint_id = Column(UUID(as_uuid=True), ForeignKey("assessment_checkpoints.id"), nullable=False)
    submitted_code = Column(Text, nullable=True)
    language = Column(String(50), nullable=True)
    paste_event_count = Column(Integer, default=0)
    paste_char_count = Column(Integer, default=0)
    time_spent_seconds = Column(Integer, default=0)
    submitted_at = Column(DateTime(timezone=True), default=utc_now)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    attempt = relationship("AssessmentAttempt", back_populates="submissions")
    checkpoint = relationship("AssessmentCheckpoint")


class ReviewAction(Base):
    __tablename__ = "review_actions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    attempt_id = Column(UUID(as_uuid=True), ForeignKey("assessment_attempts.id"), nullable=False)
    admin_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    action = Column(SQLEnum(ReviewActionEnum, name="review_action_enum"), nullable=False)
    explanation_reviewed = Column(Text, nullable=True)
    reviewed_at = Column(DateTime(timezone=True), default=utc_now)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    attempt = relationship("AssessmentAttempt", back_populates="review_action")


# --- OPPORTUNITIES ---

class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    title = Column(String(150), nullable=False)
    required_skills = Column(JSONB, nullable=True)
    min_readiness_pct = Column(SmallInteger, nullable=True)
    description = Column(Text, nullable=True)
    employment_type = Column(SQLEnum(EmploymentType, name="employment_type_enum"), default=EmploymentType.full_time)
    location = Column(String(150), nullable=True)
    work_mode = Column(SQLEnum(WorkMode, name="work_mode_enum"), default=WorkMode.remote)
    experience_min = Column(Integer, default=0)
    experience_max = Column(Integer, default=2)
    salary_min = Column(Numeric(12, 2), nullable=True)
    salary_max = Column(Numeric(12, 2), nullable=True)
    salary_currency = Column(String(10), default="INR")
    number_of_openings = Column(Integer, default=1)
    application_deadline = Column(DateTime(timezone=True), nullable=True)
    status = Column(SQLEnum(JobStatus, name="job_status_enum"), default=JobStatus.published)
    posted_at = Column(DateTime(timezone=True), default=utc_now)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    company = relationship("Company", back_populates="jobs")


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    opportunity_type = Column(SQLEnum(OpportunityType, name="opportunity_type_enum"), nullable=False)
    title = Column(String(200), nullable=False)
    organizer = Column(String(200), nullable=True)
    required_skills = Column(JSONB, nullable=True)
    deadline = Column(DateTime(timezone=True), nullable=True)
    source_job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    source_job = relationship("Job")


class OpportunityRecommendation(Base):
    __tablename__ = "opportunity_recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    opportunity_id = Column(UUID(as_uuid=True), ForeignKey("opportunities.id"), nullable=False)
    relevance_score = Column(SmallInteger, default=50)
    reason = Column(Text, nullable=True)
    generated_at = Column(DateTime(timezone=True), default=utc_now)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    opportunity = relationship("Opportunity")


class Application(Base):
    __tablename__ = "applications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    opportunity_id = Column(UUID(as_uuid=True), ForeignKey("opportunities.id"), nullable=False)
    status = Column(SQLEnum(ApplicationStatus, name="application_status_enum"), default=ApplicationStatus.applied)
    applied_at = Column(DateTime(timezone=True), default=utc_now)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    opportunity = relationship("Opportunity")
    user = relationship("User")


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    opportunity_id = Column(UUID(as_uuid=True), ForeignKey("opportunities.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)


# --- PROJECTS ---

class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    repo_url = Column(Text, nullable=True)
    tech_stack = Column(JSONB, nullable=True)
    status = Column(SQLEnum(ProjectStatus, name="project_status_enum"), default=ProjectStatus.in_progress)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    owner = relationship("User")
    members = relationship("ProjectMember", back_populates="project", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    completion = relationship("ProjectCompletion", back_populates="project", uselist=False, cascade="all, delete-orphan")


class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    role = Column(String(100), default="Collaborator")
    created_at = Column(DateTime(timezone=True), default=utc_now)

    project = relationship("Project", back_populates="members")
    user = relationship("User")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    title = Column(String(200), nullable=False)
    status = Column(SQLEnum(TaskStatus, name="task_status_enum"), default=TaskStatus.todo)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User")


class ProjectCompletion(Base):
    __tablename__ = "project_completions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    verified_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    verified_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(SQLEnum(CompletionStatus, name="completion_status_enum"), default=CompletionStatus.pending)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    project = relationship("Project", back_populates="completion")


class CareerSandboxChallenge(Base):
    __tablename__ = "career_sandbox_challenges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id"), nullable=True)
    difficulty = Column(String(50), default="Medium")
    created_at = Column(DateTime(timezone=True), default=utc_now)

    skill = relationship("Skill")


# --- RECRUITER & PAYMENTS ---

class Company(Base):
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False)
    industry = Column(String(100), nullable=True)
    logo_url = Column(Text, nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(Text, nullable=True)
    verification_status = Column(SQLEnum(CompanyVerificationStatus, name="company_verification_status_enum"), default=CompanyVerificationStatus.pending)
    verification_notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    recruiters = relationship("Recruiter", back_populates="company")
    jobs = relationship("Job", back_populates="company")


class Recruiter(Base):
    __tablename__ = "recruiters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    designation = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    user = relationship("User", back_populates="recruiter_profile")
    company = relationship("Company", back_populates="recruiters")
    subscriptions = relationship("Subscription", back_populates="recruiter")


class JobMatchResult(Base):
    __tablename__ = "job_match_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    overall_score = Column(SmallInteger, default=0)
    matched_skills = Column(JSONB, nullable=True)
    missing_skills = Column(JSONB, nullable=True)
    portfolio_rating = Column(SQLEnum(CandidateRating, name="portfolio_rating_enum"), default=CandidateRating.average)
    assessment_rating = Column(SQLEnum(CandidateRating, name="assessment_rating_enum"), default=CandidateRating.average)
    computed_at = Column(DateTime(timezone=True), default=utc_now)
    created_at = Column(DateTime(timezone=True), default=utc_now)


class CandidateShortlist(Base):
    __tablename__ = "candidate_shortlists"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recruiter_id = Column(UUID(as_uuid=True), ForeignKey("recruiters.id"), nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    shortlisted_at = Column(DateTime(timezone=True), default=utc_now)
    created_at = Column(DateTime(timezone=True), default=utc_now)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    action = Column(String(200), nullable=False)
    details = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)


class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    category_type = Column(SQLEnum(CategoryType, name="category_type_enum"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)


class Plan(Base):
    __tablename__ = "plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_name = Column(String(100), nullable=False)
    tier = Column(SQLEnum(PlanTier, name="plan_tier_enum"), nullable=False)
    monthly_credits = Column(Integer, default=50)
    price_inr = Column(Numeric(10, 2), default=0.0)
    features = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recruiter_id = Column(UUID(as_uuid=True), ForeignKey("recruiters.id"), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    plan_id = Column(UUID(as_uuid=True), ForeignKey("plans.id"), nullable=False)
    credits_remaining = Column(Integer, default=50)
    is_trial = Column(Boolean, default=False)
    trial_ends_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(SQLEnum(SubscriptionStatus, name="subscription_status_enum"), default=SubscriptionStatus.active)
    renews_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    recruiter = relationship("Recruiter", back_populates="subscriptions")
    plan = relationship("Plan")
    user = relationship("User")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subscription_id = Column(UUID(as_uuid=True), ForeignKey("subscriptions.id"), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    razorpay_order_id = Column(String(250), nullable=False)
    razorpay_payment_id = Column(String(250), nullable=True)
    amount_inr = Column(Numeric(10, 2), nullable=False)
    plan_name = Column(String(150), nullable=True)
    payment_method = Column(String(50), nullable=True)
    status = Column(SQLEnum(TransactionStatus, name="transaction_status_enum"), default=TransactionStatus.pending)
    created_at = Column(DateTime(timezone=True), default=utc_now)


class CreditLedger(Base):
    __tablename__ = "credit_ledger"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subscription_id = Column(UUID(as_uuid=True), ForeignKey("subscriptions.id"), nullable=False)
    action = Column(String(255), nullable=False)
    credits_used = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), default=utc_now)
