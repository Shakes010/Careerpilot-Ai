from typing import List, Tuple
from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.sandbox import SandboxChallenge, SandboxAttempt, AttemptStatus
from app.repositories.sandbox_repository import SandboxRepository
from app.schemas.sandbox import ChallengeResponse, AttemptResponse, AttemptSubmitRequest

class SandboxService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = SandboxRepository(db)

    def list_challenges(self, search: str = None, category: str = None, difficulty: str = None, page: int = 1, page_size: int = 20) -> Tuple[List[ChallengeResponse], int]:
        challenges, total = self.repo.list_challenges(search=search, category=category, difficulty=difficulty, page=page, page_size=page_size)
        return [ChallengeResponse.model_validate(c) for c in challenges], total

    def get_challenge_details(self, challenge_id: str) -> ChallengeResponse:
        ch = self.repo.get_challenge(challenge_id)
        if not ch:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandbox challenge not found.")
        return ChallengeResponse.model_validate(ch)

    def start_attempt(self, student_id: str, challenge_id: str) -> AttemptResponse:
        ch = self.repo.get_challenge(challenge_id)
        if not ch:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandbox challenge not found.")

        # Check existing active attempt
        active = self.repo.get_active_attempt(challenge_id, student_id)
        if active:
            return self._format_attempt(active)

        attempt = SandboxAttempt(
            challenge_id=challenge_id,
            student_id=student_id,
            status=AttemptStatus.STARTED
        )
        created = self.repo.create_attempt(attempt)
        return self._format_attempt(created)

    def get_attempt_details(self, student_id: str, attempt_id: str) -> AttemptResponse:
        attempt = self.repo.get_attempt(attempt_id)
        if not attempt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found.")

        if attempt.student_id != student_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this challenge attempt.")

        return self._format_attempt(attempt)

    def submit_attempt(self, student_id: str, attempt_id: str, req: AttemptSubmitRequest) -> AttemptResponse:
        attempt = self.repo.get_attempt(attempt_id)
        if not attempt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found.")

        if attempt.student_id != student_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot submit an attempt for another user.")

        attempt.submitted_at = datetime.now(timezone.utc)
        attempt.feedback = "Your submission has been received. Evaluation will be connected to the assessment system."
        submitted = self.repo.submit_attempt(attempt, req.submission)
        return self._format_attempt(submitted)

    def list_my_attempts(self, student_id: str) -> List[AttemptResponse]:
        attempts = self.repo.list_my_attempts(student_id)
        return [self._format_attempt(a) for a in attempts]

    def _format_attempt(self, a: SandboxAttempt) -> AttemptResponse:
        return AttemptResponse(
            id=a.id,
            challenge_id=a.challenge_id,
            challenge_title=a.challenge.title if a.challenge else "",
            student_id=a.student_id,
            started_at=a.started_at,
            submitted_at=a.submitted_at,
            status=a.status,
            score=a.score,
            feedback=a.feedback,
            submission=a.submission
        )
