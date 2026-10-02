from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
import app.models as models
from app.services.auth_service import get_current_user
from app.services.ai_matcher import match_skills_against_job

router = APIRouter(prefix="/opportunities", tags=["Opportunities & AI Radar"])

@router.get("/radar")
def get_opportunity_radar(
    min_match_pct: int = Query(0, ge=0, le=100),
    type_filter: Optional[str] = Query(None), # job, hackathon, research, competition
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Fetch student's skills
    student_skills_db = db.query(models.StudentSkill).filter(models.StudentSkill.user_id == current_user.id).all()
    student_skills = [
        {
            "skill_name": ss.skill.skill_name if ss.skill else "",
            "badge_tier": ss.badge_tier.value,
            "trust_score": ss.trust_score
        }
        for ss in student_skills_db
    ]

    # Fetch opportunities (or active jobs)
    opps = db.query(models.Opportunity).all()
    if not opps:
        # Seed dummy opportunities if database has none
        jobs = db.query(models.Job).filter(models.Job.status == models.JobStatus.published).all()
        for j in jobs:
            opp = models.Opportunity(
                opportunity_type=models.OpportunityType.job if j.employment_type == models.EmploymentType.full_time else models.OpportunityType.job,
                title=j.title,
                organizer=j.company.name if j.company else "Tech Corp",
                required_skills=j.required_skills or ["Python", "FastAPI"],
                source_job_id=j.id
            )
            db.add(opp)
        db.commit()
        opps = db.query(models.Opportunity).all()

    radar_results = []

    for opp in opps:
        if type_filter and opp.opportunity_type.value.lower() != type_filter.lower():
            continue

        req_skills = opp.required_skills if isinstance(opp.required_skills, list) else []
        overall_score, matched, missing = match_skills_against_job(student_skills, req_skills)

        # Calculate candidate's actual skill trust score for this opportunity
        if matched:
            candidate_trust_score = int(sum(m.get("trust_score", 0) for m in matched) / len(matched))
        else:
            candidate_trust_score = 0

        # Standard threshold: 50 for full-time jobs, 35 for projects/hackathons
        min_trust_score_required = 50 if opp.opportunity_type == models.OpportunityType.job else 35
        has_verified_match = any(m.get("badge_tier") == "verified" for m in matched)
        is_trust_qualified = (candidate_trust_score >= min_trust_score_required) and has_verified_match

        if is_trust_qualified:
            trust_fit_label = f"✓ Verified Trust Fit ({candidate_trust_score}/100)"
        elif candidate_trust_score > 0:
            trust_fit_label = f"Emerging Competency ({candidate_trust_score}/100)"
        else:
            trust_fit_label = "Unverified (Take Assessment to Qualify)"

        if overall_score >= min_match_pct:
            is_applied = db.query(models.Application).filter(
                models.Application.user_id == current_user.id,
                models.Application.opportunity_id == opp.id
            ).first() is not None

            is_bookmarked = db.query(models.Bookmark).filter(
                models.Bookmark.user_id == current_user.id,
                models.Bookmark.opportunity_id == opp.id
            ).first() is not None

            radar_results.append({
                "id": str(opp.id),
                "opportunity_type": opp.opportunity_type.value,
                "title": opp.title,
                "organizer": opp.organizer,
                "required_skills": req_skills,
                "match_percentage": overall_score,
                "matched_skills": matched,
                "missing_skills": missing,
                "candidate_trust_score": candidate_trust_score,
                "min_trust_score_required": min_trust_score_required,
                "is_trust_qualified": is_trust_qualified,
                "trust_fit_label": trust_fit_label,
                "is_applied": is_applied,
                "is_bookmarked": is_bookmarked,
                "deadline": opp.deadline.isoformat() if opp.deadline else None,
                "source_job_id": str(opp.source_job_id) if opp.source_job_id else None
            })

    # Sort opportunities based on candidate's skill trust score and match percentage
    radar_results.sort(key=lambda x: (x["candidate_trust_score"], x["match_percentage"]), reverse=True)
    return radar_results

@router.post("/{opportunity_id}/apply")
def apply_opportunity(opportunity_id: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    opp = db.query(models.Opportunity).filter(models.Opportunity.id == opportunity_id).first()
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    existing = db.query(models.Application).filter(
        models.Application.user_id == current_user.id,
        models.Application.opportunity_id == opp.id
    ).first()

    if existing:
        return {"message": "Already applied to this opportunity", "application_id": str(existing.id)}

    app = models.Application(
        user_id=current_user.id,
        opportunity_id=opp.id,
        status=models.ApplicationStatus.applied
    )
    db.add(app)
    db.commit()

    # Notify recruiter if this opportunity is linked to a job posting
    if opp.source_job_id:
        job = db.query(models.Job).filter(models.Job.id == opp.source_job_id).first()
        if job:
            rec = db.query(models.Recruiter).filter(models.Recruiter.company_id == job.company_id).first()
            if rec:
                db.add(models.Notification(
                    user_id=rec.user_id,
                    title="New Application Received!",
                    message=f"{current_user.full_name} applied to your job posting '{opp.title}'."
                ))
                db.commit()

    return {"message": "Application submitted successfully", "application_id": str(app.id)}

@router.post("/{opportunity_id}/bookmark")
def bookmark_opportunity(opportunity_id: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    opp = db.query(models.Opportunity).filter(models.Opportunity.id == opportunity_id).first()
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    existing = db.query(models.Bookmark).filter(
        models.Bookmark.user_id == current_user.id,
        models.Bookmark.opportunity_id == opp.id
    ).first()

    if existing:
        db.delete(existing)
        db.commit()
        return {"bookmarked": False, "message": "Bookmark removed"}

    bm = models.Bookmark(user_id=current_user.id, opportunity_id=opp.id)
    db.add(bm)
    db.commit()

    return {"bookmarked": True, "message": "Bookmarked successfully"}

@router.get("/my-applications")
def get_my_applications(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    apps = db.query(models.Application).filter(models.Application.user_id == current_user.id).order_by(models.Application.applied_at.desc()).all()
    results = []
    for a in apps:
        opp = a.opportunity
        results.append({
            "id": str(a.id),
            "opportunity_id": str(a.opportunity_id),
            "title": opp.title if opp else "Software Developer Intern",
            "organizer": opp.organizer if opp else "TechCorp India",
            "opportunity_type": opp.opportunity_type.value if opp else "job",
            "required_skills": opp.required_skills if opp and isinstance(opp.required_skills, list) else ["Python", "FastAPI"],
            "status": a.status.value,
            "applied_at": a.applied_at.isoformat() if a.applied_at else None
        })
    return results
