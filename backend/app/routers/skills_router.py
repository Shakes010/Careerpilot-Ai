from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
import app.models as models
from app.services.auth_service import get_current_user
from app.services.trust_meter_service import recalculate_trust_score

router = APIRouter(prefix="/skills", tags=["Skills & Trust Meter"])

class AddStudentSkillRequest(BaseModel):
    skill_id: str
    self_rating: int # 1-5

@router.get("")
def get_all_skills(db: Session = Depends(get_db)):
    return db.query(models.Skill).all()

@router.get("/my-skills")
def get_student_skills(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    student_skills = db.query(models.StudentSkill).filter(models.StudentSkill.user_id == current_user.id).all()
    
    results = []
    for ss in student_skills:
        # Check missing evidence detector flag
        evidences = db.query(models.SkillEvidence).filter(models.SkillEvidence.student_skill_id == ss.id).all()
        needs_evidence_nudge = (ss.trust_score < 40 and len(evidences) == 0)

        results.append({
            "id": str(ss.id),
            "skill_id": str(ss.skill_id),
            "skill_name": ss.skill.skill_name if ss.skill else "Skill",
            "category": ss.skill.category if ss.skill else "General",
            "self_rating": ss.self_rating,
            "trust_score": ss.trust_score,
            "badge_tier": ss.badge_tier.value,
            "evidences_count": len(evidences),
            "needs_evidence_nudge": needs_evidence_nudge,
            "last_computed_at": ss.last_computed_at.isoformat() if ss.last_computed_at else None
        })

    return results

@router.post("/my-skills")
def add_student_skill(req: AddStudentSkillRequest, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    existing = db.query(models.StudentSkill).filter(
        models.StudentSkill.user_id == current_user.id,
        models.StudentSkill.skill_id == req.skill_id
    ).first()

    if existing:
        existing.self_rating = req.self_rating
        db.commit()
        recalculate_trust_score(existing.id, db)
        return existing

    ss = models.StudentSkill(
        user_id=current_user.id,
        skill_id=req.skill_id,
        self_rating=req.self_rating,
        trust_score=min(35, req.self_rating * 7),
        badge_tier=models.BadgeTier.declared
    )
    db.add(ss)
    db.commit()
    db.refresh(ss)
    return ss

@router.get("/missing-evidence")
def get_missing_evidence_nudges(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    student_skills = db.query(models.StudentSkill).filter(models.StudentSkill.user_id == current_user.id).all()
    nudges = []
    for ss in student_skills:
        evs = db.query(models.SkillEvidence).filter(models.SkillEvidence.student_skill_id == ss.id).all()
        if ss.trust_score < 40 and len(evs) == 0:
            nudges.append({
                "student_skill_id": str(ss.id),
                "skill_id": str(ss.skill_id),
                "skill_name": ss.skill.skill_name if ss.skill else "Skill",
                "trust_score": ss.trust_score,
                "message": f"Your claimed skill '{ss.skill.skill_name if ss.skill else 'Skill'}' is at {ss.trust_score}% (Declared tier). Take a quick verification assessment or complete a project to upgrade to Verified."
            })
    return nudges

@router.get("/resources/{skill_id}")
def get_learning_resources(skill_id: str, db: Session = Depends(get_db)):
    resources = db.query(models.LearningResource).filter(models.LearningResource.skill_id == skill_id).all()
    if not resources:
        skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
        sname = skill.skill_name if skill else "Software Engineering"
        return [
            {"title": f"Official {sname} Documentation", "url": f"https://docs.python.org/3/", "source": "Official Docs"},
            {"title": f"FreeCodeCamp {sname} Course", "url": "https://www.freecodecamp.org/", "source": "FreeCodeCamp"},
            {"title": f"MDN Web Docs - {sname}", "url": "https://developer.mozilla.org/", "source": "MDN"}
        ]
    return resources
