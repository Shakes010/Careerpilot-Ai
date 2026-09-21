import os
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.session import get_db
from app.api.deps import get_current_user
from app.core.config import settings
from app.models.student import (
    User, 
    StudentProfile, 
    StudentEducation, 
    StudentSkill, 
    StudentResume,
    StudentResumeVersion,
    StudentCertificate,
    StudentGithubProfile,
    StudentGithubRepository,
    StudentTimelineEvent,
    StudentCareerPreference, 
    Job, 
    JobApplication, 
    LearningResource
)
from app.schemas.student import (
    UserResponse,
    StudentProfileResponse,
    StudentProfileUpdate,
    StudentEducationCreate,
    StudentEducationUpdate,
    StudentEducationResponse,
    StudentSkillCreate,
    StudentSkillUpdate,
    StudentSkillResponse,
    StudentResumeResponse,
    CareerPreferenceCreateOrUpdate,
    CareerPreferenceResponse,
    JobResponse,
    SkillGapItem,
    LearningResourceResponse,
    JobApplicationCreate,
    JobApplicationUpdateStatus,
    JobApplicationResponse,
    ApplicationStatusSummary,
    StudentDashboardSummary,
    StudentResumeVersionCreate,
    StudentResumeVersionUpdate,
    StudentResumeVersionResponse,
    StudentCertificateCreate,
    StudentCertificateUpdate,
    StudentCertificateResponse,
    GithubConnectRequest,
    StudentGithubProfileResponse,
    StudentGithubRepositoryResponse,
    StudentTimelineEventResponse,
    CareerPassportResponse,
    AIGeneratedResumeData,
    AISaveResumeRequest
)
from app.services.resume_validator import (
    extract_text_from_file,
    validate_resume_text,
    calculate_ats_score
)
from app.services.scoring import compute_student_metrics
from app.services.github_service import fetch_github_user_data
from app.services.timeline_service import log_timeline_event
from app.services.resume_generator import generate_non_paid_resume

router = APIRouter()


# -------------------------------------------------------------
# 1. STUDENT DASHBOARD
# -------------------------------------------------------------
@router.get("/dashboard", response_model=StudentDashboardSummary)
def get_student_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = compute_student_metrics(db, current_user.id)
    educations = db.query(StudentEducation).filter(StudentEducation.student_id == current_user.id).all()
    skills = db.query(StudentSkill).filter(StudentSkill.student_id == current_user.id).all()
    resume = db.query(StudentResume).filter(StudentResume.student_id == current_user.id).order_by(StudentResume.uploaded_at.desc()).first()
    pref = db.query(StudentCareerPreference).filter(StudentCareerPreference.student_id == current_user.id).first()
    applications = db.query(JobApplication).filter(JobApplication.student_id == current_user.id).all()

    # Application Statistics
    applied_count = len(applications)
    under_review = sum(1 for a in applications if a.status == "Under Review")
    interviewed = sum(1 for a in applications if a.status == "Interviewed")
    accepted = sum(1 for a in applications if a.status == "Accepted")
    rejected = sum(1 for a in applications if a.status == "Rejected")

    # Update profile applications_sent count
    profile.applications_sent = applied_count
    db.commit()
    db.refresh(profile)

    completion_pct = profile.career_readiness_score

    # Skill Gap Summary
    all_jobs = db.query(Job).filter(Job.is_active == True).all()
    student_skill_names = set(s.skill_name.lower().strip() for s in skills)
    target_role = pref.preferred_role if pref else "Software Engineer"
    all_req_skills = set()
    for job in all_jobs[:3]:
        all_req_skills.update(job.required_skills.split(","))
    
    req_skills_clean = [s.strip() for s in all_req_skills if s.strip()]
    exist_skills_clean = [s.skill_name for s in skills]
    missing_skills_clean = [s for s in req_skills_clean if s.lower() not in student_skill_names]
    
    match_pct = int((len(exist_skills_clean) / max(1, len(req_skills_clean))) * 100) if req_skills_clean else 75
    
    skill_gap_sum = SkillGapItem(
        target_role=target_role,
        existing_skills=exist_skills_clean,
        required_skills=req_skills_clean[:6],
        missing_skills=missing_skills_clean[:4],
        match_percentage=min(100, max(40, match_pct))
    )

    # Dynamic AI Recommendations
    ai_recs = []
    if missing_skills_clean:
        ai_recs.append(f"Recommended Learning: Learn {missing_skills_clean[0]} to increase your career match score by +15%.")
    else:
        ai_recs.append("Great job! You possess all primary skills required for your target roles.")
    
    if not resume:
        ai_recs.append("Upload your latest PDF resume to unlock personalized ATS score breakdown and employer visibility.")
    else:
        ai_recs.append(f"Resume ATS Score is currently {resume.ats_score}%. Keep skills updated to boost visibility.")
    
    if completion_pct < 90:
        ai_recs.append(f"Your profile completion is at {completion_pct}%. Complete remaining contact & project sections to reach 100%.")

    return StudentDashboardSummary(
        user=UserResponse.from_orm(current_user),
        profile=StudentProfileResponse.from_orm(profile),
        completion_percentage=completion_pct,
        education_count=len(educations),
        skills_count=len(skills),
        resumes_count=1 if resume else 0,
        career_preference=CareerPreferenceResponse.from_orm(pref) if pref else None,
        application_summary=ApplicationStatusSummary(
            applied=applied_count,
            under_review=under_review,
            interviewed=interviewed,
            accepted=accepted,
            rejected=rejected
        ),
        skill_gap_summary=skill_gap_sum,
        ai_recommendations=ai_recs
    )


