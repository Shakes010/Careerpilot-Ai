from sqlalchemy.orm import Session
from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.models.student import (
    User, 
    StudentProfile, 
    StudentEducation, 
    StudentSkill, 
    StudentResume, 
    StudentCareerPreference, 
    Job, 
    JobApplication, 
    LearningResource
)
from app.core.security import get_password_hash

def init_db(db: Session) -> None:
    # Create all database tables
    Base.metadata.create_all(bind=engine)

    # 1. Seed catalog jobs if table is empty
    if db.query(Job).count() == 0:
        jobs = [
            Job(
                title="Full Stack Software Engineer",
                company="TechPulse Systems",
                industry="Software Development",
                location="San Francisco, CA (Hybrid)",
                type="Job",
                required_skills="Python, FastAPI, Vue.js, PostgreSQL, Git",
                min_education="Bachelor's or Master's in CS/MCA",
                description="Join TechPulse to build next-generation scalable web applications using Python FastAPI microservices and modern Vue 3 web interfaces.",
                salary_range="$95,000 - $130,000 / year",
                deadline="Sep 25, 2026"
            ),
            Job(
                title="AI / ML Engineer Intern",
                company="DeepMind Solutions",
                industry="Artificial Intelligence",
                location="Remote",
                type="Internship",
                required_skills="Python, PyTorch, Machine Learning, Data Science, NLP",
                min_education="Currently enrolled in CS/MCA degree",
                description="Develop cutting-edge machine learning and natural language processing models alongside world-class AI researchers.",
                salary_range="$50 / hour",
                deadline="Oct 10, 2026"
            ),
            Job(
                title="Backend Developer (Python / Cloud)",
                company="CloudScale Networks",
                industry="Cloud Computing",
                location="Seattle, WA",
                type="Job",
                required_skills="Python, FastAPI, Docker, AWS, PostgreSQL, Redis",
                min_education="Bachelor's / Master's Degree",
                description="Optimize microservices architecture and cloud backend deployment pipelines on AWS infrastructure.",
                salary_range="$105,000 - $140,000 / year",
                deadline="Sep 30, 2026"
            ),
            Job(
                title="Frontend Developer (Vue.js & Modern CSS)",
                company="PixelCraft Studios",
                industry="Digital Media",
                location="Austin, TX (Remote)",
                type="Job",
                required_skills="Vue.js, JavaScript, HTML5, CSS, TailwindCSS",
                min_education="Bachelor's Degree",
                description="Craft pixel-perfect, highly responsive user experiences for millions of active monthly users.",
                salary_range="$85,000 - $115,000 / year",
                deadline="Oct 15, 2026"
            ),
            Job(
                title="Global AI & Cloud Hackathon 2026",
                company="AWS & DevPost",
                industry="AI & Cloud Innovation",
                location="Online",
                type="Hackathon",
                required_skills="Python, FastAPI, Vue.js, Cloud, Generative AI",
                min_education="Open to all students",
                description="Build innovative generative AI solutions competing for $50,000 in total prizes and recruiter interviews.",
                salary_range="Prize Pool: $50,000",
                deadline="Nov 01, 2026"
            )
        ]
        db.add_all(jobs)
        db.commit()

    # 2. Seed learning resources if table is empty
    if db.query(LearningResource).count() == 0:
        resources = [
            LearningResource(
                skill_name="FastAPI",
                topic="Backend Web Frameworks",
                title="FastAPI Masterclass: High-Performance Python APIs",
                provider="CareerPilot AI Academy",
                url="https://fastapi.tiangolo.com/tutorial/",
                difficulty="Intermediate"
            ),
            LearningResource(
                skill_name="Vue.js",
                topic="Frontend Frameworks",
                title="Vue 3 & Pinia Architecture Guide",
                provider="Vue School",
                url="https://vuejs.org/guide/introduction.html",
                difficulty="Intermediate"
            ),
            LearningResource(
                skill_name="PostgreSQL",
                topic="Database Systems",
                title="Relational Database Design & Indexing",
                provider="PostgreSQL Docs",
                url="https://www.postgresql.org/docs/",
                difficulty="Advanced"
            ),
            LearningResource(
                skill_name="Docker",
                topic="DevOps & Containers",
                title="Docker Containerization for Full-Stack Apps",
                provider="Docker Education",
                url="https://docs.docker.com/get-started/",
                difficulty="Intermediate"
            ),
            LearningResource(
                skill_name="Machine Learning",
                topic="Artificial Intelligence",
                title="Applied Machine Learning with Scikit-Learn & Python",
                provider="Coursera",
                url="https://scikit-learn.org/stable/tutorial/index.html",
                difficulty="Intermediate"
            )
        ]
        db.add_all(resources)
        db.commit()

    # 3. Seed demo student user
    demo_user = db.query(User).filter(User.email == "student@careerpilot.ai").first()
    if not demo_user:
        demo_user = User(
            email="student@careerpilot.ai",
            hashed_password=get_password_hash("password123"),
            full_name="Alex Morgan",
            role="student",
            is_active=True
        )
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)

        # Profile
        demo_profile = StudentProfile(
            user_id=demo_user.id,
            headline="Computer Science Student & Aspiring Full-Stack Engineer",
            phone="+1 (555) 234-5678",
            location="San Francisco, CA",
            linkedin_url="https://linkedin.com/in/alexmorgan",
            github_url="https://github.com/alexmorgan",
            website="https://alexmorgan.dev",
            university="National Institute of Technology",
            major="Master of Computer Applications (MCA)",
            graduation_year=2026,
            bio="Passionate about AI, full-stack web applications, and high-performance microservices. Building industry-ready projects with CareerPilot AI.",
            profile_picture="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=300",
            career_readiness_score=88,
            applications_sent=3,
            active_opportunities=5,
            assessments_completed=8,
            verified_skills_count=5,
            skill_trust_meter=92.0
        )
        db.add(demo_profile)

        # Education
        edu1 = StudentEducation(
            student_id=demo_user.id,
            degree="Master of Computer Applications (MCA)",
            institution="National Institute of Technology",
            start_year=2024,
            end_year=2026,
            grade="3.9 / 4.0 GPA",
            details="Specialization in Software Engineering, Cloud Computing, and Artificial Intelligence."
        )
        edu2 = StudentEducation(
            student_id=demo_user.id,
            degree="Bachelor of Science in Computer Science (B.Sc CS)",
            institution="State University of Technology",
            start_year=2021,
            end_year=2024,
            grade="3.8 / 4.0 GPA",
            details="Graduated with High Honors. Led the University Computer Science Student Association."
        )
        db.add_all([edu1, edu2])

        # Skills
        skills = [
            StudentSkill(student_id=demo_user.id, skill_name="Python", category="Programming Languages", proficiency="Advanced", is_verified=True),
            StudentSkill(student_id=demo_user.id, skill_name="FastAPI", category="Web Development", proficiency="Advanced", is_verified=True),
            StudentSkill(student_id=demo_user.id, skill_name="Vue.js", category="Web Development", proficiency="Intermediate", is_verified=True),
            StudentSkill(student_id=demo_user.id, skill_name="JavaScript", category="Programming Languages", proficiency="Intermediate", is_verified=True),
            StudentSkill(student_id=demo_user.id, skill_name="Git", category="Cloud & DevOps", proficiency="Advanced", is_verified=True)
        ]
        db.add_all(skills)

        # Resume
        resume = StudentResume(
            student_id=demo_user.id,
            filename="Alex_Morgan_Software_Engineer_Resume.pdf",
            file_path="/uploads/resumes/alex_morgan_resume.pdf",
            file_type="application/pdf",
            file_size=245000,
            summary="Experienced MCA student with background in Python, FastAPI, Vue.js, and database engineering. Built full-stack web applications.",
            ats_score=88
        )
        db.add(resume)

        # Career Preference
        pref = StudentCareerPreference(
            student_id=demo_user.id,
            preferred_role="Full Stack Software Engineer",
            preferred_industry="Software & Cloud Tech",
            preferred_location="San Francisco, CA / Remote",
            employment_type="Full-Time",
            work_mode="Hybrid",
            expected_salary="$95,000 - $130,000 / year"
        )
        db.add(pref)

        db.commit()

        # Job Applications
        first_job = db.query(Job).first()
        if first_job:
            app1 = JobApplication(
                student_id=demo_user.id,
                job_id=first_job.id,
                status="Under Review",
                notes="Submitted resume & portfolio GitHub link."
            )
            db.add(app1)
            db.commit()

if __name__ == "__main__":
    db = SessionLocal()
    init_db(db)
    print("Database initialized & seeded successfully!")

