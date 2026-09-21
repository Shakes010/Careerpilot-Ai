from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.student import User, StudentProfile
from app.schemas.student import StudentRegister, StudentLogin, AuthResponse, UserResponse, StudentProfileResponse
from app.core.security import verify_password, get_password_hash, create_access_token
from app.services.scoring import compute_student_metrics

router = APIRouter()

@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register_student(student_in: StudentRegister, db: Session = Depends(get_db)):
    # Check existing user
    existing_user = db.query(User).filter(User.email == student_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Create user
    user = User(
        email=student_in.email,
        hashed_password=get_password_hash(student_in.password),
        full_name=student_in.full_name,
        role="student",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create profile with 0 initial scores
    profile = StudentProfile(
        user_id=user.id,
        university=student_in.university or "National Institute of Technology",
        major=student_in.major or "Master of Computer Applications (MCA)",
        career_readiness_score=0,
        applications_sent=0,
        active_opportunities=0,
        assessments_completed=0,
        verified_skills_count=0,
        skill_trust_meter=0.0
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)

    # Compute actual initial metrics from DB
    profile = compute_student_metrics(db, user.id)

    # Generate JWT token
    access_token = create_access_token(subject=user.id)

    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.from_orm(user),
        profile=StudentProfileResponse.from_orm(profile)
    )

@router.post("/login", response_model=AuthResponse)
def login_student(login_in: StudentLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_in.email).first()
    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Account is disabled")

    # Get profile and compute authoritative scores from DB
    profile = compute_student_metrics(db, user.id)

    access_token = create_access_token(subject=user.id)

    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.from_orm(user),
        profile=StudentProfileResponse.from_orm(profile)
    )

@router.get("/me", response_model=AuthResponse)
def get_current_student_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = compute_student_metrics(db, current_user.id)
    token = create_access_token(subject=current_user.id)

    return AuthResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse.from_orm(current_user),
        profile=StudentProfileResponse.from_orm(profile)
    )
