from typing import List, Tuple, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.job import Job, JobStatus, EmploymentType, WorkMode
from app.models.company import VerificationStatus
from app.repositories.job_repository import JobRepository
from app.repositories.company_repository import CompanyRepository
from app.schemas.job import JobCreateRequest, JobUpdateRequest, JobResponse, JobListFilter

class JobService:
    def __init__(self, db: Session):
        self.db = db
        self.job_repo = JobRepository(db)
        self.company_repo = CompanyRepository(db)

    def create_job(self, recruiter_id: str, company_id: str, req: JobCreateRequest, publish_immediately: bool = False) -> JobResponse:
        company = self.company_repo.get_by_id(company_id)
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found.")

        initial_status = JobStatus.DRAFT
        if publish_immediately:
            if company.verification_status == VerificationStatus.PENDING:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Your company must be verified before publishing jobs."
                )
            elif company.verification_status == VerificationStatus.REJECTED:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Your company verification was rejected. You cannot publish jobs."
                )
            initial_status = JobStatus.PUBLISHED

        job = Job(
            company_id=company_id,
            created_by=recruiter_id,
            title=req.title.strip(),
            description=req.description.strip(),
            employment_type=req.employment_type,
            location=req.location.strip(),
            work_mode=req.work_mode,
            experience_min=req.experience_min,
            experience_max=req.experience_max,
            salary_min=req.salary_min,
            salary_max=req.salary_max,
            salary_currency=req.salary_currency,
            education_requirements=req.education_requirements.strip() if req.education_requirements else None,
            job_category=req.job_category.strip() if req.job_category else None,
            number_of_openings=req.number_of_openings,
            application_deadline=req.application_deadline,
            status=initial_status
        )

        created_job = self.job_repo.create(job, req.skills)
        return JobResponse.model_validate(created_job)

    def get_job_details(self, job_id: str, company_id: str) -> JobResponse:
        job = self.job_repo.get_by_id(job_id)
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")

        # Strict Recruiter Ownership check
        if job.company_id != company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. You do not have permission to view this job."
            )

        return JobResponse.model_validate(job)

    def list_jobs(self, company_id: str, filter_params: JobListFilter) -> Tuple[List[JobResponse], int]:
        jobs, total = self.job_repo.get_by_company(
            company_id=company_id,
            search=filter_params.search,
            status=filter_params.status,
            employment_type=filter_params.employment_type,
            work_mode=filter_params.work_mode,
            page=filter_params.page,
            page_size=filter_params.page_size
        )
        return [JobResponse.model_validate(j) for j in jobs], total

    def update_job(self, job_id: str, company_id: str, req: JobUpdateRequest) -> JobResponse:
        job = self.job_repo.get_by_id(job_id)
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")

        if job.company_id != company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. You do not have permission to modify this job."
            )

        update_data = req.model_dump(exclude_unset=True)
        skills = update_data.pop("skills", None)

        for key, value in update_data.items():
            if value is not None:
                setattr(job, key, value)

        updated_job = self.job_repo.update(job, skills)
        return JobResponse.model_validate(updated_job)

    def publish_job(self, job_id: str, company_id: str) -> JobResponse:
        job = self.job_repo.get_by_id(job_id)
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")

        if job.company_id != company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. You do not have permission to modify this job."
            )

        company = self.company_repo.get_by_id(company_id)
        if not company or company.verification_status == VerificationStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Your company must be verified before publishing jobs."
            )
        elif company.verification_status == VerificationStatus.REJECTED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Your company verification was rejected. You cannot publish jobs."
            )

        if job.status == JobStatus.CLOSED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Closed jobs cannot be republished."
            )

        updated = self.job_repo.update_status(job, JobStatus.PUBLISHED)
        return JobResponse.model_validate(updated)

    def pause_job(self, job_id: str, company_id: str) -> JobResponse:
        job = self.job_repo.get_by_id(job_id)
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")

        if job.company_id != company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied."
            )

        if job.status != JobStatus.PUBLISHED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only published jobs can be paused."
            )

        updated = self.job_repo.update_status(job, JobStatus.PAUSED)
        return JobResponse.model_validate(updated)

    def close_job(self, job_id: str, company_id: str) -> JobResponse:
        job = self.job_repo.get_by_id(job_id)
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")

        if job.company_id != company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied."
            )

        updated = self.job_repo.update_status(job, JobStatus.CLOSED)
        return JobResponse.model_validate(updated)

    def delete_job(self, job_id: str, company_id: str) -> bool:
        job = self.job_repo.get_by_id(job_id)
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")

        if job.company_id != company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied."
            )

        if job.status != JobStatus.DRAFT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only draft jobs can be deleted. Published, paused, or closed jobs must use status transitions."
            )

        return self.job_repo.delete(job)

    def get_dashboard_summary(self, company_id: str) -> dict:
        company = self.company_repo.get_by_id(company_id)
        stats = self.job_repo.get_dashboard_stats(company_id)
        stats["company_name"] = company.name if company else "Company"
        stats["verification_status"] = company.verification_status.value if company else "PENDING"
        return stats
