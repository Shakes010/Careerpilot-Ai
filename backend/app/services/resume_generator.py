from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.student import (
    User,
    StudentProfile,
    StudentEducation,
    StudentSkill,
    StudentCertificate,
    StudentGithubProfile,
    StudentGithubRepository,
    StudentCareerPreference
)

def generate_non_paid_resume(db: Session, user_id: int) -> Dict[str, Any]:
    """
    Generates a professional ATS-friendly resume structure strictly using actual
    data available in PostgreSQL for the student. No fake skills, experience, or certs.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")

    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    educations = db.query(StudentEducation).filter(StudentEducation.student_id == user_id).order_by(StudentEducation.start_year.desc()).all()
    skills = db.query(StudentSkill).filter(StudentSkill.student_id == user_id).all()
    certs = db.query(StudentCertificate).filter(StudentCertificate.student_id == user_id).all()
    gh_profile = db.query(StudentGithubProfile).filter(StudentGithubProfile.student_id == user_id).first()
    gh_repos = db.query(StudentGithubRepository).filter(StudentGithubRepository.student_id == user_id).order_by(StudentGithubRepository.stargazers_count.desc()).all()
    pref = db.query(StudentCareerPreference).filter(StudentCareerPreference.student_id == user_id).first()
    target_role = pref.preferred_role if pref and pref.preferred_role else "Software Engineer"
    headline = (profile.headline if profile and profile.headline else f"Aspiring {target_role}")
    major_uni = ""
    if profile and profile.major and profile.university:
        major_uni = f" Pursuing {profile.major} at {profile.university}."
    elif profile and profile.university:
        major_uni = f" Student at {profile.university}."

    bio_snippet = f" {profile.bio.strip()}" if profile and profile.bio else ""
    skill_list_str = ", ".join([s.skill_name for s in skills[:6]]) if skills else ""
    skill_snippet = f" Proficient in {skill_list_str}." if skill_list_str else ""

    summary_text = f"{headline}.{major_uni}{skill_snippet}{bio_snippet}".strip()

    # Group skills by category
    skills_by_category = {}
    for sk in skills:
        cat = sk.category or "Technical Skills"
        if cat not in skills_by_category:
            skills_by_category[cat] = []
        skills_by_category[cat].append(sk.skill_name)

    formatted_skills = [
        {"category": cat, "skills": items}
        for cat, items in skills_by_category.items()
    ]

    # Format Education
    formatted_edu = [
        {
            "id": edu.id,
            "degree": edu.degree,
            "institution": edu.institution,
            "start_year": edu.start_year,
            "end_year": edu.end_year,
            "grade": edu.grade,
            "details": edu.details
        }
        for edu in educations
    ]

    # Format Certifications
    formatted_certs = [
        {
            "id": c.id,
            "title": c.title,
            "issuing_organization": c.issuing_organization,
            "issue_date": c.issue_date,
            "expiry_date": c.expiry_date,
            "credential_id": c.credential_id,
            "credential_url": c.credential_url,
            "skills_tags": c.skills_tags
        }
        for c in certs
    ]

    # Format Projects (from GitHub or profile)
    formatted_projects = [
        {
            "id": repo.id,
            "name": repo.name,
            "description": repo.description or f"Open-source software repository built with {repo.language or 'Modern Web Tech'}.",
            "html_url": repo.html_url,
            "language": repo.language,
            "stars": repo.stargazers_count
        }
        for repo in gh_repos[:6]
    ]

    return {
        "full_name": user.full_name,
        "email": user.email,
        "phone": profile.phone if profile else None,
        "location": profile.location if profile else None,
        "linkedin_url": profile.linkedin_url if profile else None,
        "github_url": gh_profile.html_url if gh_profile else (profile.github_url if profile else None),
        "target_role": target_role,
        "professional_summary": summary_text,
        "skills_grouped": formatted_skills,
        "education": formatted_edu,
        "certifications": formatted_certs,
        "projects": formatted_projects
    }
