from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import Optional, List
from datetime import date, datetime
from app.models.job import EmploymentType, WorkMode, JobStatus

class JobSkillSchema(BaseModel):
    id: str
    skill_name: str

    model_config = ConfigDict(from_attributes=True)

class JobCreateRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=10)
    employment_type: EmploymentType = EmploymentType.FULL_TIME
    location: str = Field(..., min_length=2, max_length=255)
    work_mode: WorkMode = WorkMode.ONSITE
    
    experience_min: int = Field(default=0, ge=0)
    experience_max: int = Field(default=0, ge=0)
    salary_min: Optional[int] = Field(default=None, ge=0)
    salary_max: Optional[int] = Field(default=None, ge=0)
    salary_currency: str = "INR"
    
    education_requirements: Optional[str] = None
    job_category: Optional[str] = None
    number_of_openings: int = Field(default=1, gt=0)
    application_deadline: date
    skills: List[str] = Field(default_factory=list)

    @field_validator("application_deadline")
    @classmethod
    def validate_deadline(cls, v: date) -> date:
        if v < date.today():
            raise ValueError("Application deadline cannot be in the past.")
        return v

    @model_validator(mode="after")
    def validate_ranges(self):
        if self.experience_max < self.experience_min:
            raise ValueError("experience_max must be greater than or equal to experience_min")
        if self.salary_min is not None and self.salary_max is not None:
            if self.salary_max < self.salary_min:
                raise ValueError("salary_max must be greater than or equal to salary_min")
        return self

class JobUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = Field(None, min_length=10)
    employment_type: Optional[EmploymentType] = None
    location: Optional[str] = None
    work_mode: Optional[WorkMode] = None
    
    experience_min: Optional[int] = Field(None, ge=0)
    experience_max: Optional[int] = Field(None, ge=0)
    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    salary_currency: Optional[str] = None
    
    education_requirements: Optional[str] = None
    job_category: Optional[str] = None
    number_of_openings: Optional[int] = Field(None, gt=0)
    application_deadline: Optional[date] = None
    skills: Optional[List[str]] = None

    @field_validator("application_deadline")
    @classmethod
    def validate_deadline(cls, v: Optional[date]) -> Optional[date]:
        if v is not None and v < date.today():
            raise ValueError("Application deadline cannot be in the past.")
        return v

class JobResponse(BaseModel):
    id: str
    company_id: str
    created_by: Optional[str] = None
    title: str
    description: str
    employment_type: EmploymentType
    location: str
    work_mode: WorkMode
    experience_min: int
    experience_max: int
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: str
    education_requirements: Optional[str] = None
    job_category: Optional[str] = None
    number_of_openings: int
    application_deadline: date
    status: JobStatus
    created_at: datetime
    updated_at: datetime
    skills: List[JobSkillSchema] = []

    model_config = ConfigDict(from_attributes=True)

class JobListFilter(BaseModel):
    search: Optional[str] = None
    status: Optional[JobStatus] = None
    employment_type: Optional[EmploymentType] = None
    work_mode: Optional[WorkMode] = None
    page: int = 1
    page_size: int = 20
