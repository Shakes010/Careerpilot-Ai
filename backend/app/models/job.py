import uuid
import enum
from datetime import datetime, timezone, date
from sqlalchemy import Column, String, Text, Integer, DateTime, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class EmploymentType(str, enum.Enum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    INTERNSHIP = "INTERNSHIP"
    CONTRACT = "CONTRACT"

class WorkMode(str, enum.Enum):
    REMOTE = "REMOTE"
    HYBRID = "HYBRID"
    ONSITE = "ONSITE"

class JobStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    PAUSED = "PAUSED"
    CLOSED = "CLOSED"
    EXPIRED = "EXPIRED"

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    created_by = Column(String(36), ForeignKey("recruiters.id", ondelete="SET NULL"), nullable=True)
    
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    employment_type = Column(Enum(EmploymentType), nullable=False, default=EmploymentType.FULL_TIME)
    location = Column(String(255), nullable=False)
    work_mode = Column(Enum(WorkMode), nullable=False, default=WorkMode.ONSITE)
    
    experience_min = Column(Integer, nullable=False, default=0)
    experience_max = Column(Integer, nullable=False, default=0)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    salary_currency = Column(String(10), nullable=False, default="INR")
    
    education_requirements = Column(String(255), nullable=True)
    job_category = Column(String(150), nullable=True)
    number_of_openings = Column(Integer, nullable=False, default=1)
    application_deadline = Column(Date, nullable=False)
    status = Column(Enum(JobStatus), nullable=False, default=JobStatus.DRAFT, index=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    company = relationship("Company", back_populates="jobs")
    recruiter = relationship("Recruiter", back_populates="jobs")
    skills = relationship("JobSkill", back_populates="job", cascade="all, delete-orphan")

class JobSkill(Base):
    __tablename__ = "job_skills"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String(36), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_name = Column(String(100), nullable=False)

    job = relationship("Job", back_populates="skills")
