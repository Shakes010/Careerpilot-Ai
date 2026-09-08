from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.user import User, UserRole
from app.models.company import Company, VerificationStatus
from app.models.job import Job, ModerationStatus
from app.models.skill import Skill
from app.models.project import Project
from app.models.sandbox import SandboxChallenge
from app.models.admin import UserAudit, FlaggedActivity, FlagStatus

class AdminRepository:
    def __init__(self, db: Session):
        self.db = db

    # --- FEATURE 36: USER MANAGEMENT ---
    def get_users(
        self,
        role: Optional[UserRole] = None,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[User], int]:
        query = self.db.query(User)

        if role:
            query = query.filter(User.role == role)

        if is_active is not None:
            query = query.filter(User.is_active == is_active)

        if search:
            pattern = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    User.full_name.ilike(pattern),
                    User.email.ilike(pattern),
                    User.phone.ilike(pattern)
                )
            )

        total = query.count()
        offset = (page - 1) * page_size
        users = query.order_by(User.created_at.desc()).offset(offset).limit(page_size).all()
        return users, total

    def update_user_status(self, user_id: str, is_active: bool, admin_id: str, notes: Optional[str] = None) -> Optional[User]:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        user.is_active = is_active
        action_text = "ACCOUNT_ACTIVATED" if is_active else "ACCOUNT_SUSPENDED"

        audit = UserAudit(
            user_id=user_id,
            admin_id=admin_id,
            action=action_text,
            notes=notes
        )
        self.db.add(audit)

        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user_role(self, user_id: str, role: UserRole, admin_id: str) -> Optional[User]:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        user.role = role
        audit = UserAudit(
            user_id=user_id,
            admin_id=admin_id,
            action=f"ROLE_CHANGED_TO_{role.value}"
        )
        self.db.add(audit)

        self.db.commit()
        self.db.refresh(user)
        return user

    # --- FEATURE 37 & 38: RECRUITER VERIFICATION & JOB MODERATION ---
    def get_companies(
        self,
        status: Optional[VerificationStatus] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Company], int]:
        query = self.db.query(Company)

        if status:
            query = query.filter(Company.verification_status == status)

        if search:
            pattern = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Company.name.ilike(pattern),
                    Company.email.ilike(pattern),
                    Company.industry.ilike(pattern)
                )
            )

        total = query.count()
        offset = (page - 1) * page_size
        companies = query.order_by(Company.created_at.desc()).offset(offset).limit(page_size).all()
        return companies, total

    def update_company_status(
        self,
        company_id: str,
        status: VerificationStatus,
        notes: Optional[str] = None
    ) -> Optional[Company]:
        company = self.db.query(Company).filter(Company.id == company_id).first()
        if not company:
            return None

        company.verification_status = status
        if notes:
            company.verification_notes = notes

        self.db.commit()
        self.db.refresh(company)
        return company

    def get_jobs_for_moderation(
        self,
        moderation_status: Optional[ModerationStatus] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Job], int]:
        query = self.db.query(Job)

        if moderation_status:
            query = query.filter(Job.moderation_status == moderation_status)

        if search:
            pattern = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Job.title.ilike(pattern),
                    Job.description.ilike(pattern),
                    Job.job_category.ilike(pattern)
                )
            )

        total = query.count()
        offset = (page - 1) * page_size
        jobs = query.order_by(Job.created_at.desc()).offset(offset).limit(page_size).all()
        return jobs, total

    def update_job_moderation(
        self,
        job_id: str,
        moderation_status: ModerationStatus,
        notes: Optional[str] = None
    ) -> Optional[Job]:
        job = self.db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return None

        job.moderation_status = moderation_status
        if notes:
            job.moderation_notes = notes

        self.db.commit()
        self.db.refresh(job)
        return job

    # --- FEATURE 41: FLAGGED ACTIVITY QUEUE ---
    def get_flagged_activities(
        self,
        status: Optional[FlagStatus] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[FlaggedActivity], int]:
        query = self.db.query(FlaggedActivity)

        if status:
            query = query.filter(FlaggedActivity.status == status)

        total = query.count()
        offset = (page - 1) * page_size
        flags = query.order_by(FlaggedActivity.risk_score.desc(), FlaggedActivity.created_at.desc()).offset(offset).limit(page_size).all()
        return flags, total

    def resolve_flagged_activity(
        self,
        flag_id: str,
        status: FlagStatus,
        admin_id: str,
        notes: Optional[str] = None
    ) -> Optional[FlaggedActivity]:
        flag = self.db.query(FlaggedActivity).filter(FlaggedActivity.id == flag_id).first()
        if not flag:
            return None

        flag.status = status
        flag.resolved_by = admin_id
        if notes:
            flag.resolution_notes = notes

        self.db.commit()
        self.db.refresh(flag)
        return flag

    # --- FEATURE 40: TELEMETRY & ANALYTICS ---
    def get_metrics(self) -> dict:
        pending_comp = self.db.query(Company).filter(Company.verification_status == VerificationStatus.PENDING).count()
        verified_comp = self.db.query(Company).filter(Company.verification_status == VerificationStatus.VERIFIED).count()
        rejected_comp = self.db.query(Company).filter(Company.verification_status == VerificationStatus.REJECTED).count()
        total_comp = self.db.query(Company).count()

        total_jobs = self.db.query(Job).count()
        flagged_jobs = self.db.query(Job).filter(Job.moderation_status == ModerationStatus.FLAGGED).count()
        total_skills = self.db.query(Skill).count()

        total_users = self.db.query(User).count()
        active_students = self.db.query(User).filter(User.role == UserRole.STUDENT, User.is_active == True).count()
        active_recruiters = self.db.query(User).filter(User.role == UserRole.RECRUITER, User.is_active == True).count()
        flagged_pending = self.db.query(FlaggedActivity).filter(FlaggedActivity.status == FlagStatus.PENDING).count()

        total_projects = self.db.query(Project).count()
        sandbox_count = self.db.query(SandboxChallenge).count()

        return {
            "pending_verifications": pending_comp,
            "verified_companies": verified_comp,
            "rejected_companies": rejected_comp,
            "total_companies": total_comp,
            "total_jobs": total_jobs,
            "flagged_jobs": flagged_jobs,
            "total_skills": total_skills,
            "total_users": total_users,
            "active_students": active_students,
            "active_recruiters": active_recruiters,
            "flagged_activities_pending": flagged_pending,
            "total_projects": total_projects,
            "sandbox_challenges_count": sandbox_count
        }