# -------------------------------------------------------------
# 2. STUDENT PROFILE MANAGEMENT
# -------------------------------------------------------------
@router.get("/profile", response_model=StudentProfileResponse)
def get_student_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = compute_student_metrics(db, current_user.id)
    return StudentProfileResponse.from_orm(profile)

@router.put("/profile", response_model=StudentProfileResponse)
def update_student_profile(
    profile_in: StudentProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        profile = StudentProfile(user_id=current_user.id)
        db.add(profile)

    update_data = profile_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)

    profile.updated_at = datetime.utcnow()
    db.commit()
    profile = compute_student_metrics(db, current_user.id)
    return StudentProfileResponse.from_orm(profile)

@router.post("/profile/picture", response_model=StudentProfileResponse)
async def upload_student_profile_picture(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate allowed image extensions
    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    filename = file.filename or "profile.jpg"
    ext = os.path.splitext(filename)[1].lower()

    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image format. Please upload a JPG, JPEG, PNG, or WEBP image."
        )

    # Validate file size (max 5 MB)
    contents = await file.read()
    max_size = 5 * 1024 * 1024
    if len(contents) > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image size exceeds the 5MB limit. Please choose a smaller image."
        )

    # Ensure storage directory exists
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    uploads_dir = os.path.join(base_dir, "uploads", "profile_pictures")
    os.makedirs(uploads_dir, exist_ok=True)

    # Generate unique filename for user
    timestamp = int(datetime.utcnow().timestamp() * 1000)
    saved_filename = f"user_{current_user.id}_{timestamp}{ext}"
    saved_path = os.path.join(uploads_dir, saved_filename)

    with open(saved_path, "wb") as f:
        f.write(contents)

    picture_url = f"/uploads/profile_pictures/{saved_filename}"

    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        profile = StudentProfile(user_id=current_user.id)
        db.add(profile)

    profile.profile_picture = picture_url
    profile.updated_at = datetime.utcnow()
    db.commit()
    profile = compute_student_metrics(db, current_user.id)

    return StudentProfileResponse.from_orm(profile)


# -------------------------------------------------------------
# 3. EDUCATION CRUD
# -------------------------------------------------------------
@router.get("/education", response_model=List[StudentEducationResponse])
def get_student_educations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(StudentEducation).filter(StudentEducation.student_id == current_user.id).order_by(StudentEducation.start_year.desc()).all()

