import json
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from app.database import get_db
import app.models as models
from app.services.auth_service import get_current_user, get_current_user_optional
from app.services.trust_meter_service import add_skill_evidence
from app.services.code_executor import execute_multi_language_code

router = APIRouter(prefix="/assessments", tags=["Assessments & Checkpoints"])

class StartAssessmentRequest(BaseModel):
    chosen_language: Optional[str] = "python"

class SubmitCheckpointRequest(BaseModel):
    submitted_code: str
    language: Optional[str] = "python"
    paste_event_count: int = 0
    paste_char_count: int = 0
    time_spent_seconds: int = 0

class FlagExplanationRequest(BaseModel):
    explanation: str

@router.get("")
def list_assessments(
    current_user: Optional[models.User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    all_ass = db.query(models.Assessment).order_by(models.Assessment.created_at.asc(), models.Assessment.assessment_name.asc()).all()

    # Group assessments by track (by skill_id or aptitude topic)
    track_groups = {}
    for ass in all_ass:
        if ass.skill_id:
            key = str(ass.skill_id)
        else:
            key = "flexible_" + (ass.assessment_name.split(":")[0] if ":" in ass.assessment_name else ass.assessment_name)
        if key not in track_groups:
            track_groups[key] = []
        track_groups[key].append(ass)

    tracks = []
    for key, ass_list in track_groups.items():
        if not current_user:
            first_ass = ass_list[0]
            clean_name = first_ass.assessment_name
            if "Variant" in clean_name:
                clean_name = clean_name.split("(")[0].strip()
            checkpoints_count = len(first_ass.checkpoints)
            tracks.append({
                "id": str(first_ass.id),
                "assessment_name": clean_name,
                "assessment_type": first_ass.assessment_type.value,
                "skill_id": str(first_ass.skill_id) if first_ass.skill_id else None,
                "skill_name": first_ass.skill.skill_name if first_ass.skill else "General Programming",
                "is_language_flexible": first_ass.is_language_flexible,
                "total_checkpoints": checkpoints_count or 3,
                "status": "available",
                "status_label": "Assessment Ready",
                "status_desc": "Sequential checkpoint verification challenge.",
                "can_start": True,
                "is_retake": False
            })
            continue

        # Authenticated student: find the active or next assessment
        chosen_ass = None
        chosen_status = "available"
        chosen_label = "New Assessment Ready"
        chosen_desc = "Sequential checkpoint verification challenge."
        can_start = True
        is_retake = False

        for ass in ass_list:
            latest_att = db.query(models.AssessmentAttempt).filter(
                models.AssessmentAttempt.assessment_id == ass.id,
                models.AssessmentAttempt.user_id == current_user.id
            ).order_by(models.AssessmentAttempt.taken_at.desc()).first()

            if latest_att:
                if latest_att.status == models.AttemptStatus.passed:
                    # User completed and passed: Finished assessments MUST NOT be present in list!
                    # Continue loop to serve next new variant!
                    continue

                if latest_att.status == models.AttemptStatus.flagged_pending:
                    # Flagged attempt: wait for admin response
                    chosen_ass = ass
                    chosen_status = "flagged_pending"
                    chosen_label = "⏳ Waiting for Admin Response (Flagged)"
                    chosen_desc = f"Your attempt was flagged for review ({latest_att.flag_reason or 'Paste/timing anomaly'}). Awaiting administrator response."
                    can_start = False
                    is_retake = False
                    break

                if latest_att.status == models.AttemptStatus.flagged_rejected:
                    # Admin rejected: retake same assessment
                    chosen_ass = ass
                    chosen_status = "flagged_rejected"
                    chosen_label = "⚠️ Admin Review: Attempt Rejected"
                    chosen_desc = "Administrator rejected previous submission. You must retake this same assessment to verify."
                    can_start = True
                    is_retake = True
                    break

            # If no attempt, this is the active new assessment variant!
            chosen_ass = ass
            chosen_status = "available"
            chosen_label = "New Assessment Ready"
            chosen_desc = "Sequential checkpoint verification challenge."
            can_start = True
            is_retake = False
            break

        if chosen_ass:
            clean_name = chosen_ass.assessment_name
            checkpoints_count = len(chosen_ass.checkpoints)
            tracks.append({
                "id": str(chosen_ass.id),
                "assessment_name": clean_name,
                "assessment_type": chosen_ass.assessment_type.value,
                "skill_id": str(chosen_ass.skill_id) if chosen_ass.skill_id else None,
                "skill_name": chosen_ass.skill.skill_name if chosen_ass.skill else "General Programming",
                "is_language_flexible": chosen_ass.is_language_flexible,
                "total_checkpoints": checkpoints_count or 3,
                "status": chosen_status,
                "status_label": chosen_label,
                "status_desc": chosen_desc,
                "can_start": can_start,
                "is_retake": is_retake
            })

    return tracks

# 1. Skill-Based Assessment Selection (Active/New Variant Serving)
@router.get("/by-skill/{skill_id}")
def get_assessment_by_skill(
    skill_id: str,
    current_user: Optional[models.User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    target_skill_id = None
    try:
        import uuid
        uuid.UUID(skill_id)
        target_skill_id = skill_id
    except (ValueError, AttributeError):
        sk = db.query(models.Skill).filter(func.lower(models.Skill.skill_name) == skill_id.lower()).first()
        if sk:
            target_skill_id = sk.id

    pool = []
    if target_skill_id:
        pool = db.query(models.Assessment).filter(
            models.Assessment.skill_id == target_skill_id
        ).order_by(models.Assessment.created_at.asc(), models.Assessment.assessment_name.asc()).all()

    if not pool:
        pool = db.query(models.Assessment).filter(
            models.Assessment.is_language_flexible == True
        ).order_by(models.Assessment.created_at.asc()).all()

    if not pool:
        raise HTTPException(status_code=404, detail="No assessment found for this skill")

    # Pick the next uncompleted or retake assessment for user
    target_ass = pool[0]
    if current_user:
        for a in pool:
            latest_att = db.query(models.AssessmentAttempt).filter(
                models.AssessmentAttempt.assessment_id == a.id,
                models.AssessmentAttempt.user_id == current_user.id
            ).order_by(models.AssessmentAttempt.taken_at.desc()).first()

            if latest_att:
                if latest_att.status == models.AttemptStatus.passed:
                    continue # Passed: check next new variant
                if latest_att.status == models.AttemptStatus.flagged_pending:
                    target_ass = a
                    break
                if latest_att.status == models.AttemptStatus.flagged_rejected:
                    target_ass = a
                    break
            target_ass = a
            break

    checkpoints = db.query(models.AssessmentCheckpoint).filter(
        models.AssessmentCheckpoint.assessment_id == target_ass.id
    ).order_by(models.AssessmentCheckpoint.sequence_order.asc()).all()

    clean_name = target_ass.assessment_name

    return {
        "id": str(target_ass.id),
        "assessment_name": clean_name,
        "assessment_type": target_ass.assessment_type.value,
        "skill_id": str(target_ass.skill_id) if target_ass.skill_id else None,
        "skill_name": target_ass.skill.skill_name if target_ass.skill else "General Programming",
        "is_language_flexible": target_ass.is_language_flexible,
        "variant_id": str(target_ass.id)[:6],
        "checkpoints": [
            {
                "id": str(cp.id),
                "sequence_order": cp.sequence_order,
                "title": cp.title,
                "instructions": cp.instructions,
                "validation_test": cp.validation_test
            }
            for cp in checkpoints
        ]
    }

@router.get("/{assessment_id}")
def get_assessment_details(assessment_id: str, db: Session = Depends(get_db)):
    target_ass = db.query(models.Assessment).filter(models.Assessment.id == assessment_id).first()
    if not target_ass:
        raise HTTPException(status_code=404, detail="Assessment not found")

    # Anti-Collusion & Candidate Differentiation:
    # Randomize variant from the pool so candidates do not receive identical questions
    if target_ass.skill_id:
        pool = db.query(models.Assessment).filter(models.Assessment.skill_id == target_ass.skill_id).all()
        if len(pool) > 1:
            target_ass = db.query(models.Assessment).filter(models.Assessment.skill_id == target_ass.skill_id).order_by(func.random()).first()
    elif target_ass.is_language_flexible:
        pool = db.query(models.Assessment).filter(models.Assessment.is_language_flexible == True).all()
        if len(pool) > 1:
            target_ass = db.query(models.Assessment).filter(models.Assessment.is_language_flexible == True).order_by(func.random()).first()

    checkpoints = db.query(models.AssessmentCheckpoint).filter(
        models.AssessmentCheckpoint.assessment_id == target_ass.id
    ).order_by(models.AssessmentCheckpoint.sequence_order.asc()).all()

    clean_name = target_ass.assessment_name
    if "Variant" in clean_name:
        clean_name = clean_name.split("(")[0].strip()

    return {
        "id": str(target_ass.id),
        "assessment_name": clean_name,
        "assessment_type": target_ass.assessment_type.value,
        "skill_id": str(target_ass.skill_id) if target_ass.skill_id else None,
        "skill_name": target_ass.skill.skill_name if target_ass.skill else "General Programming",
        "is_language_flexible": target_ass.is_language_flexible,
        "variant_id": str(target_ass.id)[:6],
        "checkpoints": [
            {
                "id": str(cp.id),
                "sequence_order": cp.sequence_order,
                "title": cp.title,
                "instructions": cp.instructions,
                "validation_test": cp.validation_test
            }
            for cp in checkpoints
        ]
    }

@router.post("/{assessment_id}/start")
def start_assessment_attempt(
    assessment_id: str,
    req: Optional[StartAssessmentRequest] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ass = db.query(models.Assessment).filter(models.Assessment.id == assessment_id).first()
    if not ass:
        raise HTTPException(status_code=404, detail="Assessment not found")

    # If an attempt is currently flagged and waiting for admin, block starting
    pending = db.query(models.AssessmentAttempt).filter(
        models.AssessmentAttempt.assessment_id == ass.id,
        models.AssessmentAttempt.user_id == current_user.id,
        models.AssessmentAttempt.status == models.AttemptStatus.flagged_pending
    ).first()
    if pending:
        raise HTTPException(
            status_code=400,
            detail="Your previous attempt is currently under Admin Review for an integrity flag. Please wait for administrator response."
        )

    attempt = models.AssessmentAttempt(
        user_id=current_user.id,
        assessment_id=ass.id,
        status=models.AttemptStatus.in_progress,
        score_pct=0.0,
        is_flagged=False
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return {
        "attempt_id": str(attempt.id),
        "assessment_name": ass.assessment_name,
        "is_language_flexible": ass.is_language_flexible,
        "chosen_language": req.chosen_language if (req and ass.is_language_flexible) else None,
        "status": attempt.status.value,
        "taken_at": attempt.taken_at.isoformat()
    }

@router.post("/attempts/{attempt_id}/checkpoints/{checkpoint_id}/submit")
def submit_checkpoint(
    attempt_id: str,
    checkpoint_id: str,
    req: SubmitCheckpointRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    attempt = db.query(models.AssessmentAttempt).filter(models.AssessmentAttempt.id == attempt_id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    if attempt.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to submit for this attempt")

    checkpoint = db.query(models.AssessmentCheckpoint).filter(models.AssessmentCheckpoint.id == checkpoint_id).first()
    if not checkpoint:
        raise HTTPException(status_code=404, detail="Checkpoint not found")

    ass = checkpoint.assessment

    # ENFORCE: sequence_order N requires sequence_order N-1 submission
    seq_order = checkpoint.sequence_order
    if seq_order > 1:
        prev_cp = db.query(models.AssessmentCheckpoint).filter(
            models.AssessmentCheckpoint.assessment_id == checkpoint.assessment_id,
            models.AssessmentCheckpoint.sequence_order == seq_order - 1
        ).first()

        if prev_cp:
            prev_sub = db.query(models.CheckpointSubmission).filter(
                models.CheckpointSubmission.attempt_id == attempt.id,
                models.CheckpointSubmission.checkpoint_id == prev_cp.id
            ).first()

            if not prev_sub:
                raise HTTPException(
                    status_code=400,
                    detail=f"Sequence order enforced. You must complete Checkpoint {seq_order - 1} ({prev_cp.title}) before starting Checkpoint {seq_order}."
                )

    # Code Execution & Test Case Validation
    test_cases_summary = "1/1 test cases passed"
    runtime_error = None
    is_test_passed = True
    exec_result = None

    if ass.is_language_flexible and checkpoint.validation_test:
        try:
            test_cases = json.loads(checkpoint.validation_test)
            if isinstance(test_cases, list):
                exec_result = execute_multi_language_code(
                    submitted_code=req.submitted_code,
                    language=req.language or "python",
                    test_cases=test_cases
                )
                test_cases_summary = f"{exec_result['passed_cases']}/{exec_result['total_cases']} test cases passed"
                runtime_error = exec_result.get("error")
                is_test_passed = exec_result["all_passed"]
        except Exception as e:
            print(f"Error parsing validation test cases: {e}")

    # Build formatted results for UI
    formatted_results = []
    if exec_result and "results" in exec_result:
        for r in exec_result["results"]:
            formatted_results.append({
                "index": r["test_case"],
                "passed": r["passed"],
                "error": runtime_error if not r["passed"] else None
            })

    # If test validation failed, block submission completion and prompt resubmission
    if not is_test_passed:
        return {
            "status": "test_failed",
            "is_flagged": False,
            "test_cases_summary": test_cases_summary,
            "passed_count": exec_result.get("passed_cases", 0) if exec_result else 0,
            "total_cases": exec_result.get("total_cases", 0) if exec_result else 0,
            "results": formatted_results,
            "error": runtime_error,
            "message": f"Test case validation failed ({test_cases_summary}). Debug your solution code and resubmit."
        }

    # Save submission
    sub = models.CheckpointSubmission(
        attempt_id=attempt.id,
        checkpoint_id=checkpoint.id,
        submitted_code=req.submitted_code,
        language=req.language if ass.is_language_flexible else None,
        paste_event_count=req.paste_event_count,
        paste_char_count=req.paste_char_count,
        time_spent_seconds=req.time_spent_seconds
    )
    db.add(sub)
    db.commit()

    # Behavioral anti-cheat flagging logic
    if req.paste_char_count > 150 or req.time_spent_seconds < 5:
        attempt.is_flagged = True
        attempt.status = models.AttemptStatus.flagged_pending
        attempt.flag_reason = f"Structural anomaly detected: Large paste event ({req.paste_char_count} chars) in {req.time_spent_seconds}s."
        db.commit()

        return {
            "submission_id": str(sub.id),
            "status": "flagged_pending",
            "is_flagged": True,
            "test_cases_summary": test_cases_summary,
            "passed_count": exec_result.get("passed_cases", 1) if exec_result else 1,
            "total_cases": exec_result.get("total_cases", 1) if exec_result else 1,
            "results": formatted_results,
            "message": "Attempt flagged due to paste/timing anomaly. Please submit your written code explanation for human admin review."
        }

    # Check if all checkpoints completed
    total_cps = db.query(models.AssessmentCheckpoint).filter(
        models.AssessmentCheckpoint.assessment_id == checkpoint.assessment_id
    ).count()

    completed_cps = db.query(models.CheckpointSubmission).filter(
        models.CheckpointSubmission.attempt_id == attempt.id
    ).count()

    if completed_cps >= total_cps and not attempt.is_flagged:
        attempt.status = models.AttemptStatus.passed
        attempt.score_pct = 95.0
        attempt.completed_at = datetime.now(timezone.utc)
        db.commit()

        # Award Verified Skill Evidence if assessment tied to a skill
        if ass and ass.skill_id:
            add_skill_evidence(
                user_id=str(current_user.id),
                skill_id=str(ass.skill_id),
                evidence_type=models.EvidenceType.assessment,
                evidence_ref_id=str(attempt.id),
                weight=0.75,
                db=db
            )

        return {
            "submission_id": str(sub.id),
            "status": "passed",
            "is_flagged": False,
            "test_cases_summary": test_cases_summary,
            "passed_count": exec_result.get("passed_cases", 1) if exec_result else 1,
            "total_cases": exec_result.get("total_cases", 1) if exec_result else 1,
            "results": formatted_results,
            "message": "Assessment passed successfully! Skill evidence verified."
        }

    return {
        "submission_id": str(sub.id),
        "status": attempt.status.value,
        "is_flagged": False,
        "test_cases_summary": test_cases_summary,
        "passed_count": exec_result.get("passed_cases", 1) if exec_result else 1,
        "total_cases": exec_result.get("total_cases", 1) if exec_result else 1,
        "results": formatted_results,
        "message": f"Checkpoint {seq_order} submitted successfully."
    }

@router.post("/attempts/{attempt_id}/explain")
def submit_flag_explanation(
    attempt_id: str,
    req: FlagExplanationRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    attempt = db.query(models.AssessmentAttempt).filter(models.AssessmentAttempt.id == attempt_id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    if attempt.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    attempt.flag_reason = f"{attempt.flag_reason} | Student Explanation: {req.explanation}"
    db.commit()

    return {
        "attempt_id": str(attempt.id),
        "status": attempt.status.value,
        "message": "Explanation submitted. Routed to Admin Review Queue."
    }
