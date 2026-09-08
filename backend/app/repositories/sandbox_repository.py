from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.sandbox import SandboxChallenge, SandboxAttempt, SandboxStatus, AttemptStatus

class SandboxRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_challenges(
        self,
        category: Optional[str] = None,
        difficulty: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[SandboxChallenge], int]:
        query = self.db.query(SandboxChallenge).filter(SandboxChallenge.status == SandboxStatus.PUBLISHED)

        if search:
            pattern = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    SandboxChallenge.title.ilike(pattern),
                    SandboxChallenge.description.ilike(pattern),
                    SandboxChallenge.skills.ilike(pattern)
                )
            )

        if category and category.lower() != "all":
            query = query.filter(SandboxChallenge.category.ilike(category.strip()))

        if difficulty:
            query = query.filter(SandboxChallenge.difficulty == difficulty)

        total = query.count()
        offset = (page - 1) * page_size
        challenges = query.order_by(SandboxChallenge.created_at.desc()).offset(offset).limit(page_size).all()
        return challenges, total

    def get_challenge(self, challenge_id: str) -> Optional[SandboxChallenge]:
        return self.db.query(SandboxChallenge).filter(SandboxChallenge.id == challenge_id).first()

    def get_attempt(self, attempt_id: str) -> Optional[SandboxAttempt]:
        return self.db.query(SandboxAttempt).filter(SandboxAttempt.id == attempt_id).first()

    def get_active_attempt(self, challenge_id: str, student_id: str) -> Optional[SandboxAttempt]:
        return self.db.query(SandboxAttempt).filter(
            SandboxAttempt.challenge_id == challenge_id,
            SandboxAttempt.student_id == student_id,
            SandboxAttempt.status == AttemptStatus.STARTED
        ).first()

    def create_attempt(self, attempt: SandboxAttempt) -> SandboxAttempt:
        self.db.add(attempt)
        self.db.commit()
        self.db.refresh(attempt)
        return attempt

    def submit_attempt(self, attempt: SandboxAttempt, submission_text: str) -> SandboxAttempt:
        attempt.submission = submission_text
        attempt.status = AttemptStatus.SUBMITTED
        attempt.submitted_at = attempt.submitted_at or attempt.started_at
        self.db.commit()
        self.db.refresh(attempt)
        return attempt

    def list_my_attempts(self, student_id: str) -> List[SandboxAttempt]:
        return self.db.query(SandboxAttempt).filter(
            SandboxAttempt.student_id == student_id
        ).order_by(SandboxAttempt.started_at.desc()).all()
