from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.student import (
    StudentProfile,
    StudentEducation,
    StudentSkill,
    StudentResume,
    StudentCareerPreference
)

def compute_student_metrics(db: Session, user_id: int) -> StudentProfile:
    """
    Computes Readiness Index, Skill Trust Score, and Verified Skills count
    strictly from the student's actual persisted records in PostgreSQL.
    """
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    if not profile:
        profile = StudentProfile(
            user_id=user_id,
            career_readiness_score=0,
            skill_trust_meter=0.0,
            verified_skills_count=0
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)

    educations = db.query(StudentEducation).filter(StudentEducation.student_id == user_id).all()
    skills = db.query(StudentSkill).filter(StudentSkill.student_id == user_id).all()
    resume = db.query(StudentResume).filter(StudentResume.student_id == user_id).order_by(StudentResume.uploaded_at.desc()).first()
    pref = db.query(StudentCareerPreference).filter(StudentCareerPreference.student_id == user_id).first()

    # 1. Skill Trust Score & Verified Skills Count
    total_skills = len(skills)
    verified_skills = sum(1 for s in skills if s.is_verified)
    unverified_skills = total_skills - verified_skills

    if total_skills == 0:
        trust_score = 0.0
    else:
        # Verified skills provide full trust (1.0), unverified provide partial confidence (0.4)
        raw_trust = ((verified_skills * 1.0 + unverified_skills * 0.4) / total_skills) * 100.0
        # Scale with depth/volume of skills (1 skill = 33% depth factor, 3+ skills = 100% depth factor)
        depth_factor = min(1.0, total_skills / 3.0)
        trust_score = round(raw_trust * depth_factor, 1)

    # 2. Readiness Index (Profile Completeness)
    readiness = 0

    # Profile personal info contributions (Max 30%)
    if profile.bio and len(profile.bio.strip()) > 10:
        readiness += 10
    if profile.phone and profile.location:
        readiness += 10
    if profile.headline and len(profile.headline.strip()) > 3:
        readiness += 5
    if profile.linkedin_url or profile.github_url or profile.website:
        readiness += 5

    # Education contribution (Max 20%)
    if len(educations) == 1:
        readiness += 15
    elif len(educations) >= 2:
        readiness += 20

    # Skills contribution (Max 25%)
    if total_skills == 1:
        readiness += 10
    elif total_skills == 2:
        readiness += 15
    elif total_skills >= 3:
        readiness += 20
        if verified_skills > 0:
            readiness += 5 # +5 bonus for having verified skills

    # Resume contribution (Max 15%)
    if resume is not None:
        readiness += 15

    # Career Preferences contribution (Max 10%)
    if pref is not None and pref.preferred_role and len(pref.preferred_role.strip()) > 0:
        readiness += 10

    final_readiness_score = min(100, readiness)

    # Persist updated values into PostgreSQL
    profile.career_readiness_score = int(final_readiness_score)
    profile.skill_trust_meter = float(trust_score)
    profile.verified_skills_count = int(verified_skills)

    db.commit()
    db.refresh(profile)

    return profile
