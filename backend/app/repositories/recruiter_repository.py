from typing import Optional
from sqlalchemy.orm import Session
from app.models.recruiter import Recruiter

class RecruiterRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, recruiter_id: str) -> Optional[Recruiter]:
        return self.db.query(Recruiter).filter(Recruiter.id == recruiter_id).first()

    def get_by_user_id(self, user_id: str) -> Optional[Recruiter]:
        return self.db.query(Recruiter).filter(Recruiter.user_id == user_id).first()

    def create(self, recruiter: Recruiter) -> Recruiter:
        self.db.add(recruiter)
        self.db.commit()
        self.db.refresh(recruiter)
        return recruiter
