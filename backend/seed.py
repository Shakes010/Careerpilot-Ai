import os
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.company import Company, VerificationStatus as CompanyVerificationStatus
from app.models.recruiter import Recruiter
from app.models.job import Job, JobSkill, EmploymentType, WorkMode, JobStatus, ModerationStatus
from app.models.skill import Skill
from app.models.project import (
    Project, ProjectMember, ProjectTask, ProjectStatus, ProjectVisibility, MemberRole, MemberStatus, TaskPriority, TaskStatus
)
from app.models.sandbox import SandboxChallenge, SandboxDifficulty, SandboxStatus
from app.models.notification import Notification

def seed_data():
    print("=== Initializing CareerPilot AI Database Seed ===")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Create Demo Admin User
        admin_email = "admin@careerpilot.ai"
        admin_user = User(
            email=admin_email,
            password_hash=get_password_hash("AdminPass123!"),
            full_name="System Administrator",
            phone="+91 90000 11111",
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin_user)
        db.flush()
        print(f"[OK] Created Admin User: {admin_user.full_name} ({admin_user.email})")

        # 2. Create Demo Student User
        student_email = "student@careerpilot.ai"
        student_user = User(
            email=student_email,
            password_hash=get_password_hash("Password123!"),
            full_name="Sensha Shaji",
            phone="+91 98765 00000",
            role=UserRole.STUDENT,
            is_active=True
        )
        db.add(student_user)
        db.flush()
        print(f"[OK] Created Student User: {student_user.full_name} ({student_user.email})")

        # 3. Create Demo Recruiter User & Verified Company
        demo_email = "sensha@careerpilot.ai"
        recruiter_user = User(
            email=demo_email,
            password_hash=get_password_hash("Password123!"),
            full_name="Sensha",
            phone="+91 98765 43210",
            role=UserRole.RECRUITER,
            is_active=True
        )
        db.add(recruiter_user)
        db.flush()
        print(f"[OK] Created Recruiter User: {recruiter_user.full_name} ({recruiter_user.email})")

        company = Company(
            name="CareerPilot Technologies",
            legal_name="CareerPilot AI Private Limited",
            email="hiring@careerpilot.ai",
            phone="+91 80 1234 5678",
            website="https://careerpilot.ai",
            industry="AI & HRTech",
            company_size="50-200 employees",
            description="CareerPilot AI is an evidence-based career development platform empowering students and connecting tech recruiters with verified talent.",
            location="Bengaluru, Karnataka, India",
            verification_status=CompanyVerificationStatus.VERIFIED,
            verification_notes="Verified official MCA final year showcase account."
        )
        db.add(company)
        db.flush()
        print(f"[OK] Created Company: {company.name} [VERIFIED]")

        recruiter = Recruiter(
            user_id=recruiter_user.id,
            company_id=company.id,
            designation="Senior Talent Acquisition Lead"
        )
        db.add(recruiter)
        db.flush()

        # 4. Seed Central Skills Taxonomy
        initial_skills = [
            {"name": "Python", "category": "Backend Engineering", "description": "Core Python programming."},
            {"name": "FastAPI", "category": "Backend Engineering", "description": "FastAPI REST framework."},
            {"name": "Vue.js", "category": "Frontend Engineering", "description": "Progressive Vue 3 frontend framework."},
            {"name": "React", "category": "Frontend Engineering", "description": "React UI library."},
            {"name": "PostgreSQL", "category": "Databases & Storage", "description": "PostgreSQL RDBMS."},
            {"name": "Docker", "category": "DevOps & Cloud", "description": "Containerization platform."}
        ]
        for sk in initial_skills:
            db.add(Skill(name=sk["name"], category=sk["category"], description=sk["description"]))

        # 5. Seed Demo Collaboration Projects (Feature 31 & 32)
        demo_projects = [
            {
                "title": "AI Resume Analyzer",
                "description": "Build an AI-powered resume analysis application that parses PDF resumes and extracts candidate skill scores.",
                "category": "AI & Data Science",
                "technology_stack": "Python, FastAPI, Vue.js, PostgreSQL",
                "visibility": ProjectVisibility.PUBLIC,
                "maximum_members": 5,
                "status": ProjectStatus.OPEN
            },
            {
                "title": "Campus Placement Portal",
                "description": "An integrated student recruitment drive management system with schedule tracking and job applications.",
                "category": "Software Engineering",
                "technology_stack": "Vue.js, Node.js, PostgreSQL",
                "visibility": ProjectVisibility.PUBLIC,
                "maximum_members": 4,
                "status": ProjectStatus.IN_PROGRESS
            },
            {
                "title": "Smart Attendance System",
                "description": "Facial recognition-based automated attendance logging for university classrooms.",
                "category": "AI & Data Science",
                "technology_stack": "Python, OpenCV, SQLite",
                "visibility": ProjectVisibility.PUBLIC,
                "maximum_members": 3,
                "status": ProjectStatus.OPEN
            }
        ]

        for p_data in demo_projects:
            proj = Project(
                owner_id=student_user.id,
                **p_data
            )
            db.add(proj)
            db.flush()
            db.add(ProjectMember(
                project_id=proj.id,
                student_id=student_user.id,
                role=MemberRole.OWNER,
                status=MemberStatus.ACTIVE
            ))
            # Add sample tasks for Feature 33 progress calculation
            db.add(ProjectTask(
                project_id=proj.id,
                title="Design Database Schema & Models",
                description="Set up SQLAlchemy tables for project.",
                assigned_to=student_user.id,
                created_by=student_user.id,
                priority=TaskPriority.HIGH,
                status=TaskStatus.COMPLETED
            ))
            db.add(ProjectTask(
                project_id=proj.id,
                title="Implement REST API Endpoints",
                description="Build FastAPI routes.",
                assigned_to=student_user.id,
                created_by=student_user.id,
                priority=TaskPriority.MEDIUM,
                status=TaskStatus.IN_PROGRESS
            ))
            print(f"[OK] Seeded Project: {proj.title} [{proj.status.value}]")

        # 6. Seed Career Sandbox Challenges (Feature 35)
        demo_challenges = [
            {
                "title": "Build a REST API with FastAPI",
                "description": "Construct a high-performance RESTful API using FastAPI and Pydantic validation rules.",
                "category": "Software Engineering",
                "difficulty": SandboxDifficulty.BEGINNER,
                "skills": "Python, FastAPI, REST",
                "instructions": "1. Define a Pydantic model with fields (name, email, age).\n2. Implement POST /users and GET /users endpoints.\n3. Return valid JSON responses with 200/201 status codes.",
                "time_limit": 45,
                "status": SandboxStatus.PUBLISHED
            },
            {
                "title": "Create a Vue 3 Interactive Dashboard",
                "description": "Build a responsive Vue 3 component with state management using Pinia.",
                "category": "Frontend Engineering",
                "difficulty": SandboxDifficulty.INTERMEDIATE,
                "skills": "Vue.js, Pinia, JavaScript",
                "instructions": "1. Create a Pinia store to hold list state.\n2. Render interactive data cards with filtering.\n3. Handle loading and empty states cleanly.",
                "time_limit": 60,
                "status": SandboxStatus.PUBLISHED
            },
            {
                "title": "SQL Query Optimization Challenge",
                "description": "Optimize slow multi-join SQL queries on large relational tables.",
                "category": "Databases & Storage",
                "difficulty": SandboxDifficulty.INTERMEDIATE,
                "skills": "SQL, PostgreSQL, Indexing",
                "instructions": "1. Analyze EXPLAIN ANALYZE execution plan.\n2. Add composite indexes to resolve sequential scans.\n3. Rewrite subqueries into JOIN clauses.",
                "time_limit": 30,
                "status": SandboxStatus.PUBLISHED
            }
        ]

        for c_data in demo_challenges:
            ch = SandboxChallenge(
                created_by=admin_user.id,
                **c_data
            )
            db.add(ch)
            print(f"[OK] Seeded Sandbox Challenge: {ch.title} [{ch.difficulty.value}]")

        # 7. Seed Sample System Notifications
        demo_notifications = [
            {
                "user_id": admin_user.id,
                "title": "System Audit Complete",
                "message": "Platform verification queue status: 1 company pending review.",
                "is_read": False
            },
            {
                "user_id": student_user.id,
                "title": "Welcome to CareerPilot AI!",
                "message": "Start by exploring collaboration projects or taking a Career Sandbox challenge.",
                "is_read": False
            },
            {
                "user_id": recruiter_user.id,
                "title": "Company Profile Verified",
                "message": "CareerPilot Technologies has been officially verified by platform administrators.",
                "is_read": True
            }
        ]

        for n_data in demo_notifications:
            db.add(Notification(**n_data))
        print("[OK] Seeded Initial System Notifications")

        db.commit()
        print("\nDatabase Seed Completed Successfully!")
        print("--------------------------------------------------")
        print(f"Demo Admin Email       : {admin_email} (Password: AdminPass123!)")
        print(f"Demo Student Email     : {student_email} (Password: Password123!)")
        print(f"Demo Recruiter Email   : {demo_email} (Password: Password123!)")
        print("--------------------------------------------------")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
