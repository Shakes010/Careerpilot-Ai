from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import ApiResponse
from app.schemas.sandbox import ChallengeResponse, AttemptResponse, AttemptSubmitRequest
from app.models.user import User
from app.services.sandbox_service import SandboxService
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/career-sandbox", tags=["Career Sandbox"])

@router.get("/challenges", response_model=ApiResponse[dict])
def list_challenges(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Browse published Career Sandbox challenges."""
    service = SandboxService(db)
    challenges, total = service.list_challenges(
        search=search,
        category=category,
        difficulty=difficulty,
        page=page,
        page_size=page_size
    )
    return ApiResponse(
        success=True,
        data={
            "challenges": [c.model_dump() for c in challenges],
            "pagination": {"total": total, "page": page, "page_size": page_size}
        },
        message="Sandbox challenges loaded."
    )

@router.get("/challenges/{challenge_id}", response_model=ApiResponse[ChallengeResponse])
def get_challenge_details(
    challenge_id: str,
    db: Session = Depends(get_db)
):
    """Get challenge details and instructions."""
    service = SandboxService(db)
    ch = service.get_challenge_details(challenge_id)
    return ApiResponse(
        success=True,
        data=ch,
        message="Challenge details loaded."
    )

@router.post("/challenges/{challenge_id}/start", response_model=ApiResponse[AttemptResponse])
def start_attempt(
    challenge_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a new attempt on a sandbox challenge."""
    service = SandboxService(db)
    attempt = service.start_attempt(current_user.id, challenge_id)
    return ApiResponse(
        success=True,
        data=attempt,
        message="Challenge attempt started."
    )

@router.get("/attempts/{attempt_id}", response_model=ApiResponse[AttemptResponse])
def get_attempt_details(
    attempt_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get details of an ongoing or submitted attempt."""
    service = SandboxService(db)
    attempt = service.get_attempt_details(current_user.id, attempt_id)
    return ApiResponse(
        success=True,
        data=attempt,
        message="Attempt details loaded."
    )

@router.post("/attempts/{attempt_id}/submit", response_model=ApiResponse[AttemptResponse])
def submit_attempt(
    attempt_id: str,
    req: AttemptSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit code / solution for evaluation."""
    service = SandboxService(db)
    attempt = service.submit_attempt(current_user.id, attempt_id, req)
    return ApiResponse(
        success=True,
        data=attempt,
        message="Submission received for evaluation."
    )

@router.get("/my-attempts", response_model=ApiResponse[List[AttemptResponse]])
def list_my_attempts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all sandbox attempts for current student."""
    service = SandboxService(db)
    attempts = service.list_my_attempts(current_user.id)
    return ApiResponse(
        success=True,
        data=attempts,
        message="My sandbox attempts loaded."
    )