@router.post("/education", response_model=StudentEducationResponse, status_code=status.HTTP_201_CREATED)
def create_student_education(
    edu_in: StudentEducationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    edu = StudentEducation(
        student_id=current_user.id,
        **edu_in.dict()
    )
    db.add(edu)
    db.commit()
    db.refresh(edu)
    log_timeline_event(
        db,
        current_user.id,
        title=f"Added Education: {edu.degree}",
        description=f"Studied {edu.degree} at {edu.institution} ({edu.start_year} - {edu.end_year or 'Present'})",
        category="Education"
    )
    compute_student_metrics(db, current_user.id)
    return StudentEducationResponse.from_orm(edu)


@router.put("/education/{education_id}", response_model=StudentEducationResponse)
def update_student_education(
    education_id: int,
    edu_in: StudentEducationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    edu = db.query(StudentEducation).filter(
        StudentEducation.id == education_id,
        StudentEducation.student_id == current_user.id
    ).first()
    if not edu:
        raise HTTPException(status_code=404, detail="Education record not found")

    update_data = edu_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(edu, field, value)

    db.commit()
    db.refresh(edu)
    compute_student_metrics(db, current_user.id)
    return StudentEducationResponse.from_orm(edu)

@router.delete("/education/{education_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_education(
    education_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    edu = db.query(StudentEducation).filter(
        StudentEducation.id == education_id,
        StudentEducation.student_id == current_user.id
    ).first()
    if not edu:
        raise HTTPException(status_code=404, detail="Education record not found")

    db.delete(edu)
    db.commit()
    compute_student_metrics(db, current_user.id)
    return None


# -------------------------------------------------------------
# 4. SKILLS CRUD
# -------------------------------------------------------------
@router.get("/skills", response_model=List[StudentSkillResponse])
def get_student_skills(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(StudentSkill).filter(StudentSkill.student_id == current_user.id).order_by(StudentSkill.created_at.desc()).all()

@router.post("/skills", response_model=StudentSkillResponse, status_code=status.HTTP_201_CREATED)
def add_student_skill(
    skill_in: StudentSkillCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Prevent exact duplicate skill name for same student
    existing = db.query(StudentSkill).filter(
        StudentSkill.student_id == current_user.id,
        StudentSkill.skill_name.ilike(skill_in.skill_name.strip())
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Skill already exists in your profile")

    skill = StudentSkill(
        student_id=current_user.id,
        skill_name=skill_in.skill_name.strip(),
        category=skill_in.category or "Programming Languages",
        proficiency=skill_in.proficiency or "Intermediate",
        is_verified=skill_in.is_verified if skill_in.is_verified is not None else True
    )
    db.add(skill)
    db.commit()
    db.refresh(skill)

    log_timeline_event(
        db,
        current_user.id,
        title=f"Added Skill: {skill.skill_name}",
        description=f"Added {skill.skill_name} ({skill.proficiency}) in category {skill.category}.",
        category="Skill"
    )

    # Recompute student metrics from DB
    compute_student_metrics(db, current_user.id)

    return StudentSkillResponse.from_orm(skill)


@router.put("/skills/{skill_id}", response_model=StudentSkillResponse)
def update_student_skill(
    skill_id: int,
    skill_in: StudentSkillUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    skill = db.query(StudentSkill).filter(
        StudentSkill.id == skill_id,
        StudentSkill.student_id == current_user.id
    ).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    update_data = skill_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(skill, field, value)

    db.commit()
    db.refresh(skill)

    # Recompute student metrics from DB
    compute_student_metrics(db, current_user.id)

    return StudentSkillResponse.from_orm(skill)

@router.delete("/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_skill(
    skill_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    skill = db.query(StudentSkill).filter(
        StudentSkill.id == skill_id,
        StudentSkill.student_id == current_user.id
    ).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    db.delete(skill)
    db.commit()

    # Recompute student metrics from DB
    compute_student_metrics(db, current_user.id)

    return None


# -------------------------------------------------------------
# 5. RESUME MANAGEMENT
# -------------------------------------------------------------
@router.get("/resume", response_model=Optional[StudentResumeResponse])
def get_student_resume(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resume = db.query(StudentResume).filter(
        StudentResume.student_id == current_user.id
    ).order_by(StudentResume.uploaded_at.desc()).first()
    if not resume:
        return None
    return StudentResumeResponse.from_orm(resume)

@router.post("/resume/upload", response_model=StudentResumeResponse)
async def upload_student_resume(
    file: Optional[UploadFile] = File(None),
    summary: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    skill_count = db.query(StudentSkill).filter(StudentSkill.student_id == current_user.id).count()
    edu_count = db.query(StudentEducation).filter(StudentEducation.student_id == current_user.id).count()

    filename = "Student_Resume.pdf"
    file_type = "application/pdf"
    file_size = 250000
    file_path = f"/uploads/resumes/user_{current_user.id}_resume.pdf"
    extracted_text = ""

    if file:
        filename = file.filename
        file_type = file.content_type or "application/pdf"
        lower_name = filename.lower()
        # Validate file format
        if not (lower_name.endswith('.pdf') or lower_name.endswith('.docx') or lower_name.endswith('.doc')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file format. Please upload a PDF or Word document (.pdf, .docx)."
            )
        contents = await file.read()
        file_size = len(contents)
        if file_size == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The uploaded document contains insufficient text or is unreadable. Please upload a valid text-based PDF or DOCX resume."
            )
        extracted_text = extract_text_from_file(contents, filename)
    elif summary:
        extracted_text = summary
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No resume file or summary provided. Please upload a valid resume."
        )

    # Validate extracted text content against non-resume documents and structural criteria
    is_valid, err_msg = validate_resume_text(extracted_text)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err_msg or "The uploaded document does not appear to be a valid resume/CV. Please upload your resume in PDF format."
        )

    # Calculate dynamic ATS score and parsed summary based on validated content
    ats_score, parsed_summary = calculate_ats_score(
        extracted_text,
        user_full_name=current_user.full_name,
        profile_skills_count=skill_count,
        profile_edu_count=edu_count
    )

    resume_summary = summary or parsed_summary or f"Resume uploaded for {current_user.full_name}."

    # Save to disk if file was uploaded
    if file:
        try:
            os.makedirs("uploads/resumes", exist_ok=True)
            file_path = f"uploads/resumes/user_{current_user.id}_{filename}"
            with open(file_path, "wb") as f:
                f.write(contents)
        except Exception:
            pass

    # Unset active on all existing versions for this student
    db.query(StudentResumeVersion).filter(
        StudentResumeVersion.student_id == current_user.id
    ).update({"is_active": False})

    # Create new version record
    new_version = StudentResumeVersion(
        student_id=current_user.id,
        title=f"Uploaded Resume - {filename}",
        filename=filename,
        file_path=file_path,
        file_type=file_type,
        file_size=file_size,
        summary=resume_summary,
        ats_score=ats_score,
        is_active=True,
        status="Active",
        source="Uploaded"
    )
    db.add(new_version)

    # Overwrite previous active resume record or create new for StudentResume table
    existing_resume = db.query(StudentResume).filter(StudentResume.student_id == current_user.id).first()
    if existing_resume:
        existing_resume.filename = filename
        existing_resume.file_type = file_type
        existing_resume.file_size = file_size
        existing_resume.file_path = file_path
        existing_resume.summary = resume_summary
        existing_resume.ats_score = ats_score
        existing_resume.uploaded_at = datetime.utcnow()
    else:
        existing_resume = StudentResume(
            student_id=current_user.id,
            filename=filename,
            file_path=file_path,
            file_type=file_type,
            file_size=file_size,
            summary=resume_summary,
            ats_score=ats_score
        )
        db.add(existing_resume)

    db.commit()
    db.refresh(existing_resume)

    # Log timeline event
    log_timeline_event(
        db, 
        current_user.id, 
        title="Resume Uploaded", 
        description=f"Uploaded new resume document '{filename}' with ATS score {ats_score}%.", 
        category="Resume"
    )

    compute_student_metrics(db, current_user.id)
    return StudentResumeResponse.from_orm(existing_resume)


@router.delete("/resume/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resume = db.query(StudentResume).filter(
        StudentResume.id == resume_id,
        StudentResume.student_id == current_user.id
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume record not found")

    db.delete(resume)
    db.commit()
    compute_student_metrics(db, current_user.id)
    return None


# -------------------------------------------------------------
# 6. CAREER PREFERENCES
# -------------------------------------------------------------
@router.get("/preferences", response_model=Optional[CareerPreferenceResponse])
def get_career_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pref = db.query(StudentCareerPreference).filter(
        StudentCareerPreference.student_id == current_user.id
    ).first()
    if not pref:
        return None
    return CareerPreferenceResponse.from_orm(pref)

@router.put("/preferences", response_model=CareerPreferenceResponse)
def save_career_preferences(
    pref_in: CareerPreferenceCreateOrUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pref = db.query(StudentCareerPreference).filter(
        StudentCareerPreference.student_id == current_user.id
    ).first()
    
    if not pref:
        pref = StudentCareerPreference(student_id=current_user.id, **pref_in.dict())
        db.add(pref)
    else:
        for field, value in pref_in.dict().items():
            setattr(pref, field, value)
        pref.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(pref)
    compute_student_metrics(db, current_user.id)
    return CareerPreferenceResponse.from_orm(pref)



# -------------------------------------------------------------
# 8. SKILL-GAP ANALYSIS
# -------------------------------------------------------------
@router.get("/skill-gap", response_model=SkillGapItem)
def get_skill_gap_analysis(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    skills = db.query(StudentSkill).filter(StudentSkill.student_id == current_user.id).all()
    pref = db.query(StudentCareerPreference).filter(StudentCareerPreference.student_id == current_user.id).first()
    
    target_role = pref.preferred_role if pref else "Full Stack Engineer"

    # Gather required skills from active job catalog matching the target role or overall industry
    catalog_jobs = db.query(Job).filter(Job.is_active == True).all()
    required_skills_set = set()
    for job in catalog_jobs:
        for sk in job.required_skills.split(","):
            if sk.strip():
                required_skills_set.add(sk.strip())

    req_list = list(required_skills_set) if required_skills_set else ["Python", "FastAPI", "Vue.js", "PostgreSQL", "Docker", "Git"]
    existing_list = [s.skill_name for s in skills]
    existing_lower = set(s.skill_name.lower().strip() for s in skills)

    missing_list = [s for s in req_list if s.lower().strip() not in existing_lower]

    match_pct = int((len(existing_list) / max(1, len(req_list))) * 100)

    return SkillGapItem(
        target_role=target_role,
        existing_skills=existing_list,
        required_skills=req_list[:8],
        missing_skills=missing_list[:5],
        match_percentage=min(100, max(35, match_pct))
    )


# -------------------------------------------------------------
# 9. LEARNING RECOMMENDATIONS
# -------------------------------------------------------------
@router.get("/learning-recommendations", response_model=List[LearningResourceResponse])
def get_learning_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Find student's missing skills
    skills = db.query(StudentSkill).filter(StudentSkill.student_id == current_user.id).all()
    existing_lower = set(s.skill_name.lower().strip() for s in skills)

    # Get all learning resources
    resources = db.query(LearningResource).all()

    # Prioritize resources for skills student doesn't have yet
    recommended = []
    for res in resources:
        if res.skill_name.lower().strip() not in existing_lower:
            recommended.append(res)

    # If student has all skills or list is short, append remaining resources
    if len(recommended) < 3:
        for res in resources:
            if res not in recommended:
                recommended.append(res)

    return [LearningResourceResponse.from_orm(r) for r in recommended]


# -------------------------------------------------------------
# 10. JOB APPLICATION TRACKING
# -------------------------------------------------------------
@router.get("/applications", response_model=List[JobApplicationResponse])
def get_student_applications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    apps = db.query(JobApplication).filter(JobApplication.student_id == current_user.id).order_by(JobApplication.application_date.desc()).all()
    return [JobApplicationResponse.from_orm(a) for a in apps]

@router.post("/applications", response_model=JobApplicationResponse, status_code=status.HTTP_201_CREATED)
def apply_for_job(
    app_in: JobApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify job exists
    job = db.query(Job).filter(Job.id == app_in.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Prevent double application
    existing_app = db.query(JobApplication).filter(
        JobApplication.student_id == current_user.id,
        JobApplication.job_id == app_in.job_id
    ).first()
    if existing_app:
        raise HTTPException(status_code=400, detail="You have already applied for this position")

    new_app = JobApplication(
        student_id=current_user.id,
        job_id=app_in.job_id,
        status="Applied",
        notes=app_in.notes or f"Application submitted on {datetime.now().strftime('%b %d, %Y')}"
    )
    db.add(new_app)
    
    # Increment profile application count
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if profile:
        profile.applications_sent += 1

    db.commit()
    db.refresh(new_app)
    return JobApplicationResponse.from_orm(new_app)

@router.put("/applications/{application_id}/status", response_model=JobApplicationResponse)
def update_application_status(
    application_id: int,
    status_in: JobApplicationUpdateStatus,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    app_obj = db.query(JobApplication).filter(
        JobApplication.id == application_id,
        JobApplication.student_id == current_user.id
    ).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application record not found")

    app_obj.status = status_in.status
    if status_in.notes:
        app_obj.notes = status_in.notes

    db.commit()
    db.refresh(app_obj)
    return JobApplicationResponse.from_orm(app_obj)

@router.delete("/applications/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def withdraw_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    app_obj = db.query(JobApplication).filter(
        JobApplication.id == application_id,
        JobApplication.student_id == current_user.id
    ).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application record not found")

    db.delete(app_obj)

    # Decrement profile applications count
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if profile and profile.applications_sent > 0:
        profile.applications_sent -= 1

    db.commit()
    return None


# =============================================================
# 1. SMART RESUME VERSION MANAGER ENDPOINTS
# =============================================================
@router.get("/resume-versions", response_model=List[StudentResumeVersionResponse])
def get_resume_versions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    versions = db.query(StudentResumeVersion).filter(
        StudentResumeVersion.student_id == current_user.id
    ).order_by(StudentResumeVersion.created_at.desc()).all()
    return versions

@router.post("/resume-versions", response_model=StudentResumeVersionResponse, status_code=status.HTTP_201_CREATED)
def create_resume_version(
    version_in: StudentResumeVersionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Unset active status on all existing versions
    db.query(StudentResumeVersion).filter(
        StudentResumeVersion.student_id == current_user.id
    ).update({"is_active": False})

    new_v = StudentResumeVersion(
        student_id=current_user.id,
        title=version_in.title,
        filename=version_in.filename or "Resume_Version.pdf",
        file_path=f"/uploads/resumes/v_{current_user.id}_{int(datetime.utcnow().timestamp())}.pdf",
        file_type="application/pdf",
        file_size=150000,
        summary=version_in.summary or f"Resume version: {version_in.title}",
        content_json=version_in.content_json,
        ats_score=85,
        is_active=True,
        status="Active",
        source="Uploaded"
    )
    db.add(new_v)

    # Sync active version to StudentResume
    existing_resume = db.query(StudentResume).filter(StudentResume.student_id == current_user.id).first()
    if existing_resume:
        existing_resume.filename = new_v.filename
        existing_resume.file_path = new_v.file_path
        existing_resume.summary = new_v.summary
        existing_resume.ats_score = new_v.ats_score
    else:
        db.add(StudentResume(
            student_id=current_user.id,
            filename=new_v.filename,
            file_path=new_v.file_path,
            file_type="application/pdf",
            file_size=150000,
            summary=new_v.summary,
            ats_score=new_v.ats_score
        ))

    db.commit()
    db.refresh(new_v)
    log_timeline_event(db, current_user.id, f"Created Resume Version: {new_v.title}", f"New version created and set to active.", "Resume")
    compute_student_metrics(db, current_user.id)
    return StudentResumeVersionResponse.from_orm(new_v)

@router.get("/resume-versions/{version_id}", response_model=StudentResumeVersionResponse)
def get_resume_version_detail(
    version_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    version = db.query(StudentResumeVersion).filter(
        StudentResumeVersion.id == version_id,
        StudentResumeVersion.student_id == current_user.id
    ).first()
    if not version:
        raise HTTPException(status_code=404, detail="Resume version not found")
    return StudentResumeVersionResponse.from_orm(version)

@router.put("/resume-versions/{version_id}", response_model=StudentResumeVersionResponse)
def update_resume_version(
    version_id: int,
    version_in: StudentResumeVersionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    version = db.query(StudentResumeVersion).filter(
        StudentResumeVersion.id == version_id,
        StudentResumeVersion.student_id == current_user.id
    ).first()
    if not version:
        raise HTTPException(status_code=404, detail="Resume version not found")

    if version_in.title is not None:
        version.title = version_in.title
    if version_in.status is not None:
        version.status = version_in.status

    db.commit()
    db.refresh(version)
    return StudentResumeVersionResponse.from_orm(version)

@router.post("/resume-versions/{version_id}/set-active", response_model=StudentResumeVersionResponse)
def set_active_resume_version(
    version_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    version = db.query(StudentResumeVersion).filter(
        StudentResumeVersion.id == version_id,
        StudentResumeVersion.student_id == current_user.id
    ).first()
    if not version:
        raise HTTPException(status_code=404, detail="Resume version not found")

    # Deactivate all student versions
    db.query(StudentResumeVersion).filter(
        StudentResumeVersion.student_id == current_user.id
    ).update({"is_active": False})

    version.is_active = True
    version.status = "Active"
    version.updated_at = datetime.utcnow()

    # Sync to StudentResume table
    existing_resume = db.query(StudentResume).filter(StudentResume.student_id == current_user.id).first()
    if existing_resume:
        existing_resume.filename = version.filename
        existing_resume.file_path = version.file_path
        existing_resume.summary = version.summary
        existing_resume.ats_score = version.ats_score
    else:
        db.add(StudentResume(
            student_id=current_user.id,
            filename=version.filename,
            file_path=version.file_path,
            file_type=version.file_type or "application/pdf",
            file_size=version.file_size or 150000,
            summary=version.summary,
            ats_score=version.ats_score
        ))

    db.commit()
    db.refresh(version)
    log_timeline_event(db, current_user.id, f"Activated Resume Version: {version.title}", f"Set '{version.title}' as the primary active resume.", "Resume")
    return StudentResumeVersionResponse.from_orm(version)

@router.delete("/resume-versions/{version_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume_version(
    version_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    version = db.query(StudentResumeVersion).filter(
        StudentResumeVersion.id == version_id,
        StudentResumeVersion.student_id == current_user.id
    ).first()
    if not version:
        raise HTTPException(status_code=404, detail="Resume version not found")

    was_active = version.is_active
    db.delete(version)
    db.commit()

    # If active was deleted, make latest remaining version active if present
    if was_active:
        next_v = db.query(StudentResumeVersion).filter(
            StudentResumeVersion.student_id == current_user.id
        ).order_by(StudentResumeVersion.created_at.desc()).first()
        if next_v:
            next_v.is_active = True
            db.commit()

    compute_student_metrics(db, current_user.id)
    return None


# =============================================================
# 2. CERTIFICATE MANAGEMENT ENDPOINTS
# =============================================================
@router.get("/certificates", response_model=List[StudentCertificateResponse])
def get_student_certificates(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(StudentCertificate).filter(
        StudentCertificate.student_id == current_user.id
    ).order_by(StudentCertificate.created_at.desc()).all()

@router.post("/certificates", response_model=StudentCertificateResponse, status_code=status.HTTP_201_CREATED)
async def create_student_certificate(
    title: str = Form(...),
    issuing_organization: str = Form(...),
    issue_date: str = Form(...),
    expiry_date: Optional[str] = Form(None),
    credential_id: Optional[str] = Form(None),
    credential_url: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    skills_tags: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    filename = None
    file_path = None
    file_type = None
    file_size = None

    if file:
        filename = file.filename
        file_type = file.content_type
        contents = await file.read()
        file_size = len(contents)

        # File validation
        ext = os.path.splitext(filename)[1].lower()
        if ext not in ['.pdf', '.png', '.jpg', '.jpeg', '.webp', '.docx']:
            raise HTTPException(status_code=400, detail="Invalid certificate file type. Allowed: PDF, PNG, JPG, WEBP, DOCX")
        
        os.makedirs("uploads/certificates", exist_ok=True)
        file_path = f"uploads/certificates/user_{current_user.id}_{int(datetime.utcnow().timestamp())}_{filename}"
        with open(file_path, "wb") as f:
            f.write(contents)

    cert = StudentCertificate(
        student_id=current_user.id,
        title=title.strip(),
        issuing_organization=issuing_organization.strip(),
        issue_date=issue_date.strip(),
        expiry_date=expiry_date.strip() if expiry_date else None,
        credential_id=credential_id.strip() if credential_id else None,
        credential_url=credential_url.strip() if credential_url else None,
        description=description.strip() if description else None,
        skills_tags=skills_tags.strip() if skills_tags else None,
        filename=filename,
        file_path=file_path,
        file_type=file_type,
        file_size=file_size
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)

    log_timeline_event(
        db,
        current_user.id,
        title=f"Earned Certificate: {cert.title}",
        description=f"Earned certification '{cert.title}' issued by {cert.issuing_organization}.",
        category="Certificate"
    )
    compute_student_metrics(db, current_user.id)
    return StudentCertificateResponse.from_orm(cert)

@router.get("/certificates/{certificate_id}", response_model=StudentCertificateResponse)
def get_certificate_detail(
    certificate_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cert = db.query(StudentCertificate).filter(
        StudentCertificate.id == certificate_id,
        StudentCertificate.student_id == current_user.id
    ).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return StudentCertificateResponse.from_orm(cert)


@router.get("/certificates/{certificate_id}/file")
def get_student_certificate_file(
    certificate_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cert = db.query(StudentCertificate).filter(
        StudentCertificate.id == certificate_id,
        StudentCertificate.student_id == current_user.id
    ).first()
    
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found or unauthorized access")
    
    if not cert.file_path or not cert.filename:
        raise HTTPException(status_code=404, detail="No certificate file attached to this record")

    file_path = cert.file_path
    if not os.path.isabs(file_path):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        file_path = os.path.normpath(os.path.join(base_dir, file_path))

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Certificate file not found on server storage")

    ext = os.path.splitext(cert.filename)[1].lower()
    media_type_map = {
        ".pdf": "application/pdf",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".doc": "application/msword",
    }
    media_type = media_type_map.get(ext, cert.file_type or "application/octet-stream")
    disposition_type = "inline" if ext in [".pdf", ".png", ".jpg", ".jpeg", ".webp"] else "attachment"

    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=cert.filename,
        headers={"Content-Disposition": f'{disposition_type}; filename="{cert.filename}"'}
    )

@router.put("/certificates/{certificate_id}", response_model=StudentCertificateResponse)
def update_student_certificate(
    certificate_id: int,
    cert_in: StudentCertificateUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cert = db.query(StudentCertificate).filter(
        StudentCertificate.id == certificate_id,
        StudentCertificate.student_id == current_user.id
    ).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")

    update_data = cert_in.dict(exclude_unset=True)
    for field, val in update_data.items():
        if val is not None:
            setattr(cert, field, val)

    db.commit()
    db.refresh(cert)
    return StudentCertificateResponse.from_orm(cert)

@router.delete("/certificates/{certificate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_certificate(
    certificate_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cert = db.query(StudentCertificate).filter(
        StudentCertificate.id == certificate_id,
        StudentCertificate.student_id == current_user.id
    ).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")

    db.delete(cert)
    db.commit()
    compute_student_metrics(db, current_user.id)
    return None


# =============================================================
# 3. GITHUB INTEGRATION ENDPOINTS
# =============================================================
@router.get("/github", response_model=Optional[StudentGithubProfileResponse])
def get_github_integration(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(StudentGithubProfile).filter(
        StudentGithubProfile.student_id == current_user.id
    ).first()
    if not profile:
        return None
    return StudentGithubProfileResponse.from_orm(profile)

@router.post("/github/connect", response_model=StudentGithubProfileResponse)
def connect_github_profile(
    req: GithubConnectRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        gh_data = fetch_github_user_data(req.username)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="GitHub service is currently unavailable. Please check your connection and try again.")

    # Remove existing profile if any
    existing = db.query(StudentGithubProfile).filter(StudentGithubProfile.student_id == current_user.id).first()
    if existing:
        db.delete(existing)
        db.commit()

    # Create new github profile record
    profile = StudentGithubProfile(
        student_id=current_user.id,
        username=gh_data["username"],
        name=gh_data.get("name"),
        bio=gh_data.get("bio"),
        avatar_url=gh_data.get("avatar_url"),
        html_url=gh_data["html_url"],
        public_repos=gh_data["public_repos"],
        followers=gh_data["followers"],
        following=gh_data["following"],
        last_synced_at=datetime.utcnow()
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)

    # Insert repositories
    for r in gh_data["repositories"]:
        repo = StudentGithubRepository(
            student_id=current_user.id,
            github_profile_id=profile.id,
            name=r["name"],
            description=r.get("description"),
            html_url=r["html_url"],
            language=r.get("language"),
            stargazers_count=r["stargazers_count"],
            forks_count=r["forks_count"],
            is_fork=r["is_fork"],
            updated_at_remote=r.get("updated_at_remote")
        )
        db.add(repo)

    # Update github_url in student profile if empty
    std_prof = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if std_prof and not std_prof.github_url:
        std_prof.github_url = gh_data["html_url"]

    db.commit()
    db.refresh(profile)

    log_timeline_event(
        db,
        current_user.id,
        title=f"Connected GitHub Profile: @{profile.username}",
        description=f"Imported GitHub profile with {len(gh_data['repositories'])} public repositories.",
        category="GitHub"
    )
    compute_student_metrics(db, current_user.id)
    return StudentGithubProfileResponse.from_orm(profile)

@router.post("/github/sync", response_model=StudentGithubProfileResponse)
def sync_github_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(StudentGithubProfile).filter(
        StudentGithubProfile.student_id == current_user.id
    ).first()
    if not profile:
        raise HTTPException(status_code=404, detail="No connected GitHub profile found to sync")

    return connect_github_profile(GithubConnectRequest(username=profile.username), current_user, db)

@router.delete("/github", status_code=status.HTTP_204_NO_CONTENT)
def disconnect_github(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(StudentGithubProfile).filter(
        StudentGithubProfile.student_id == current_user.id
    ).first()
    if not profile:
        raise HTTPException(status_code=404, detail="No connected GitHub profile found")

    db.delete(profile)
    db.commit()
    compute_student_metrics(db, current_user.id)
    return None



# =============================================================
# 4. CAREER TIMELINE ENDPOINTS
# =============================================================
@router.get("/timeline", response_model=List[StudentTimelineEventResponse])
def get_career_timeline(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    events = db.query(StudentTimelineEvent).filter(
        StudentTimelineEvent.student_id == current_user.id
    ).order_by(StudentTimelineEvent.event_date.desc()).all()
    
    return events


# =============================================================
# 5. CAREER PASSPORT ENDPOINTS
# =============================================================
@router.get("/passport", response_model=CareerPassportResponse)
def get_career_passport(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    prof = compute_student_metrics(db, current_user.id)
    educations = db.query(StudentEducation).filter(StudentEducation.student_id == current_user.id).order_by(StudentEducation.start_year.desc()).all()
    skills = db.query(StudentSkill).filter(StudentSkill.student_id == current_user.id).order_by(StudentSkill.created_at.desc()).all()
    
    # Active resume version
    active_resume_version = db.query(StudentResumeVersion).filter(
        StudentResumeVersion.student_id == current_user.id,
        StudentResumeVersion.is_active == True
    ).first()
    if not active_resume_version:
        # Fallback to latest resume version
        active_resume_version = db.query(StudentResumeVersion).filter(
            StudentResumeVersion.student_id == current_user.id
        ).order_by(StudentResumeVersion.created_at.desc()).first()

    certs = db.query(StudentCertificate).filter(StudentCertificate.student_id == current_user.id).order_by(StudentCertificate.created_at.desc()).all()
    gh_profile = db.query(StudentGithubProfile).filter(StudentGithubProfile.student_id == current_user.id).first()
    pref = db.query(StudentCareerPreference).filter(StudentCareerPreference.student_id == current_user.id).first()
    timeline = db.query(StudentTimelineEvent).filter(StudentTimelineEvent.student_id == current_user.id).order_by(StudentTimelineEvent.event_date.desc()).limit(10).all()

    return CareerPassportResponse(
        user=UserResponse.from_orm(current_user),
        profile=StudentProfileResponse.from_orm(prof),
        educations=[StudentEducationResponse.from_orm(e) for e in educations],
        skills=[StudentSkillResponse.from_orm(s) for s in skills],
        active_resume=StudentResumeVersionResponse.from_orm(active_resume_version) if active_resume_version else None,
        certificates=[StudentCertificateResponse.from_orm(c) for c in certs],
        github_profile=StudentGithubProfileResponse.from_orm(gh_profile) if gh_profile else None,
        career_preference=CareerPreferenceResponse.from_orm(pref) if pref else None,
        recent_timeline=[StudentTimelineEventResponse.from_orm(t) for t in timeline]
    )


# =============================================================
# 6. AI RESUME GENERATOR (NON-PAID) ENDPOINTS
# =============================================================
@router.post("/resume/generate")
def generate_ai_resume(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        resume_data = generate_non_paid_resume(db, current_user.id)
        return resume_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate resume: {str(e)}")

@router.post("/resume/save-generated", response_model=StudentResumeVersionResponse)
def save_generated_resume(
    req: AISaveResumeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    import json
    content_json_str = json.dumps(req.resume_data.dict())

    if req.set_active:
        db.query(StudentResumeVersion).filter(
            StudentResumeVersion.student_id == current_user.id
        ).update({"is_active": False})

    version = StudentResumeVersion(
        student_id=current_user.id,
        title=req.title.strip(),
        filename=f"Generated_{current_user.full_name.replace(' ', '_')}_Resume.pdf",
        file_path=f"/uploads/resumes/ai_gen_{current_user.id}_{int(datetime.utcnow().timestamp())}.pdf",
        file_type="application/pdf",
        file_size=180000,
        summary=req.resume_data.professional_summary,
        content_json=content_json_str,
        ats_score=90,
        is_active=req.set_active if req.set_active is not None else True,
        status="Active",
        source="AI Generated"
    )
    db.add(version)

    if req.set_active:
        existing_resume = db.query(StudentResume).filter(StudentResume.student_id == current_user.id).first()
        if existing_resume:
            existing_resume.filename = version.filename
            existing_resume.file_path = version.file_path
            existing_resume.summary = version.summary
            existing_resume.ats_score = version.ats_score
        else:
            db.add(StudentResume(
                student_id=current_user.id,
                filename=version.filename,
                file_path=version.file_path,
                file_type=version.file_type,
                file_size=version.file_size,
                summary=version.summary,
                ats_score=version.ats_score
            ))

    db.commit()
    db.refresh(version)

    log_timeline_event(
        db,
        current_user.id,
        title=f"AI Resume Generated: {version.title}",
        description=f"Generated professional resume for target role '{req.resume_data.target_role or 'Software Engineer'}'.",
        category="Resume"
    )
    compute_student_metrics(db, current_user.id)
    return StudentResumeVersionResponse.from_orm(version)

