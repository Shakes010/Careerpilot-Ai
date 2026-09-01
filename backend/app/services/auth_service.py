from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.models.company import Company, VerificationStatus
from app.models.recruiter import Recruiter
from app.repositories.user_repository import UserRepository
from app.repositories.company_repository import CompanyRepository
from app.repositories.recruiter_repository import RecruiterRepository
from app.schemas.auth import RecruiterRegisterRequest, RecruiterLoginRequest, TokenResponse
from app.core.security import get_password_hash, verify_password, create_access_token

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.company_repo = CompanyRepository(db)
        self.recruiter_repo = RecruiterRepository(db)

    def register_recruiter(self, req: RecruiterRegisterRequest) -> TokenResponse:
        # Check duplicate email
        existing_user = self.user_repo.get_by_email(req.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered. Please login instead."
            )

        # 1. Create Company (PENDING verification status)
        company = Company(
            name=req.company_name.strip(),
            website=req.company_website.strip() if req.company_website else None,
            verification_status=VerificationStatus.PENDING
        )
        company = self.company_repo.create(company)

        # 2. Create User (RECRUITER role)
        user = User(
            email=req.email.lower().strip(),
            password_hash=get_password_hash(req.password),
            full_name=req.full_name.strip(),
            phone=req.phone.strip() if req.phone else None,
            role=UserRole.RECRUITER
        )
        user = self.user_repo.create(user)

        # 3. Create Recruiter profile link
        recruiter = Recruiter(
            user_id=user.id,
            company_id=company.id,
            designation=req.designation.strip() if req.designation else "Hiring Manager"
        )
        recruiter = self.recruiter_repo.create(recruiter)

        # 4. Generate JWT
        token = create_access_token(data={"sub": user.id, "role": user.role.value, "recruiter_id": recruiter.id, "company_id": company.id})

        return TokenResponse(
            access_token=token,
            user_id=user.id,
            email=user.email,
            full_name=user.full_name,
            role=user.role.value,
            company_id=company.id,
            company_name=company.name,
            company_verification_status=company.verification_status.value
        )

    def login_recruiter(self, req: RecruiterLoginRequest) -> TokenResponse:
        user = self.user_repo.get_by_email(req.email)
        if not user or not verify_password(req.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )

        if user.role != UserRole.RECRUITER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Only recruiter accounts can log in here."
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated. Please contact support."
            )

        recruiter = self.recruiter_repo.get_by_user_id(user.id)
        if not recruiter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recruiter profile not found."
            )

        company = self.company_repo.get_by_id(recruiter.company_id)
        company_name = company.name if company else "Company"
        company_status = company.verification_status.value if company else "PENDING"

        token = create_access_token(data={"sub": user.id, "role": user.role.value, "recruiter_id": recruiter.id, "company_id": recruiter.company_id})

        return TokenResponse(
            access_token=token,
            user_id=user.id,
            email=user.email,
            full_name=user.full_name,
            role=user.role.value,
            company_id=recruiter.company_id,
            company_name=company_name,
            company_verification_status=company_status
        )
