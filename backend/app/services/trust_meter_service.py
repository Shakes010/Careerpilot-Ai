from datetime import datetime, timezone
from sqlalchemy.orm import Session
import app.models as models

def recalculate_trust_score(student_skill_id: str, db: Session) -> models.StudentSkill:
    student_skill = db.query(models.StudentSkill).filter(models.StudentSkill.id == student_skill_id).first()
    if not student_skill:
        return None

    evidences = db.query(models.SkillEvidence).filter(models.SkillEvidence.student_skill_id == student_skill_id).all()

    if not evidences:
        # Base declared score derived from self rating
        base_score = min(35, student_skill.self_rating * 7)
        student_skill.trust_score = base_score
        student_skill.badge_tier = models.BadgeTier.declared
    else:
        # Noisy-OR Aggregation: S = 1 - product(1 - w_i)
        prod = 1.0
        for ev in evidences:
            w = float(ev.weight)
            prod *= (1.0 - w)
        
        calculated_prob = 1.0 - prod
        # Scale to 0-100 score with base self-rating weight
        final_score = int(min(100, max(20, calculated_prob * 100)))

        student_skill.trust_score = final_score

        # Badge tier upgrade threshold: trust score >= 60 OR has at least one passed assessment/verified project
        has_strong_evidence = any(ev.evidence_type in [models.EvidenceType.assessment, models.EvidenceType.project] for ev in evidences)
        if final_score >= 60 or has_strong_evidence:
            student_skill.badge_tier = models.BadgeTier.verified
        else:
            student_skill.badge_tier = models.BadgeTier.declared

    student_skill.last_computed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(student_skill)
    return student_skill

def add_skill_evidence(
    user_id: str,
    skill_id: str,
    evidence_type: models.EvidenceType,
    evidence_ref_id: str,
    weight: float,
    db: Session
) -> models.StudentSkill:
    # Ensure student_skill exists
    student_skill = db.query(models.StudentSkill).filter(
        models.StudentSkill.user_id == user_id,
        models.StudentSkill.skill_id == skill_id
    ).first()

    if not student_skill:
        student_skill = models.StudentSkill(
            user_id=user_id,
            skill_id=skill_id,
            self_rating=3,
            trust_score=25,
            badge_tier=models.BadgeTier.declared
        )
        db.add(student_skill)
        db.flush()

    # Prevent duplicate evidence
    existing_ev = db.query(models.SkillEvidence).filter(
        models.SkillEvidence.student_skill_id == student_skill.id,
        models.SkillEvidence.evidence_type == evidence_type,
        models.SkillEvidence.evidence_ref_id == evidence_ref_id
    ).first()

    if not existing_ev:
        ev = models.SkillEvidence(
            student_skill_id=student_skill.id,
            evidence_type=evidence_type,
            evidence_ref_id=evidence_ref_id,
            weight=weight,
            verified_at=datetime.now(timezone.utc)
        )
        db.add(ev)
        db.commit()

    return recalculate_trust_score(student_skill.id, db)
