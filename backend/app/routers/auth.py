from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import RecruiterRegisterRequest, RecruiterLoginRequest, TokenResponse, ApiResponse, UserResponse
from app.services.auth_service import AuthService
from app.dependencies.auth import get_current_user, get_current_recruiter
from app.models.user import User
from app.models.recruiter import Recruiter
from app.repositories.company_repository import CompanyRepository

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=ApiResponse[TokenResponse], status_code=status.HTTP_201_CREATED)
@router.post("/recruiter/register", response_model=ApiResponse[TokenResponse], status_code=status.HTTP_201_CREATED)
def register_recruiter(req: RecruiterRegisterRequest, db: Session = Depends(get_db)):
    """Register a new recruiter and associated company (verification status set to PENDING)."""
    service = AuthService(db)
    token_resp = service.register_recruiter(req)
    return ApiResponse(
        success=True,
        data=token_resp,
        message="Recruiter registered successfully. Your company verification is pending."
    )

@router.post("/login", response_model=ApiResponse[TokenResponse])
@router.post("/recruiter/login", response_model=ApiResponse[TokenResponse])
def login_user(req: RecruiterLoginRequest, db: Session = Depends(get_db)):
    """Universal authentication endpoint supporting ADMIN, RECRUITER, and STUDENT logins."""
    service = AuthService(db)
    token_resp = service.login_universal(req)
    return ApiResponse(
        success=True,
        data=token_resp,
        message="Login successful."
    )

@router.get("/me", response_model=ApiResponse[dict])
def get_current_profile(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve currently authenticated user's profile metadata."""
    return ApiResponse(
        success=True,
        data={
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "phone": user.phone,
                "role": user.role.value
            }
        },
        message="Profile retrieved."
    )

@router.post("/logout", response_model=ApiResponse[dict])
def logout():
    """Logout endpoint."""
    return ApiResponse(
        success=True,
        data={},
        message="Logged out successfully."
    )
