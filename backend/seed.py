import os
import sys
from datetime import date, timedelta, datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.company import Company, VerificationStatus
from app.models.recruiter import Recruiter
from app.models.job import Job, JobSkill, EmploymentType, WorkMode, JobStatus

def seed_data():
    print("=== Initializing CareerPilot AI Database Seed ===")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Create or get Demo Recruiter User
        demo_email = "sensha@careerpilot.ai"
        user = db.query(User).filter(User.email == demo_email).first()
        if not user:
            user = User(
                email=demo_email,
                password_hash=get_password_hash("Password123!"),
                full_name="Sensha",
                phone="+91 98765 43210",
                role=UserRole.RECRUITER,
                is_active=True
            )
            db.add(user)
            db.flush()
            print(f"[OK] Created User: {user.full_name} ({user.email})")

        # 2. Create or get Demo Company (VERIFIED)
        company = db.query(Company).filter(Company.name == "CareerPilot Technologies").first()
        if not company:
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
                verification_status=VerificationStatus.VERIFIED,
                verification_notes="Verified official MCA final year showcase account."
            )
            db.add(company)
            db.flush()
            print(f"[OK] Created Company: {company.name} [VERIFIED]")

        # 3. Create or get Recruiter Profile
        recruiter = db.query(Recruiter).filter(Recruiter.user_id == user.id).first()
        if not recruiter:
            recruiter = Recruiter(
                user_id=user.id,
                company_id=company.id,
                designation="Senior Talent Acquisition Lead"
            )
            db.add(recruiter)
            db.flush()
            print("[OK] Linked Recruiter Profile")

        # 4. Create Sample Jobs if company has no jobs
        existing_jobs_count = db.query(Job).filter(Job.company_id == company.id).count()
        if existing_jobs_count == 0:
            sample_jobs = [
                {
                    "title": "Software Developer Intern",
                    "description": "We are seeking a motivated Software Developer Intern passionate about Python, FastAPI, and modern web application development. You will work on real-world AI features and high-throughput REST APIs.",
                    "employment_type": EmploymentType.INTERNSHIP,
                    "location": "Bengaluru, India",
                    "work_mode": WorkMode.REMOTE,
                    "experience_min": 0,
                    "experience_max": 1,
                    "salary_min": 25000,
                    "salary_max": 40000,
                    "salary_currency": "INR",
                    "education_requirements": "B.Tech / MCA / BE in Computer Science or related field",
                    "job_category": "Software Engineering",
                    "number_of_openings": 3,
                    "application_deadline": date.today() + timedelta(days=45),
                    "status": JobStatus.PUBLISHED,
                    "skills": ["Python", "FastAPI", "React", "PostgreSQL", "Git"]
                },
                {
                    "title": "Frontend Developer (Vue.js)",
                    "description": "Join our frontend engineering team to craft high-performance interactive user interfaces using Vue 3, Pinia, and Tailwind CSS. Attention to detail and responsive design expertise required.",
                    "employment_type": EmploymentType.FULL_TIME,
                    "location": "Bengaluru, India",
                    "work_mode": WorkMode.HYBRID,
                    "experience_min": 1,
                    "experience_max": 3,
                    "salary_min": 600000,
                    "salary_max": 1000000,
                    "salary_currency": "INR",
                    "education_requirements": "Bachelor's degree in Computer Science or equivalent experience",
                    "job_category": "Frontend Engineering",
                    "number_of_openings": 2,
                    "application_deadline": date.today() + timedelta(days=30),
                    "status": JobStatus.PUBLISHED,
                    "skills": ["Vue", "JavaScript", "HTML5", "CSS3", "Pinia", "Axios"]
                },
                {
                    "title": "Python Backend Developer",
                    "description": "Looking for an experienced Python Backend Engineer to build robust RESTful microservices, optimize PostgreSQL queries, and manage JWT authentication workflows.",
                    "employment_type": EmploymentType.FULL_TIME,
                    "location": "Remote",
                    "work_mode": WorkMode.REMOTE,
                    "experience_min": 2,
                    "experience_max": 5,
                    "salary_min": 1000000,
                    "salary_max": 1800000,
                    "salary_currency": "INR",
                    "education_requirements": "B.Tech / MCA",
                    "job_category": "Backend Engineering",
                    "number_of_openings": 4,
                    "application_deadline": date.today() + timedelta(days=60),
                    "status": JobStatus.DRAFT,
                    "skills": ["Python", "FastAPI", "Django", "PostgreSQL", "Docker", "AWS"]
                },
                {
                    "title": "Data Analyst Intern",
                    "description": "Analyze candidate verification metrics, trust scores, and platform usage statistics. Strong skills in SQL, Python data libraries, and visualization tools expected.",
                    "employment_type": EmploymentType.INTERNSHIP,
                    "location": "Bengaluru, India",
                    "work_mode": WorkMode.ONSITE,
                    "experience_min": 0,
                    "experience_max": 1,
                    "salary_min": 20000,
                    "salary_max": 30000,
                    "salary_currency": "INR",
                    "education_requirements": "B.Sc / B.Tech / MCA in Analytics, Math, or CS",
                    "job_category": "Data Science",
                    "number_of_openings": 1,
                    "application_deadline": date.today() + timedelta(days=15),
                    "status": JobStatus.PAUSED,
                    "skills": ["Python", "SQL", "Pandas", "Tableau", "Excel"]
                }
            ]

            for j_data in sample_jobs:
                skills_list = j_data.pop("skills")
                job_obj = Job(
                    company_id=company.id,
                    created_by=recruiter.id,
                    **j_data
                )
                db.add(job_obj)
                db.flush()
                for s_name in skills_list:
                    db.add(JobSkill(job_id=job_obj.id, skill_name=s_name))
                print(f"[OK] Seeded Job: {job_obj.title} [{job_obj.status.value}]")

        db.commit()
        print("\nDatabase Seed Completed Successfully!")
        print("--------------------------------------------------")
        print(f"Demo Recruiter Email   : {demo_email}")
        print(f"Demo Recruiter Password: Password123!")
        print(f"Demo Company           : CareerPilot Technologies [VERIFIED]")
        print("--------------------------------------------------")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
