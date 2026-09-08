from typing import List, Tuple, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.project import (
    Project, ProjectJoinRequest, ProjectMember, ProjectTask, ProjectVerification,
    ProjectStatus, ProjectVisibility, MemberRole, MemberStatus, JoinRequestStatus,
    TaskStatus, VerificationStatus
)
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import (
    ProjectCreateRequest, ProjectUpdateRequest, TaskCreateRequest, TaskUpdateRequest,
    VerificationCreateRequest, ProjectResponse, ProjectMemberResponse,
    ProjectJoinRequestResponse, ProjectTaskResponse, ProjectVerificationResponse,
    ProjectProgressResponse
)

class ProjectService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ProjectRepository(db)

    def list_projects(
        self,
        search: str = None,
        category: str = None,
        status_enum: ProjectStatus = None,
        visibility: ProjectVisibility = ProjectVisibility.PUBLIC,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[ProjectResponse], int]:
        projects, total = self.repo.list_projects(
            search=search,
            category=category,
            status=status_enum,
            visibility=visibility,
            page=page,
            page_size=page_size
        )
        return [self._format_project(p) for p in projects], total

    def get_project_details(self, project_id: str) -> ProjectResponse:
        project = self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")
        return self._format_project(project)

    def create_project(self, student_id: str, req: ProjectCreateRequest) -> ProjectResponse:
        project = Project(
            owner_id=student_id,
            title=req.title.strip(),
            description=req.description.strip(),
            category=req.category.strip(),
            technology_stack=req.technology_stack.strip() if req.technology_stack else None,
            visibility=req.visibility,
            maximum_members=req.maximum_members,
            status=ProjectStatus.OPEN
        )

        owner_member = ProjectMember(
            student_id=student_id,
            role=MemberRole.OWNER,
            status=MemberStatus.ACTIVE
        )

        created = self.repo.create_project(project, owner_member)
        return self._format_project(created)

    def update_project(self, student_id: str, project_id: str, req: ProjectUpdateRequest) -> ProjectResponse:
        project = self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

        if project.owner_id != student_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the project owner can edit project settings.")

        updates = req.model_dump(exclude_unset=True)
        updated = self.repo.update_project(project, updates)
        return self._format_project(updated)

    def delete_project(self, student_id: str, project_id: str) -> bool:
        project = self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

        if project.owner_id != student_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the project owner can delete this project.")

        return self.repo.delete_project(project)

    # --- FEATURE 31: JOIN REQUESTS ---
    def request_to_join(self, student_id: str, project_id: str) -> ProjectJoinRequestResponse:
        project = self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

        # Check project visibility & status
        if project.visibility == ProjectVisibility.PRIVATE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot request to join a private project.")
        if project.status in [ProjectStatus.CLOSED, ProjectStatus.VERIFIED]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cannot join a project with status '{project.status.value}'.")

        # Check team capacity
        active_count = self.repo.count_active_members(project_id)
        if active_count >= project.maximum_members:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Team is already full.")

        # Check existing member
        existing_member = self.repo.get_member(project_id, student_id)
        if existing_member:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are already a member of this project.")

        # Check existing pending join request
        existing_req = self.repo.get_join_request(project_id, student_id)
        if existing_req:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Join request already pending.")

        join_req = ProjectJoinRequest(
            project_id=project_id,
            student_id=student_id,
            status=JoinRequestStatus.PENDING
        )
        created = self.repo.create_join_request(join_req)
        return self._format_join_request(created)

    def get_join_requests(self, student_id: str, project_id: str) -> List[ProjectJoinRequestResponse]:
        project = self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

        if project.owner_id != student_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only project owner can view join requests.")

        requests = self.repo.get_join_requests_for_project(project_id)
        return [self._format_join_request(r) for r in requests]

    def accept_join_request(self, student_id: str, project_id: str, request_id: str) -> ProjectMemberResponse:
        project = self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

        if project.owner_id != student_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only project owner can accept join requests.")

        join_req = self.repo.get_join_request_by_id(request_id)
        if not join_req or join_req.project_id != project_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Join request not found.")

        if join_req.status != JoinRequestStatus.PENDING:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Join request is already {join_req.status.value}.")

        # Check team capacity on backend
        active_count = self.repo.count_active_members(project_id)
        if active_count >= project.maximum_members:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot accept request. Team is already full.")

        # Update request
        self.repo.update_join_request_status(join_req, JoinRequestStatus.ACCEPTED)

        # Create member record
        member = ProjectMember(
            project_id=project_id,
            student_id=join_req.student_id,
            role=MemberRole.MEMBER,
            status=MemberStatus.ACTIVE
        )
        created_member = self.repo.add_member(member)
        return self._format_member(created_member)

    def reject_join_request(self, student_id: str, project_id: str, request_id: str) -> ProjectJoinRequestResponse:
        project = self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

        if project.owner_id != student_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only project owner can reject join requests.")

        join_req = self.repo.get_join_request_by_id(request_id)
        if not join_req or join_req.project_id != project_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Join request not found.")

        updated = self.repo.update_join_request_status(join_req, JoinRequestStatus.REJECTED)
        return self._format_join_request(updated)

    # --- FEATURE 32: TEAM MEMBERS & ROLES ---
    def update_member_role(self, student_id: str, project_id: str, target_student_id: str, role: MemberRole) -> ProjectMemberResponse:
        project = self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

        if project.owner_id != student_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only project owner can update team roles.")

        member = self.repo.get_member(project_id, target_student_id)
        if not member:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found in project.")

        updated = self.repo.update_member_role(member, role)
        return self._format_member(updated)

    def remove_member(self, student_id: str, project_id: str, target_student_id: str) -> bool:
        project = self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

        if project.owner_id != student_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only project owner can remove team members.")

        if target_student_id == project.owner_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Do not allow removing the project owner.")

        member = self.repo.get_member(project_id, target_student_id)
        if not member:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found in project.")

        self.repo.remove_member(member)
        return True

    # --- FEATURE 32: TASKS ---
    def create_task(self, student_id: str, project_id: str, req: TaskCreateRequest) -> ProjectTaskResponse:
        project = self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

        # Ensure creator is an active member or owner
        creator_member = self.repo.get_member(project_id, student_id)
        if not creator_member and project.owner_id != student_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only project members can create tasks.")

        # Ensure assignee is an active team member
        if req.assigned_to:
            assignee_member = self.repo.get_member(project_id, req.assigned_to)
            if not assignee_member:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot assign task to a non-member.")

        task = ProjectTask(
            project_id=project_id,
            title=req.title.strip(),
            description=req.description.strip() if req.description else None,
            assigned_to=req.assigned_to,
            created_by=student_id,
            priority=req.priority,
            status=TaskStatus.TODO,
            due_date=req.due_date
        )

        created = self.repo.create_task(task)
        
        # Automatically update project status to IN_PROGRESS if OPEN
        if project.status == ProjectStatus.OPEN:
            self.repo.update_project(project, {"status": ProjectStatus.IN_PROGRESS})

        return self._format_task(created)

    def update_task(self, student_id: str, project_id: str, task_id: str, req: TaskUpdateRequest) -> ProjectTaskResponse:
        project = self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

        member = self.repo.get_member(project_id, student_id)
        if not member and project.owner_id != student_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only project members can update tasks.")

        task = self.repo.get_task(task_id)
        if not task or task.project_id != project_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")

        # Validate assignee if updated
        if req.assigned_to:
            assignee_member = self.repo.get_member(project_id, req.assigned_to)
            if not assignee_member:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot assign task to a non-member.")

        updates = req.model_dump(exclude_unset=True)
        updated = self.repo.update_task(task, updates)
        return self._format_task(updated)

    def delete_task(self, student_id: str, project_id: str, task_id: str) -> bool:
        project = self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

        if project.owner_id != student_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only project owner can delete tasks.")

        task = self.repo.get_task(task_id)
        if not task or task.project_id != project_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")

        return self.repo.delete_task(task)

    # --- FEATURE 33: PROGRESS TRACKING ---
    def get_progress(self, project_id: str) -> ProjectProgressResponse:
        project = self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

        total_tasks = len(project.tasks)
        completed_tasks = sum(1 for t in project.tasks if t.status == TaskStatus.COMPLETED)
        todo_tasks = sum(1 for t in project.tasks if t.status == TaskStatus.TODO)
        in_progress_tasks = sum(1 for t in project.tasks if t.status == TaskStatus.IN_PROGRESS)

        progress_pct = round((completed_tasks / total_tasks) * 100, 1) if total_tasks > 0 else 0.0

        return ProjectProgressResponse(
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            todo_tasks=todo_tasks,
            in_progress_tasks=in_progress_tasks,
            progress_percentage=progress_pct
        )

    # --- FEATURE 34: COMPLETION VERIFICATION ---
    def submit_for_verification(self, student_id: str, project_id: str, req: VerificationCreateRequest) -> ProjectVerificationResponse:
        project = self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

        if project.owner_id != student_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the project owner can submit for verification.")

        # Update project status -> VERIFICATION_PENDING
        self.repo.update_project(project, {"status": ProjectStatus.VERIFICATION_PENDING})

        verification = ProjectVerification(
            project_id=project_id,
            requested_by=student_id,
            status=VerificationStatus.PENDING,
            verification_notes=req.verification_notes
        )
        created = self.repo.create_verification(verification)
        return self._format_verification(created)

    def get_verification_status(self, project_id: str) -> Optional[ProjectVerificationResponse]:
        project = self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")

        ver = self.repo.get_latest_verification(project_id)
        return self._format_verification(ver) if ver else None

    # --- FORMATTING HELPERS ---
    def _format_project(self, p: Project) -> ProjectResponse:
        members_resp = [self._format_member(m) for m in p.members if m.status == MemberStatus.ACTIVE]
        tasks_resp = [self._format_task(t) for t in p.tasks]
        ver = self.repo.get_latest_verification(p.id)

        # Progress calculation
        total = len(p.tasks)
        comp = sum(1 for t in p.tasks if t.status == TaskStatus.COMPLETED)
        todo = sum(1 for t in p.tasks if t.status == TaskStatus.TODO)
        inp = sum(1 for t in p.tasks if t.status == TaskStatus.IN_PROGRESS)
        pct = round((comp / total) * 100, 1) if total > 0 else 0.0

        progress_resp = ProjectProgressResponse(
            total_tasks=total,
            completed_tasks=comp,
            todo_tasks=todo,
            in_progress_tasks=inp,
            progress_percentage=pct
        )

        return ProjectResponse(
            id=p.id,
            owner_id=p.owner_id,
            owner_name=p.owner.full_name if p.owner else "Unknown",
            title=p.title,
            description=p.description,
            category=p.category,
            technology_stack=p.technology_stack,
            visibility=p.visibility,
            maximum_members=p.maximum_members,
            status=p.status,
            created_at=p.created_at,
            updated_at=p.updated_at,
            members=members_resp,
            tasks=tasks_resp,
            verification=self._format_verification(ver) if ver else None,
            progress=progress_resp
        )

    def _format_member(self, m: ProjectMember) -> ProjectMemberResponse:
        return ProjectMemberResponse(
            id=m.id,
            project_id=m.project_id,
            student_id=m.student_id,
            student_name=m.student.full_name if m.student else "",
            student_email=m.student.email if m.student else "",
            role=m.role,
            status=m.status,
            joined_at=m.joined_at
        )

    def _format_join_request(self, r: ProjectJoinRequest) -> ProjectJoinRequestResponse:
        return ProjectJoinRequestResponse(
            id=r.id,
            project_id=r.project_id,
            student_id=r.student_id,
            student_name=r.student.full_name if r.student else "",
            student_email=r.student.email if r.student else "",
            status=r.status,
            created_at=r.created_at
        )

    def _format_task(self, t: ProjectTask) -> ProjectTaskResponse:
        return ProjectTaskResponse(
            id=t.id,
            project_id=t.project_id,
            title=t.title,
            description=t.description,
            assigned_to=t.assigned_to,
            assignee_name=t.assignee.full_name if t.assignee else "Unassigned",
            created_by=t.created_by,
            priority=t.priority,
            status=t.status,
            due_date=t.due_date,
            created_at=t.created_at
        )

    def _format_verification(self, v: ProjectVerification) -> ProjectVerificationResponse:
        return ProjectVerificationResponse(
            id=v.id,
            project_id=v.project_id,
            requested_by=v.requested_by,
            requester_name=v.requester.full_name if v.requester else "",
            status=v.status,
            verification_notes=v.verification_notes,
            verified_by=v.verified_by,
            verified_at=v.verified_at,
            created_at=v.created_at
        )
