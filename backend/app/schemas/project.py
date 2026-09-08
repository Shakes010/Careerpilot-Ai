from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import date, datetime
from app.models.project import (
    ProjectStatus, ProjectVisibility, MemberRole, MemberStatus,
    JoinRequestStatus, TaskPriority, TaskStatus, VerificationStatus
)

class ProjectCreateRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=10)
    category: str = Field(default="Software Engineering")
    technology_stack: Optional[str] = "Python, Vue.js, PostgreSQL"
    visibility: ProjectVisibility = ProjectVisibility.PUBLIC
    maximum_members: int = Field(default=4, ge=1, le=20)

class ProjectUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    technology_stack: Optional[str] = None
    visibility: Optional[ProjectVisibility] = None
    maximum_members: Optional[int] = Field(None, ge=1, le=20)
    status: Optional[ProjectStatus] = None

class ProjectJoinRequestCreate(BaseModel):
    pitch_message: Optional[str] = None

class MemberRoleUpdateRequest(BaseModel):
    role: MemberRole

class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[date] = None

class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[date] = None

class VerificationCreateRequest(BaseModel):
    verification_notes: Optional[str] = "Project work completed and ready for verification review."

class ProjectJoinRequestResponse(BaseModel):
    id: str
    project_id: str
    student_id: str
    student_name: Optional[str] = ""
    student_email: Optional[str] = ""
    status: JoinRequestStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProjectMemberResponse(BaseModel):
    id: str
    project_id: str
    student_id: str
    student_name: Optional[str] = ""
    student_email: Optional[str] = ""
    role: MemberRole
    status: MemberStatus
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProjectTaskResponse(BaseModel):
    id: str
    project_id: str
    title: str
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    assignee_name: Optional[str] = None
    created_by: Optional[str] = None
    priority: TaskPriority
    status: TaskStatus
    due_date: Optional[date] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProjectVerificationResponse(BaseModel):
    id: str
    project_id: str
    requested_by: str
    requester_name: Optional[str] = ""
    status: VerificationStatus
    verification_notes: Optional[str] = None
    verified_by: Optional[str] = None
    verified_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProjectProgressResponse(BaseModel):
    total_tasks: int
    completed_tasks: int
    todo_tasks: int
    in_progress_tasks: int
    progress_percentage: float

class ProjectResponse(BaseModel):
    id: str
    owner_id: str
    owner_name: Optional[str] = ""
    title: str
    description: str
    category: str
    technology_stack: Optional[str] = None
    visibility: ProjectVisibility
    maximum_members: int
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime
    members: List[ProjectMemberResponse] = []
    tasks: List[ProjectTaskResponse] = []
    verification: Optional[ProjectVerificationResponse] = None
    progress: Optional[ProjectProgressResponse] = None

    model_config = ConfigDict(from_attributes=True)
