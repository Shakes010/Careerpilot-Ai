from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.models.project import (
    Project, ProjectJoinRequest, ProjectMember, ProjectTask, ProjectVerification,
    ProjectStatus, ProjectVisibility, MemberRole, MemberStatus, JoinRequestStatus,
    TaskStatus, VerificationStatus
)

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, project_id: str) -> Optional[Project]:
        return self.db.query(Project).filter(Project.id == project_id).first()

    def list_projects(
        self,
        search: Optional[str] = None,
        category: Optional[str] = None,
        status: Optional[ProjectStatus] = None,
        visibility: Optional[ProjectVisibility] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Project], int]:
        query = self.db.query(Project)

        if visibility:
            query = query.filter(Project.visibility == visibility)

        if search:
            pattern = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Project.title.ilike(pattern),
                    Project.description.ilike(pattern),
                    Project.technology_stack.ilike(pattern)
                )
            )

        if category and category.lower() != "all":
            query = query.filter(Project.category.ilike(category.strip()))

        if status:
            query = query.filter(Project.status == status)

        total = query.count()
        offset = (page - 1) * page_size
        projects = query.order_by(Project.created_at.desc()).offset(offset).limit(page_size).all()

        return projects, total

    def create_project(self, project: Project, owner_member: ProjectMember) -> Project:
        self.db.add(project)
        self.db.flush()
        owner_member.project_id = project.id
        self.db.add(owner_member)
        self.db.commit()
        self.db.refresh(project)
        return project

    def update_project(self, project: Project, updates: dict) -> Project:
        for k, v in updates.items():
            if v is not None:
                setattr(project, k, v)
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete_project(self, project: Project) -> bool:
        self.db.delete(project)
        self.db.commit()
        return True

    # --- JOIN REQUESTS ---
    def get_join_request(self, project_id: str, student_id: str) -> Optional[ProjectJoinRequest]:
        return self.db.query(ProjectJoinRequest).filter(
            and_(
                ProjectJoinRequest.project_id == project_id,
                ProjectJoinRequest.student_id == student_id,
                ProjectJoinRequest.status == JoinRequestStatus.PENDING
            )
        ).first()

    def create_join_request(self, req: ProjectJoinRequest) -> ProjectJoinRequest:
        self.db.add(req)
        self.db.commit()
        self.db.refresh(req)
        return req

    def get_join_requests_for_project(self, project_id: str) -> List[ProjectJoinRequest]:
        return self.db.query(ProjectJoinRequest).filter(
            ProjectJoinRequest.project_id == project_id
        ).order_by(ProjectJoinRequest.created_at.desc()).all()

    def get_join_request_by_id(self, request_id: str) -> Optional[ProjectJoinRequest]:
        return self.db.query(ProjectJoinRequest).filter(ProjectJoinRequest.id == request_id).first()

    def update_join_request_status(self, req: ProjectJoinRequest, status: JoinRequestStatus) -> ProjectJoinRequest:
        req.status = status
        self.db.commit()
        self.db.refresh(req)
        return req

    # --- MEMBERS ---
    def get_member(self, project_id: str, student_id: str) -> Optional[ProjectMember]:
        return self.db.query(ProjectMember).filter(
            and_(
                ProjectMember.project_id == project_id,
                ProjectMember.student_id == student_id,
                ProjectMember.status == MemberStatus.ACTIVE
            )
        ).first()

    def count_active_members(self, project_id: str) -> int:
        return self.db.query(ProjectMember).filter(
            and_(
                ProjectMember.project_id == project_id,
                ProjectMember.status == MemberStatus.ACTIVE
            )
        ).count()

    def add_member(self, member: ProjectMember) -> ProjectMember:
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        return member

    def update_member_role(self, member: ProjectMember, role: MemberRole) -> ProjectMember:
        member.role = role
        self.db.commit()
        self.db.refresh(member)
        return member

    def remove_member(self, member: ProjectMember) -> ProjectMember:
        member.status = MemberStatus.REMOVED
        self.db.commit()
        self.db.refresh(member)
        return member

    # --- TASKS ---
    def create_task(self, task: ProjectTask) -> ProjectTask:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_task(self, task_id: str) -> Optional[ProjectTask]:
        return self.db.query(ProjectTask).filter(ProjectTask.id == task_id).first()

    def update_task(self, task: ProjectTask, updates: dict) -> ProjectTask:
        for k, v in updates.items():
            if v is not None:
                setattr(task, k, v)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, task: ProjectTask) -> bool:
        self.db.delete(task)
        self.db.commit()
        return True

    # --- VERIFICATION ---
    def get_latest_verification(self, project_id: str) -> Optional[ProjectVerification]:
        return self.db.query(ProjectVerification).filter(
            ProjectVerification.project_id == project_id
        ).order_by(ProjectVerification.created_at.desc()).first()

    def create_verification(self, verification: ProjectVerification) -> ProjectVerification:
        self.db.add(verification)
        self.db.commit()
        self.db.refresh(verification)
        return verification
