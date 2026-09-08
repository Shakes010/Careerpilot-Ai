from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import ApiResponse
from app.schemas.project import (
    ProjectCreateRequest, ProjectUpdateRequest, TaskCreateRequest, TaskUpdateRequest,
    VerificationCreateRequest, MemberRoleUpdateRequest, ProjectResponse, ProjectMemberResponse,
    ProjectJoinRequestResponse, ProjectTaskResponse, ProjectVerificationResponse,
    ProjectProgressResponse
)
from app.models.project import ProjectStatus, ProjectVisibility, MemberRole, TaskStatus
from app.models.user import User
from app.services.project_service import ProjectService
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/projects", tags=["Project Collaboration"])

@router.get("", response_model=ApiResponse[dict])
def list_projects(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    status: Optional[ProjectStatus] = Query(None),
    visibility: Optional[ProjectVisibility] = Query(ProjectVisibility.PUBLIC),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Browse public collaboration projects."""
    service = ProjectService(db)
    projects, total = service.list_projects(
        search=search,
        category=category,
        status_enum=status,
        visibility=visibility,
        page=page,
        page_size=page_size
    )
    return ApiResponse(
        success=True,
        data={
            "projects": [p.model_dump() for p in projects],
            "pagination": {"total": total, "page": page, "page_size": page_size}
        },
        message="Projects loaded."
    )

@router.post("", response_model=ApiResponse[ProjectResponse], status_code=status.HTTP_201_CREATED)
def create_project(
    req: ProjectCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new collaboration project (Authenticated student becomes Project Owner)."""
    service = ProjectService(db)
    project = service.create_project(current_user.id, req)
    return ApiResponse(
        success=True,
        data=project,
        message=f"Project '{project.title}' created successfully."
    )

@router.get("/{project_id}", response_model=ApiResponse[ProjectResponse])
def get_project_details(
    project_id: str,
    db: Session = Depends(get_db)
):
    """Get complete project details including members, tasks, progress, and verification status."""
    service = ProjectService(db)
    project = service.get_project_details(project_id)
    return ApiResponse(
        success=True,
        data=project,
        message="Project details retrieved."
    )

@router.put("/{project_id}", response_model=ApiResponse[ProjectResponse])
def update_project(
    project_id: str,
    req: ProjectUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update project settings (Project Owner only)."""
    service = ProjectService(db)
    updated = service.update_project(current_user.id, project_id, req)
    return ApiResponse(
        success=True,
        data=updated,
        message="Project settings updated."
    )

@router.delete("/{project_id}", response_model=ApiResponse[dict])
def delete_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete project (Project Owner only)."""
    service = ProjectService(db)
    service.delete_project(current_user.id, project_id)
    return ApiResponse(
        success=True,
        data={"id": project_id},
        message="Project deleted."
    )

# --- FEATURE 31: JOIN REQUESTS ---
@router.post("/{project_id}/join", response_model=ApiResponse[ProjectJoinRequestResponse])
def request_to_join(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit a request to join a public project."""
    service = ProjectService(db)
    req_resp = service.request_to_join(current_user.id, project_id)
    return ApiResponse(
        success=True,
        data=req_resp,
        message="Join request submitted."
    )

@router.get("/{project_id}/join-requests", response_model=ApiResponse[List[ProjectJoinRequestResponse]])
def get_join_requests(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List pending join requests for project (Project Owner only)."""
    service = ProjectService(db)
    requests = service.get_join_requests(current_user.id, project_id)
    return ApiResponse(
        success=True,
        data=requests,
        message="Join requests retrieved."
    )

@router.post("/{project_id}/join-requests/{request_id}/accept", response_model=ApiResponse[ProjectMemberResponse])
def accept_join_request(
    project_id: str,
    request_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Accept a student's join request (Project Owner only)."""
    service = ProjectService(db)
    member = service.accept_join_request(current_user.id, project_id, request_id)
    return ApiResponse(
        success=True,
        data=member,
        message=f"Join request accepted. {member.student_name} added to team."
    )

@router.post("/{project_id}/join-requests/{request_id}/reject", response_model=ApiResponse[ProjectJoinRequestResponse])
def reject_join_request(
    project_id: str,
    request_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reject a student's join request (Project Owner only)."""
    service = ProjectService(db)
    rejected = service.reject_join_request(current_user.id, project_id, request_id)
    return ApiResponse(
        success=True,
        data=rejected,
        message="Join request rejected."
    )

# --- FEATURE 32: TEAM MEMBERS ---
@router.get("/{project_id}/members", response_model=ApiResponse[List[ProjectMemberResponse]])
def get_project_members(
    project_id: str,
    db: Session = Depends(get_db)
):
    """List active team members for a project."""
    service = ProjectService(db)
    proj = service.get_project_details(project_id)
    return ApiResponse(
        success=True,
        data=proj.members,
        message="Team members retrieved."
    )

@router.post("/{project_id}/members/{student_id}/role", response_model=ApiResponse[ProjectMemberResponse])
def update_member_role(
    project_id: str,
    student_id: str,
    req: MemberRoleUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Assign team role to a member (Project Owner only)."""
    service = ProjectService(db)
    updated = service.update_member_role(current_user.id, project_id, student_id, req.role)
    return ApiResponse(
        success=True,
        data=updated,
        message=f"Team member role updated to {req.role.value}."
    )

@router.delete("/{project_id}/members/{student_id}", response_model=ApiResponse[dict])
def remove_member(
    project_id: str,
    student_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a member from the team (Project Owner only)."""
    service = ProjectService(db)
    service.remove_member(current_user.id, project_id, student_id)
    return ApiResponse(
        success=True,
        data={"student_id": student_id},
        message="Member removed from project team."
    )

# --- FEATURE 32: TASKS ---
@router.get("/{project_id}/tasks", response_model=ApiResponse[List[ProjectTaskResponse]])
def list_tasks(
    project_id: str,
    db: Session = Depends(get_db)
):
    """List tasks assigned within a project."""
    service = ProjectService(db)
    proj = service.get_project_details(project_id)
    return ApiResponse(
        success=True,
        data=proj.tasks,
        message="Tasks retrieved."
    )

@router.post("/{project_id}/tasks", response_model=ApiResponse[ProjectTaskResponse], status_code=status.HTTP_201_CREATED)
def create_task(
    project_id: str,
    req: TaskCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create and assign a project task (Project Members only)."""
    service = ProjectService(db)
    task = service.create_task(current_user.id, project_id, req)
    return ApiResponse(
        success=True,
        data=task,
        message=f"Task '{task.title}' created."
    )

@router.put("/{project_id}/tasks/{task_id}", response_model=ApiResponse[ProjectTaskResponse])
def update_task(
    project_id: str,
    task_id: str,
    req: TaskUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update task details (Title, Description, Priority, Assignee)."""
    service = ProjectService(db)
    task = service.update_task(current_user.id, project_id, task_id, req)
    return ApiResponse(
        success=True,
        data=task,
        message=f"Task '{task.title}' updated."
    )

@router.patch("/{project_id}/tasks/{task_id}/status", response_model=ApiResponse[ProjectTaskResponse])
def update_task_status(
    project_id: str,
    task_id: str,
    status: TaskStatus = Query(..., description="TODO, IN_PROGRESS, or COMPLETED"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update task status (TODO -> IN_PROGRESS -> COMPLETED)."""
    service = ProjectService(db)
    task = service.update_task(current_user.id, project_id, task_id, TaskUpdateRequest(status=status))
    return ApiResponse(
        success=True,
        data=task,
        message=f"Task status updated to {status.value}."
    )

@router.delete("/{project_id}/tasks/{task_id}", response_model=ApiResponse[dict])
def delete_task(
    project_id: str,
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a task (Project Owner only)."""
    service = ProjectService(db)
    service.delete_task(current_user.id, project_id, task_id)
    return ApiResponse(
        success=True,
        data={"task_id": task_id},
        message="Task deleted."
    )

# --- FEATURE 33: PROGRESS TRACKING ---
@router.get("/{project_id}/progress", response_model=ApiResponse[ProjectProgressResponse])
def get_project_progress(
    project_id: str,
    db: Session = Depends(get_db)
):
    """Calculate project progress percentage dynamically from tasks."""
    service = ProjectService(db)
    progress = service.get_progress(project_id)
    return ApiResponse(
        success=True,
        data=progress,
        message="Project progress calculated."
    )

# --- FEATURE 34: COMPLETION VERIFICATION ---
@router.post("/{project_id}/verification", response_model=ApiResponse[ProjectVerificationResponse])
def submit_for_verification(
    project_id: str,
    req: VerificationCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit finished project for verification review (Project Owner only)."""
    service = ProjectService(db)
    ver = service.submit_for_verification(current_user.id, project_id, req)
    return ApiResponse(
        success=True,
        data=ver,
        message="Project submitted for verification review."
    )

@router.get("/{project_id}/verification", response_model=ApiResponse[Optional[ProjectVerificationResponse]])
def get_verification_status(
    project_id: str,
    db: Session = Depends(get_db)
):
    """Check current project completion verification status."""
    service = ProjectService(db)
    ver = service.get_verification_status(project_id)
    return ApiResponse(
        success=True,
        data=ver,
        message="Verification status retrieved."
    )
