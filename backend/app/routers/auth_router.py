from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.database import get_db
import app.models as models
from app.schemas.profile_schemas import UserRegisterRequest, UserLoginRequest, TokenResponse, UserOut
from app.services.auth_service import (
    get_password_hash, verify_password, create_access_token, check_eligibility, get_current_user
)

router = APIRouter(prefix="/auth", tags=["Auth"])

class UpdateAccountSettingsRequest(BaseModel):
    email: Optional[EmailStr] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None


@router.post("/register", response_model=TokenResponse)
def register_user(req: UserRegisterRequest, db: Session = Depends(get_db)):
    if req.role == models.UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin accounts cannot be registered via public registration.")

    if any(char.isdigit() for char in (req.full_name or "")):
        raise HTTPException(status_code=400, detail="Full name cannot contain numbers or numeric digits.")

    existing = db.query(models.User).filter(models.User.email == req.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    # Check eligibility rule for students: strictly IT background & recent pass-outs
    is_eligible = True
    if req.role == models.UserRole.student:
        is_eligible = check_eligibility(req.degree, req.graduation_year)
        if not is_eligible:
            raise HTTPException(
                status_code=400,
                detail="Registration restricted: CareerPilot AI is strictly reserved for candidates with an IT/Computer Science background graduated in recent years (Classes of 2023–2028)."
            )

    hashed_pw = get_password_hash(req.password)
    user = models.User(
        email=req.email,
        password_hash=hashed_pw,
        role=req.role,
        full_name=req.full_name.strip(),
        phone=req.phone,
        is_verified=True,
        is_active=True
    )
    db.add(user)
    db.flush()

    if req.role == models.UserRole.student:
        student_prof = models.StudentProfile(
            user_id=user.id,
            phone=req.phone,
            degree=req.degree,
            graduation_year=req.graduation_year,
            college_name=req.college_name,
            is_eligible=is_eligible,
            profile_completion_pct=30 if (req.degree and req.graduation_year) else 15
        )
        db.add(student_prof)
        db.flush()

    db.commit()
    db.refresh(user)

    token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": str(user.id),
        "role": user.role.value,
        "full_name": user.full_name,
        "email": user.email,
        "is_eligible": is_eligible,
        "is_premium": False
    }

@router.post("/login", response_model=TokenResponse)
def login_user(req: UserLoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="User account is deactivated")

    is_eligible = True
    is_premium = False
    if user.student_profile:
        is_eligible = user.student_profile.is_eligible
        is_premium = bool(user.student_profile.is_premium)

    token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": str(user.id),
        "role": user.role.value,
        "full_name": user.full_name,
        "email": user.email,
        "is_eligible": is_eligible,
        "is_premium": is_premium
    }

@router.get("/me")
def get_current_user_profile(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_data = {
        "id": str(current_user.id),
        "email": current_user.email,
        "role": current_user.role.value,
        "full_name": current_user.full_name,
        "phone": current_user.phone,
        "profile_photo_url": current_user.profile_photo_url,
        "is_verified": current_user.is_verified,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None
    }

    if current_user.role == models.UserRole.student and current_user.student_profile:
        sp = current_user.student_profile
        user_data["student_profile"] = {
            "id": str(sp.id),
            "phone": sp.phone,
            "location": sp.location,
            "college_name": sp.college_name,
            "degree": sp.degree,
            "graduation_year": sp.graduation_year,
            "cgpa": float(sp.cgpa) if sp.cgpa else None,
            "career_goal": sp.career_goal,
            "bio": sp.bio,
            "profile_completion_pct": sp.profile_completion_pct,
            "is_eligible": sp.is_eligible,
            "is_premium": bool(sp.is_premium)
        }

    return user_data

@router.put("/account-settings")
def update_account_settings(
    req: UpdateAccountSettingsRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if req.email and req.email != current_user.email:
        existing = db.query(models.User).filter(models.User.email == req.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="This email address is already in use")
        current_user.email = req.email

    if req.new_password:
        if not req.current_password:
            raise HTTPException(status_code=400, detail="Current password is required to change password")
        if not verify_password(req.current_password, current_user.password_hash):
            raise HTTPException(status_code=400, detail="Current password is incorrect")
        current_user.password_hash = get_password_hash(req.new_password)

    if req.full_name is not None:
        if any(char.isdigit() for char in req.full_name):
            raise HTTPException(status_code=400, detail="Full name cannot contain numbers or numeric digits.")
        current_user.full_name = req.full_name.strip()
    if req.phone is not None:
        current_user.phone = req.phone

    db.commit()
    db.refresh(current_user)

    return {
        "user_id": str(current_user.id),
        "email": current_user.email,
        "full_name": current_user.full_name,
        "phone": current_user.phone,
        "message": "Account settings updated successfully!"
    }
