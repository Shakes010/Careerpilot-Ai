import uuid
from typing import List, Optional
import httpx
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from app.database import get_db
import app.models as models
from app.schemas.profile_schemas import (
    StudentProfileUpdate, StudentProfileOut, ResumeCreate, CertificateCreate,
    PortfolioItemCreate, GithubSyncRequest, LinkedinLinkCreate
)
from app.services.auth_service import get_current_user, check_eligibility
from app.services.resume_parser import extract_text_from_pdf, parse_resume_text, analyze_resume_quality
from app.services.ai_matcher import match_skills_against_job

router = APIRouter(prefix="/profile", tags=["Student Profile & Career Passport"])

# 1. Student Profile CRUD
@router.get("/student", response_model=StudentProfileOut)
def get_student_profile(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    sp = db.query(models.StudentProfile).filter(models.StudentProfile.user_id == current_user.id).first()
    if not sp:
        sp = models.StudentProfile(user_id=current_user.id, is_eligible=True, profile_completion_pct=20)
        db.add(sp)
        db.commit()
        db.refresh(sp)
    return sp

@router.put("/student", response_model=StudentProfileOut)
def update_student_profile(req: StudentProfileUpdate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    sp = db.query(models.StudentProfile).filter(models.StudentProfile.user_id == current_user.id).first()
    if not sp:
        sp = models.StudentProfile(user_id=current_user.id)
        db.add(sp)

    update_data = req.model_dump(exclude_unset=True)
    for field, val in update_data.items():
        setattr(sp, field, val)

    # Recompute eligibility if degree or graduation year updated
    if req.degree is not None or req.graduation_year is not None:
        deg = sp.degree or ""
        grad = sp.graduation_year
        sp.is_eligible = check_eligibility(deg, grad)

    # Calculate completion percentage
    fields_to_check = [sp.phone, sp.location, sp.college_name, sp.degree, sp.graduation_year, sp.cgpa, sp.career_goal, sp.bio]
    filled = sum(1 for f in fields_to_check if f is not None and str(f).strip() != "")
    sp.profile_completion_pct = int((filled / len(fields_to_check)) * 100)

    db.commit()
    db.refresh(sp)
    return sp

# 2. Resumes & Parser
@router.post("/resume/upload")
async def upload_and_parse_resume(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported for resume parsing")

    content = await file.read()
    raw_text = extract_text_from_pdf(content)

    all_skills = [s.skill_name for s in db.query(models.Skill).all()]
    parsed_json = parse_resume_text(raw_text, all_skills)
    analysis = analyze_resume_quality(parsed_json)

    return {
        "filename": file.filename,
        "parsed_data": parsed_json,
        "quality_analysis": analysis,
        "message": "Resume parsed successfully. Please review and edit before saving."
    }

@router.post("/resume/save")
def save_resume_version(req: ResumeCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Find existing resume or create new
    resume = db.query(models.Resume).filter(models.Resume.user_id == current_user.id).first()
    if not resume:
        resume = models.Resume(
            user_id=current_user.id,
            resume_label=req.resume_label,
            target_role=req.target_role
        )
        db.add(resume)
        db.flush()

    # Get latest version number
    version_count = db.query(models.ResumeVersion).filter(models.ResumeVersion.resume_id == resume.id).count()
    new_ver = models.ResumeVersion(
        resume_id=resume.id,
        version_number=version_count + 1,
        content_json=req.content_json,
        change_summary=f"Saved version {version_count + 1}"
    )
    db.add(new_ver)
    db.flush()

    resume.current_version_id = new_ver.id
    resume.resume_label = req.resume_label
    if req.target_role:
        resume.target_role = req.target_role

    db.commit()
    return {
        "resume_id": str(resume.id),
        "version_id": str(new_ver.id),
        "version_number": new_ver.version_number,
        "message": f"Resume version {new_ver.version_number} saved successfully"
    }

@router.get("/resume/versions")
def list_resume_versions(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    resume = db.query(models.Resume).filter(models.Resume.user_id == current_user.id).first()
    if not resume:
        return {"resume": None, "versions": []}

    versions = db.query(models.ResumeVersion).filter(models.ResumeVersion.resume_id == resume.id).order_by(models.ResumeVersion.version_number.desc()).all()
    return {
        "resume_id": str(resume.id),
        "resume_label": resume.resume_label,
        "target_role": resume.target_role,
        "current_version_id": str(resume.current_version_id) if resume.current_version_id else None,
        "versions": [
            {
                "id": str(v.id),
                "version_number": v.version_number,
                "content_json": v.content_json,
                "change_summary": v.change_summary,
                "created_at": v.created_at.isoformat()
            }
            for v in versions
        ]
    }

# 3. Certificates Management (Always "declared" tier)
@router.post("/certificates")
def add_certificate(req: CertificateCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    cert = models.Certificate(
        user_id=current_user.id,
        title=req.title,
        issuer=req.issuer,
        file_url=req.file_url,
        issue_date=req.issue_date,
        verification_status=models.CertificateStatus.pending # Stays declared tier
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)

    # Auto-add to portfolio
    port_item = models.PortfolioItem(
        user_id=current_user.id,
        item_type=models.PortfolioItemType.certificate,
        source_ref_id=cert.id,
        title=f"Certificate: {cert.title}",
        thumbnail_url=cert.file_url
    )
    db.add(port_item)
    db.commit()

    return cert

@router.get("/certificates")
def list_certificates(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Certificate).filter(models.Certificate.user_id == current_user.id).order_by(models.Certificate.created_at.desc()).all()

# 4. Portfolio Items
@router.post("/portfolio")
def add_portfolio_item(req: PortfolioItemCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = models.PortfolioItem(
        user_id=current_user.id,
        item_type=req.item_type,
        source_ref_id=req.source_ref_id,
        title=req.title,
        thumbnail_url=req.thumbnail_url,
        display_order=req.display_order or 0
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/portfolio")
def list_portfolio_items(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.PortfolioItem).filter(models.PortfolioItem.user_id == current_user.id).order_by(models.PortfolioItem.display_order.asc(), models.PortfolioItem.created_at.desc()).all()

# 5. GitHub & LinkedIn Integrations
@router.post("/integrations/github")
async def sync_github(req: GithubSyncRequest, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Call GitHub REST API to fetch public repos and top languages
    url = f"https://api.github.com/users/{req.github_username}"
    repos_url = f"https://api.github.com/users/{req.github_username}/repos?per_page=100"

    public_repos = 0
    total_commits = 0
    languages = {}

    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(url, headers={"User-Agent": "CareerPilot-AI"})
            if res.status_code == 200:
                data = res.json()
                public_repos = data.get("public_repos", 0)

            repos_res = await client.get(repos_url, headers={"User-Agent": "CareerPilot-AI"})
            if repos_res.status_code == 200:
                repos_data = repos_res.json()
                total_commits = sum(repo.get("stargazers_count", 0) + repo.get("forks_count", 0) for repo in repos_data) * 5 + public_repos * 12
                for repo in repos_data:
                    lang = repo.get("language")
                    if lang:
                        languages[lang] = languages.get(lang, 0) + 1
    except Exception as e:
        print(f"GitHub API sync error: {e}")

    gh = db.query(models.GithubLink).filter(models.GithubLink.user_id == current_user.id).first()
    if not gh:
        gh = models.GithubLink(user_id=current_user.id, github_username=req.github_username)
        db.add(gh)

    gh.github_username = req.github_username
    gh.public_repos = public_repos
    gh.total_commits = total_commits
    gh.top_languages = languages
    gh.last_synced_at = models.utc_now()

    db.commit()
    db.refresh(gh)
    return gh

@router.post("/integrations/linkedin")
def save_linkedin(req: LinkedinLinkCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    link = db.query(models.LinkedinLink).filter(models.LinkedinLink.user_id == current_user.id).first()
    if not link:
        link = models.LinkedinLink(user_id=current_user.id, profile_url=req.profile_url)
        db.add(link)

    link.profile_url = req.profile_url
    link.headline = req.headline
    link.last_synced_at = models.utc_now()

    db.commit()
    db.refresh(link)
    return link

# 6. Career Passport (Aggregated Read-Only Query)
@router.get("/career-passport")
def get_career_passport(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    sp = db.query(models.StudentProfile).filter(models.StudentProfile.user_id == current_user.id).first()
    skills = db.query(models.StudentSkill).filter(models.StudentSkill.user_id == current_user.id).all()
    certificates = db.query(models.Certificate).filter(models.Certificate.user_id == current_user.id).all()
    portfolio = db.query(models.PortfolioItem).filter(models.PortfolioItem.user_id == current_user.id).all()
    github = db.query(models.GithubLink).filter(models.GithubLink.user_id == current_user.id).first()
    linkedin = db.query(models.LinkedinLink).filter(models.LinkedinLink.user_id == current_user.id).first()
    resume = db.query(models.Resume).filter(models.Resume.user_id == current_user.id).first()

    verified_count = sum(1 for s in skills if s.badge_tier == models.BadgeTier.verified)
    avg_trust = int(sum(s.trust_score for s in skills) / len(skills)) if skills else 20

    return {
        "user_id": str(current_user.id),
        "full_name": current_user.full_name,
        "email": current_user.email,
        "phone": current_user.phone,
        "student_profile": sp,
        "metrics": {
            "total_skills": len(skills),
            "verified_skills_count": verified_count,
            "declared_skills_count": len(skills) - verified_count,
            "average_trust_score": avg_trust,
            "total_certificates": len(certificates),
            "portfolio_items_count": len(portfolio)
        },
        "skills": [
            {
                "id": str(s.id),
                "skill_name": s.skill.skill_name if s.skill else "Skill",
                "category": s.skill.category if s.skill else "General",
                "self_rating": s.self_rating,
                "trust_score": s.trust_score,
                "badge_tier": s.badge_tier.value,
                "last_computed_at": s.last_computed_at.isoformat() if s.last_computed_at else None
            }
            for s in skills
        ],
        "certificates": certificates,
        "portfolio": portfolio,
        "github": github,
        "linkedin": linkedin,
        "resume": resume
    }

# 7. Career Timeline (Auto-generated from timestamped events)
@router.get("/career-timeline")
def get_career_timeline(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    events = []

    # Skills added
    skills = db.query(models.StudentSkill).filter(models.StudentSkill.user_id == current_user.id).all()
    for s in skills:
        events.append({
            "event_type": "skill_added",
            "title": f"Declared Skill: {s.skill.skill_name if s.skill else 'Skill'}",
            "detail": f"Initial rating: {s.self_rating}/5 | Trust score: {s.trust_score}",
            "timestamp": s.created_at.isoformat() if s.created_at else None,
            "badge_tier": s.badge_tier.value
        })

    # Certificates added
    certs = db.query(models.Certificate).filter(models.Certificate.user_id == current_user.id).all()
    for c in certs:
        events.append({
            "event_type": "certificate",
            "title": f"Certificate Uploaded: {c.title}",
            "detail": f"Issuer: {c.issuer or 'Self-reported'}",
            "timestamp": c.created_at.isoformat() if c.created_at else None,
            "badge_tier": "declared"
        })

    # Portfolio items
    ports = db.query(models.PortfolioItem).filter(models.PortfolioItem.user_id == current_user.id).all()
    for p in ports:
        events.append({
            "event_type": "portfolio_item",
            "title": f"Portfolio Item: {p.title}",
            "detail": f"Type: {p.item_type.value}",
            "timestamp": p.created_at.isoformat() if p.created_at else None,
            "badge_tier": "declared"
        })

    # Sort reverse chronological
    events.sort(key=lambda x: x["timestamp"] or "", reverse=True)
    return {"timeline_events": events}

# 8. Career Readiness Dashboard Stats
@router.get("/readiness-dashboard")
def get_readiness_dashboard(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    sp = current_user.student_profile
    skills = db.query(models.StudentSkill).filter(models.StudentSkill.user_id == current_user.id).all()
    applications = db.query(models.Application).filter(models.Application.user_id == current_user.id).all()
    verified_skills = [s for s in skills if s.badge_tier == models.BadgeTier.verified]
    declared_skills = [s for s in skills if s.badge_tier != models.BadgeTier.verified]
    attempts = db.query(models.AssessmentAttempt).filter(models.AssessmentAttempt.user_id == current_user.id).all()
    passed_attempts = [a for a in attempts if a.status == models.AttemptStatus.passed]
    projects = db.query(models.Project).filter(models.Project.user_id == current_user.id).all()
    completed_projects = [p for p in projects if p.status == models.ProjectStatus.completed]

    # Baseline 0 - strictly earned points
    profile_score = 0
    if sp:
        if sp.degree and sp.graduation_year:
            profile_score += 5
        if sp.college_name:
            profile_score += 5
        if sp.bio or sp.career_goal:
            profile_score += 5

    skills_score = min(45, (len(verified_skills) * 15) + (len(declared_skills) * 2))
    assessments_score = min(20, len(passed_attempts) * 10)
    projects_score = min(20, len(completed_projects) * 10)
    readiness_index = min(100, profile_score + skills_score + assessments_score + projects_score)

    avg_trust = int(sum(s.trust_score for s in skills) / len(skills)) if skills else 0

    return {
        "readiness_score": readiness_index,
        "total_claimed_skills": len(skills),
        "verified_skills_count": len(verified_skills),
        "average_trust_score": avg_trust,
        "total_applications": len(applications),
        "shortlisted_applications": sum(1 for a in applications if a.status == models.ApplicationStatus.shortlisted),
        "profile_completion_pct": current_user.student_profile.profile_completion_pct if current_user.student_profile else 0
    }

# 9. Comprehensive Student Analytics
@router.get("/student-analytics")
def get_student_analytics(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    sp = current_user.student_profile
    skills = db.query(models.StudentSkill).filter(models.StudentSkill.user_id == current_user.id).all()
    verified_skills = [s for s in skills if s.badge_tier == models.BadgeTier.verified]
    declared_skills = [s for s in skills if s.badge_tier != models.BadgeTier.verified]

    # Attempts & submissions
    attempts = db.query(models.AssessmentAttempt).filter(models.AssessmentAttempt.user_id == current_user.id).all()
    passed_attempts = [a for a in attempts if a.status == models.AttemptStatus.passed]
    flagged_attempts = [a for a in attempts if a.is_flagged]

    # Projects
    projects = db.query(models.Project).filter(models.Project.user_id == current_user.id).all()
    completed_projects = [p for p in projects if p.status == models.ProjectStatus.completed]

    # 1. Genuine Career Readiness Score (0 - 100 base)
    profile_score = 0
    if sp:
        if sp.degree and sp.graduation_year:
            profile_score += 5
        if sp.college_name:
            profile_score += 5
        if sp.bio or sp.career_goal:
            profile_score += 5

    skills_score = min(45, (len(verified_skills) * 15) + (len(declared_skills) * 2))
    assessments_score = min(20, len(passed_attempts) * 10)
    projects_score = min(20, len(completed_projects) * 10)
    readiness_score = min(100, profile_score + skills_score + assessments_score + projects_score)

    # 2. Average Trust Score (0 if empty)
    avg_trust = int(sum(s.trust_score for s in skills) / len(skills)) if skills else 0

    # 3. Opportunity Match Velocity (dynamic against real opportunities)
    student_skills_repr = [
        {
            "skill_name": s.skill.skill_name if s.skill else "",
            "badge_tier": s.badge_tier.value,
            "trust_score": s.trust_score
        }
        for s in skills
    ]
    opps = db.query(models.Opportunity).all()
    if opps and skills:
        match_scores = []
        for opp in opps:
            req_skills = opp.required_skills if isinstance(opp.required_skills, list) else []
            score, _, _ = match_skills_against_job(student_skills_repr, req_skills)
            match_scores.append(score)
        match_velocity = int(sum(match_scores) / len(match_scores)) if match_scores else 0
    else:
        match_velocity = 0

    # 4. Checkpoint Timing & Pass Rate
    attempt_ids = [a.id for a in attempts]
    submissions = db.query(models.CheckpointSubmission).filter(models.CheckpointSubmission.attempt_id.in_(attempt_ids)).all() if attempt_ids else []

    if submissions:
        valid_times = [s.time_spent_seconds for s in submissions if s.time_spent_seconds > 0]
        avg_seconds = int(sum(valid_times) / len(valid_times)) if valid_times else 0
        if avg_seconds >= 60:
            avg_time_str = f"{avg_seconds // 60}m {avg_seconds % 60}s"
        elif avg_seconds > 0:
            avg_time_str = f"{avg_seconds}s"
        else:
            avg_time_str = "< 1m"
    else:
        avg_time_str = "N/A"

    test_pass_rate = round((len(passed_attempts) / len(attempts)) * 100, 1) if attempts else 0.0

    # 5. Anti-cheat integrity rating
    anti_cheat_flags_count = len(flagged_attempts)
    if anti_cheat_flags_count == 0:
        integrity_rating_pct = 100
        integrity_status = "Optimal (0 Flags)"
    else:
        integrity_rating_pct = max(20, 100 - (anti_cheat_flags_count * 30))
        integrity_status = f"{anti_cheat_flags_count} Flag(s) Detected"

    # 6. Percentile & Cohort placement
    if readiness_score == 0:
        percentile_label = "Cohort Baseline (0%)"
        headline = "0% Industry Deployment Ready"
        description = "Your career profile is at baseline. Declare your technical skills and complete checkpoint assessments to calibrate your readiness."
    elif readiness_score < 25:
        percentile_label = "Cohort Starter Tier"
        headline = f"{readiness_score}% Industry Deployment Ready"
        description = "Your profile is in the starter tier. Complete your first verification assessment to earn cryptographic skill badges."
    elif readiness_score < 50:
        percentile_label = "Top 50th percentile in cohort"
        headline = f"{readiness_score}% Industry Deployment Ready"
        description = "Solid progress. Complete verified technical assessments to boost your opportunity match velocity for entry-level roles."
    elif readiness_score < 75:
        percentile_label = "Top 25th percentile in cohort"
        headline = f"{readiness_score}% Industry Deployment Ready"
        description = "High recruiter confidence profile. Verifying 1 more high-demand skill will qualify you for top-tier hiring partner requisitions."
    else:
        percentile_label = "Top 10th percentile in cohort"
        headline = f"{readiness_score}% Industry Deployment Ready"
        description = "Outstanding profile! You rank among top engineering candidates. Your verified credentials qualify you for immediate industry deployment."

    # 7. Dynamic AI Recommendation
    if not skills:
        ai_recommendation = {
            "title": "Declare Your Core Skills",
            "text": "You haven't declared any technical skills yet. Start by declaring skills like Python, JavaScript, or SQL to begin tracking your Skill Trust Meter."
        }
    elif declared_skills:
        target = declared_skills[0].skill.skill_name if declared_skills[0].skill else "Skill"
        ai_recommendation = {
            "title": f"Verify {target} Competency",
            "text": f"Your declared skill '{target}' is currently unverified. Taking the automated checkpoint assessment will upgrade it to Verified and boost recruiter match velocity."
        }
    elif not completed_projects:
        ai_recommendation = {
            "title": "Complete a Career Sandbox Project",
            "text": "You have verified skills! Complement your test credentials by building an engineering project in the Career Sandbox to reach peak Industry Readiness."
        }
    else:
        ai_recommendation = {
            "title": "Apply to Live High-Match Requisitions",
            "text": "Your verified portfolio matches active hiring drives. Explore the Opportunity Radar to submit 1-click applications to top hiring partners."
        }

    # 8. Skills list
    skills_list = [
        {
            "id": str(s.id),
            "skill_name": s.skill.skill_name if s.skill else "Skill",
            "category": s.skill.category if s.skill else "General",
            "self_rating": s.self_rating,
            "trust_score": s.trust_score,
            "badge_tier": s.badge_tier.value,
            "last_computed_at": s.last_computed_at.isoformat() if s.last_computed_at else None
        }
        for s in skills
    ]

    return {
        "readiness_score": readiness_score,
        "readiness_headline": headline,
        "readiness_description": description,
        "percentile_label": percentile_label,
        "readiness_trend": f"▲ +{readiness_score}% Earned" if readiness_score > 0 else "Baseline (0%)",
        "verified_skills_count": len(verified_skills),
        "total_skills_count": len(skills),
        "avg_trust_score": avg_trust,
        "opportunity_match_velocity": match_velocity,
        "opportunities_count": len(opps),
        "test_pass_rate": test_pass_rate,
        "total_attempts": len(attempts),
        "passed_attempts": len(passed_attempts),
        "avg_time_per_checkpoint": avg_time_str,
        "anti_cheat_flags": anti_cheat_flags_count,
        "integrity_rating_pct": integrity_rating_pct,
        "integrity_status": integrity_status,
        "ai_recommendation": ai_recommendation,
        "skills": skills_list
    }
