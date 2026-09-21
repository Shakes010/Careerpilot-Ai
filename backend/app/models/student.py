from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, default="student")  # "student"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    profile = relationship("StudentProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    educations = relationship("StudentEducation", back_populates="user", cascade="all, delete-orphan")
    skills = relationship("StudentSkill", back_populates="user", cascade="all, delete-orphan")
    resumes = relationship("StudentResume", back_populates="user", cascade="all, delete-orphan")
    resume_versions = relationship("StudentResumeVersion", back_populates="user", cascade="all, delete-orphan")
    certificates = relationship("StudentCertificate", back_populates="user", cascade="all, delete-orphan")
    github_profile = relationship("StudentGithubProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    timeline_events = relationship("StudentTimelineEvent", back_populates="user", cascade="all, delete-orphan")
    career_preference = relationship("StudentCareerPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    applications = relationship("JobApplication", back_populates="user", cascade="all, delete-orphan")


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    headline = Column(String, nullable=True, default=None)
    phone = Column(String, nullable=True, default=None)
    location = Column(String, nullable=True, default=None)
    linkedin_url = Column(String, nullable=True, default=None)
    github_url = Column(String, nullable=True, default=None)
    website = Column(String, nullable=True, default=None)
    university = Column(String, nullable=True, default="National Institute of Technology")
    major = Column(String, nullable=True, default="Master of Computer Applications (MCA)")
    graduation_year = Column(Integer, default=2026)
    bio = Column(Text, nullable=True, default=None)
    profile_picture = Column(String, nullable=True, default=None)
    
    # Career metrics
    career_readiness_score = Column(Integer, default=0) # Percentage 0-100
    applications_sent = Column(Integer, default=0)
    active_opportunities = Column(Integer, default=0)
    assessments_completed = Column(Integer, default=0)
    verified_skills_count = Column(Integer, default=0)
    skill_trust_meter = Column(Float, default=0.0) # Trust score %
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="profile")


class StudentEducation(Base):
    __tablename__ = "student_education"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    degree = Column(String, nullable=False) # e.g., MCA, B.Tech, B.Sc Computer Science
    institution = Column(String, nullable=False) # e.g., National Institute of Technology
    start_year = Column(Integer, nullable=False)
    end_year = Column(Integer, nullable=True)
    grade = Column(String, nullable=True) # e.g., 3.9/4.0 GPA or 88%
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="educations")


class StudentSkill(Base):
    __tablename__ = "student_skills"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    skill_name = Column(String, nullable=False, index=True) # e.g., Python, Vue.js, FastAPI
    category = Column(String, default="Programming Languages") # "Programming Languages", "Web Development", "AI / Data Science", "Cloud & DevOps", "Soft Skills"
    proficiency = Column(String, default="Intermediate") # "Beginner", "Intermediate", "Advanced", "Expert"
    is_verified = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="skills")


class StudentResume(Base):
    __tablename__ = "student_resumes"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False) # e.g., application/pdf
    file_size = Column(Integer, nullable=False) # bytes
    summary = Column(Text, nullable=True)
    ats_score = Column(Integer, default=85)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="resumes")


class StudentCareerPreference(Base):
    __tablename__ = "student_career_preferences"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False, index=True)
    
    preferred_role = Column(String, default="Full Stack Engineer")
    preferred_industry = Column(String, default="Artificial Intelligence & Software")
    preferred_location = Column(String, default="Remote / Hybrid")
    employment_type = Column(String, default="Full-Time") # "Full-Time", "Internship", "Contract"
    work_mode = Column(String, default="Hybrid") # "Remote", "On-site", "Hybrid"
    expected_salary = Column(String, default="$85,000 - $120,000 / year")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="career_preference")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    company = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    location = Column(String, nullable=False)
    type = Column(String, default="Job") # "Job", "Internship", "Hackathon"
    required_skills = Column(Text, nullable=False) # Comma-separated strings or JSON string
    min_education = Column(String, default="Bachelor's / Master's")
    description = Column(Text, nullable=False)
    salary_range = Column(String, default="$90,000 - $130,000")
    deadline = Column(String, default="Sep 30, 2026")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    applications = relationship("JobApplication", back_populates="job")


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False, index=True)
    
    application_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Applied") # "Pending", "Applied", "Under Review", "Interviewed", "Accepted", "Rejected"
    notes = Column(Text, nullable=True)

    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")


class LearningResource(Base):
    __tablename__ = "learning_resources"

    id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String, nullable=False, index=True)
    topic = Column(String, nullable=False)
    title = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    url = Column(String, nullable=False)
    difficulty = Column(String, default="Intermediate")


class StudentResumeVersion(Base):
    __tablename__ = "student_resume_versions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    title = Column(String, nullable=False) # e.g. "Full Stack Resume v1"
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, default="application/pdf")
    file_size = Column(Integer, default=0) # bytes
    summary = Column(Text, nullable=True)
    content_json = Column(Text, nullable=True) # JSON representation if AI generated or structured
    ats_score = Column(Integer, default=85)
    is_active = Column(Boolean, default=True)
    status = Column(String, default="Active") # "Active", "Archived"
    source = Column(String, default="Uploaded") # "Uploaded", "AI Generated"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="resume_versions")


class StudentCertificate(Base):
    __tablename__ = "student_certificates"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    title = Column(String, nullable=False)
    issuing_organization = Column(String, nullable=False)
    issue_date = Column(String, nullable=False)
    expiry_date = Column(String, nullable=True)
    credential_id = Column(String, nullable=True)
    credential_url = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    skills_tags = Column(String, nullable=True)
    filename = Column(String, nullable=True)
    file_path = Column(String, nullable=True)
    file_type = Column(String, nullable=True)
    file_size = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="certificates")


class StudentGithubProfile(Base):
    __tablename__ = "student_github_profiles"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False, index=True)
    
    username = Column(String, nullable=False)
    name = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String, nullable=True)
    html_url = Column(String, nullable=False)
    public_repos = Column(Integer, default=0)
    followers = Column(Integer, default=0)
    following = Column(Integer, default=0)
    last_synced_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="github_profile")
    repositories = relationship("StudentGithubRepository", back_populates="github_profile", cascade="all, delete-orphan")


class StudentGithubRepository(Base):
    __tablename__ = "student_github_repositories"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    github_profile_id = Column(Integer, ForeignKey("student_github_profiles.id"), nullable=False, index=True)
    
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    html_url = Column(String, nullable=False)
    language = Column(String, nullable=True)
    stargazers_count = Column(Integer, default=0)
    forks_count = Column(Integer, default=0)
    is_fork = Column(Boolean, default=False)
    updated_at_remote = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    github_profile = relationship("StudentGithubProfile", back_populates="repositories")


class StudentTimelineEvent(Base):
    __tablename__ = "student_timeline_events"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=False) # "Education", "Skill", "Certificate", "Resume", "GitHub", "Preference", "Milestone"
    event_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="timeline_events")


