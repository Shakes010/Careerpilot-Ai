from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from app.models.job import Job, JobSkill, JobStatus, EmploymentType, WorkMode

class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, job_id: str) -> Optional[Job]:
        return self.db.query(Job).filter(Job.id == job_id).first()

    def get_by_company(
        self,
        company_id: str,
        search: Optional[str] = None,
        status: Optional[JobStatus] = None,
        employment_type: Optional[EmploymentType] = None,
        work_mode: Optional[WorkMode] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Job], int]:
        query = self.db.query(Job).filter(Job.company_id == company_id)

        if search:
            search_pattern = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Job.title.ilike(search_pattern),
                    Job.description.ilike(search_pattern),
                    Job.job_category.ilike(search_pattern)
                )
            )

        if status:
            query = query.filter(Job.status == status)

        if employment_type:
            query = query.filter(Job.employment_type == employment_type)

        if work_mode:
            query = query.filter(Job.work_mode == work_mode)

        total = query.count()
        offset = (page - 1) * page_size
        jobs = query.order_by(Job.created_at.desc()).offset(offset).limit(page_size).all()

        return jobs, total

    def create(self, job: Job, skill_names: List[str]) -> Job:
        self.db.add(job)
        self.db.flush()

        for skill_name in skill_names:
            if skill_name.strip():
                skill = JobSkill(job_id=job.id, skill_name=skill_name.strip())
                self.db.add(skill)

        self.db.commit()
        self.db.refresh(job)
        return job

    def update(self, job: Job, skill_names: Optional[List[str]] = None) -> Job:
        if skill_names is not None:
            # Replace existing skills
            self.db.query(JobSkill).filter(JobSkill.job_id == job.id).delete()
            for skill_name in skill_names:
                if skill_name.strip():
                    skill = JobSkill(job_id=job.id, skill_name=skill_name.strip())
                    self.db.add(skill)

        self.db.commit()
        self.db.refresh(job)
        return job

    def update_status(self, job: Job, status: JobStatus) -> Job:
        job.status = status
        self.db.commit()
        self.db.refresh(job)
        return job

    def delete(self, job: Job) -> bool:
        self.db.delete(job)
        self.db.commit()
        return True

    def get_dashboard_stats(self, company_id: str) -> dict:
        total = self.db.query(Job).filter(Job.company_id == company_id).count()
        active = self.db.query(Job).filter(Job.company_id == company_id, Job.status == JobStatus.PUBLISHED).count()
        drafts = self.db.query(Job).filter(Job.company_id == company_id, Job.status == JobStatus.DRAFT).count()
        paused = self.db.query(Job).filter(Job.company_id == company_id, Job.status == JobStatus.PAUSED).count()
        closed = self.db.query(Job).filter(Job.company_id == company_id, Job.status == JobStatus.CLOSED).count()

        return {
            "total_jobs": total,
            "active_jobs": active,
            "draft_jobs": drafts,
            "paused_jobs": paused,
            "closed_jobs": closed
        }
