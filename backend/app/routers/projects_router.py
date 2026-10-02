from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
import app.models as models
from app.services.auth_service import get_current_user
from app.services.trust_meter_service import add_skill_evidence

router = APIRouter(prefix="/projects", tags=["Project Collaboration & Sandbox"])

class CreateProjectRequest(BaseModel):
    title: str
    description: Optional[str] = None
    repo_url: Optional[str] = None
    tech_stack: Optional[List[str]] = []

class AddTaskRequest(BaseModel):
    title: str
    assigned_to: Optional[str] = None

class AddMemberRequest(BaseModel):
    user_id: str
    role: Optional[str] = "Collaborator"

@router.get("")
def list_projects(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Get projects where user is owner or member
    user_projects = db.query(models.Project).filter(models.Project.user_id == current_user.id).order_by(models.Project.created_at.desc()).all()
    results = []
    for p in user_projects:
        total_tasks = db.query(models.Task).filter(models.Task.project_id == p.id).count()
        done_tasks = db.query(models.Task).filter(models.Task.project_id == p.id, models.Task.status == models.TaskStatus.done).count()
        progress_pct = int((done_tasks / total_tasks) * 100) if total_tasks > 0 else 0

        completion = db.query(models.ProjectCompletion).filter(models.ProjectCompletion.project_id == p.id).first()
        is_verified = (completion and completion.status == models.CompletionStatus.verified)

        results.append({
            "id": str(p.id),
            "title": p.title,
            "description": p.description,
            "repo_url": p.repo_url,
            "tech_stack": p.tech_stack or [],
            "status": p.status.value,
            "progress_pct": progress_pct,
            "total_tasks": total_tasks,
            "done_tasks": done_tasks,
            "is_verified": is_verified,
            "created_at": p.created_at.isoformat() if p.created_at else None
        })

    return results

@router.post("")
def create_project(req: CreateProjectRequest, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = models.Project(
        user_id=current_user.id,
        title=req.title,
        description=req.description,
        repo_url=req.repo_url,
        tech_stack=req.tech_stack or [],
        status=models.ProjectStatus.in_progress
    )
    db.add(project)
    db.flush()

    # Add owner as project member
    pm = models.ProjectMember(project_id=project.id, user_id=current_user.id, role="Project Lead")
    db.add(pm)

    # Initialize completion record
    comp = models.ProjectCompletion(project_id=project.id, status=models.CompletionStatus.pending)
    db.add(comp)

    db.commit()
    db.refresh(project)
    return project

@router.get("/{project_id}")
def get_project_details(project_id: str, db: Session = Depends(get_db)):
    p = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")

    members = db.query(models.ProjectMember).filter(models.ProjectMember.project_id == p.id).all()
    tasks = db.query(models.Task).filter(models.Task.project_id == p.id).all()
    completion = db.query(models.ProjectCompletion).filter(models.ProjectCompletion.project_id == p.id).first()

    total_tasks = len(tasks)
    done_tasks = sum(1 for t in tasks if t.status == models.TaskStatus.done)
    progress_pct = int((done_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    return {
        "id": str(p.id),
        "title": p.title,
        "description": p.description,
        "repo_url": p.repo_url,
        "tech_stack": p.tech_stack or [],
        "status": p.status.value,
        "progress_pct": progress_pct,
        "is_verified": (completion and completion.status == models.CompletionStatus.verified),
        "members": [
            {
                "id": str(m.id),
                "user_id": str(m.user_id),
                "full_name": m.user.full_name if m.user else "Member",
                "role": m.role
            }
            for m in members
        ],
        "tasks": [
            {
                "id": str(t.id),
                "title": t.title,
                "status": t.status.value,
                "assigned_to": str(t.assigned_to) if t.assigned_to else None,
                "assignee_name": t.assignee.full_name if t.assignee else "Unassigned"
            }
            for t in tasks
        ]
    }

@router.post("/{project_id}/tasks")
def add_task(project_id: str, req: AddTaskRequest, db: Session = Depends(get_db)):
    t = models.Task(
        project_id=project_id,
        title=req.title,
        assigned_to=req.assigned_to if req.assigned_to else None,
        status=models.TaskStatus.todo
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

@router.put("/tasks/{task_id}/status")
def update_task_status(task_id: str, new_status: str, db: Session = Depends(get_db)):
    t = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")

    t.status = models.TaskStatus(new_status)
    db.commit()
    return {"task_id": str(t.id), "new_status": t.status.value}

@router.post("/{project_id}/verify")
def verify_project_completion(project_id: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    p = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")

    comp = db.query(models.ProjectCompletion).filter(models.ProjectCompletion.project_id == p.id).first()
    if not comp:
        comp = models.ProjectCompletion(project_id=p.id)
        db.add(comp)

    comp.status = models.CompletionStatus.verified
    comp.verified_by = current_user.id
    comp.verified_at = datetime.now(timezone.utc)
    p.status = models.ProjectStatus.verified
    db.commit()

    # Trigger evidence insertion for all tech stack skills!
    tech_stack = p.tech_stack or []
    for tech_name in tech_stack:
        skill = db.query(models.Skill).filter(models.Skill.skill_name.ilike(tech_name)).first()
        if skill:
            add_skill_evidence(
                user_id=str(p.user_id),
                skill_id=str(skill.id),
                evidence_type=models.EvidenceType.project,
                evidence_ref_id=str(p.id),
                weight=0.60,
                db=db
            )

    return {"project_id": str(p.id), "status": "verified", "message": "Project verified successfully! Skill trust scores updated."}

@router.get("/sandbox/challenges")
def get_sandbox_challenges(db: Session = Depends(get_db)):
    challenges = db.query(models.CareerSandboxChallenge).all()
    return [
        {
            "id": str(c.id),
            "title": c.title,
            "description": c.description,
            "difficulty": c.difficulty,
            "skill_name": c.skill.skill_name if c.skill else "General CS"
        }
        for c in challenges
    ]
