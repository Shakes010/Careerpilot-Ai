import pytest
from app.models.user import User, UserRole
from app.core.security import get_password_hash, create_access_token
from app.models.sandbox import SandboxChallenge, SandboxDifficulty, SandboxStatus

@pytest.fixture
def student_one(db_session):
    u = User(
        email="student1@careerpilot.ai",
        password_hash=get_password_hash("Password123!"),
        full_name="Student Owner",
        role=UserRole.STUDENT
    )
    db_session.add(u)
    db_session.commit()
    return u

@pytest.fixture
def student_two(db_session):
    u = User(
        email="student2@careerpilot.ai",
        password_hash=get_password_hash("Password123!"),
        full_name="Student Applicant",
        role=UserRole.STUDENT
    )
    db_session.add(u)
    db_session.commit()
    return u

@pytest.fixture
def demo_sandbox_challenge(db_session, student_one):
    ch = SandboxChallenge(
        title="REST API Test Challenge",
        description="Build a REST API challenge for testing.",
        category="Software Engineering",
        difficulty=SandboxDifficulty.BEGINNER,
        skills="Python, FastAPI",
        instructions="Implement user endpoints.",
        time_limit=45,
        status=SandboxStatus.PUBLISHED,
        created_by=student_one.id
    )
    db_session.add(ch)
    db_session.commit()
    return ch

def get_user_headers(user):
    token = create_access_token(data={"sub": user.id, "role": user.role.value})
    return {"Authorization": f"Bearer {token}"}

# --- FEATURE 31 & 32 TESTS ---
def test_create_and_join_project_flow(client, student_one, student_two):
    headers1 = get_user_headers(student_one)
    headers2 = get_user_headers(student_two)

    # 1. Student One Creates Project
    create_res = client.post("/api/projects", json={
        "title": "AI Resume Analyzer",
        "description": "Build an AI-powered resume analysis app.",
        "category": "AI & Data Science",
        "technology_stack": "Python, FastAPI, Vue",
        "visibility": "PUBLIC",
        "maximum_members": 2
    }, headers=headers1)
    assert create_res.status_code == 201
    proj_id = create_res.json()["data"]["id"]

    # 2. Student Two Requests to Join
    join_res = client.post(f"/api/projects/{proj_id}/join", headers=headers2)
    assert join_res.status_code == 200
    req_id = join_res.json()["data"]["id"]

    # 3. Duplicate Join Request Prevention
    dup_res = client.post(f"/api/projects/{proj_id}/join", headers=headers2)
    assert dup_res.status_code == 400

    # 4. Student One Accepts Join Request
    accept_res = client.post(f"/api/projects/{proj_id}/join-requests/{req_id}/accept", headers=headers1)
    assert accept_res.status_code == 200
    assert accept_res.json()["data"]["student_id"] == student_two.id

# --- FEATURE 32 TASK ASSIGNMENT TESTS ---
def test_task_assignment_and_member_validation(client, student_one, student_two):
    headers1 = get_user_headers(student_one)

    # Create Project
    proj = client.post("/api/projects", json={
        "title": "Smart Attendance System",
        "description": "Facial recognition attendance system.",
        "category": "Software Engineering",
        "technology_stack": "Python, OpenCV",
        "maximum_members": 3
    }, headers=headers1).json()["data"]
    proj_id = proj["id"]

    # 1. Invalid Non-Member Assignment Rejected
    bad_task = client.post(f"/api/projects/{proj_id}/tasks", json={
        "title": "Build Frontend",
        "assigned_to": student_two.id,
        "priority": "HIGH"
    }, headers=headers1)
    assert bad_task.status_code == 400

    # 2. Valid Task Assigned to Owner
    good_task = client.post(f"/api/projects/{proj_id}/tasks", json={
        "title": "Design Database Schema",
        "assigned_to": student_one.id,
        "priority": "HIGH"
    }, headers=headers1)
    assert good_task.status_code == 201
    task_id = good_task.json()["data"]["id"]

    # 3. Update Task Status -> COMPLETED
    update_task = client.patch(f"/api/projects/{proj_id}/tasks/{task_id}/status?status=COMPLETED", headers=headers1)
    assert update_task.status_code == 200
    assert update_task.json()["data"]["status"] == "COMPLETED"

# --- FEATURE 33 PROGRESS TRACKING TESTS ---
def test_project_progress_calculation(client, student_one):
    headers1 = get_user_headers(student_one)
    proj_id = client.post("/api/projects", json={
        "title": "Campus Placement Portal",
        "description": "Student placement portal system.",
        "category": "Software Engineering"
    }, headers=headers1).json()["data"]["id"]

    # Add 2 Tasks (1 TODO, 1 COMPLETED)
    t1 = client.post(f"/api/projects/{proj_id}/tasks", json={"title": "Task 1", "assigned_to": student_one.id}, headers=headers1).json()["data"]["id"]
    t2 = client.post(f"/api/projects/{proj_id}/tasks", json={"title": "Task 2", "assigned_to": student_one.id}, headers=headers1).json()["data"]["id"]
    client.patch(f"/api/projects/{proj_id}/tasks/{t1}/status?status=COMPLETED", headers=headers1)

    progress_res = client.get(f"/api/projects/{proj_id}/progress")
    assert progress_res.status_code == 200
    p_data = progress_res.json()["data"]
    assert p_data["total_tasks"] == 2
    assert p_data["completed_tasks"] == 1
    assert p_data["progress_percentage"] == 50.0

# --- FEATURE 34 COMPLETION VERIFICATION TESTS ---
def test_project_completion_verification(client, student_one, student_two):
    headers1 = get_user_headers(student_one)
    headers2 = get_user_headers(student_two)

    proj_id = client.post("/api/projects", json={
        "title": "E-Commerce App",
        "description": "Online shopping application.",
        "category": "Software Engineering"
    }, headers=headers1).json()["data"]["id"]

    # Student Two (Non-Owner) Attempting Verification Rejected
    bad_ver = client.post(f"/api/projects/{proj_id}/verification", json={"verification_notes": "Fake approval"}, headers=headers2)
    assert bad_ver.status_code == 403

    # Student One (Owner) Submits Verification
    ver_res = client.post(f"/api/projects/{proj_id}/verification", json={"verification_notes": "Completed and tested."}, headers=headers1)
    assert ver_res.status_code == 200
    assert ver_res.json()["data"]["status"] == "PENDING"

    # Check Status
    status_res = client.get(f"/api/projects/{proj_id}/verification")
    assert status_res.status_code == 200
    assert status_res.json()["data"]["status"] == "PENDING"

# --- FEATURE 35 CAREER SANDBOX TESTS ---
def test_career_sandbox_attempt_and_submission(client, student_one, demo_sandbox_challenge):
    headers1 = get_user_headers(student_one)

    # 1. List Sandbox Challenges
    challenges_res = client.get("/api/career-sandbox/challenges")
    assert challenges_res.status_code == 200

    ch_id = demo_sandbox_challenge.id

    # 2. Start Attempt
    start_res = client.post(f"/api/career-sandbox/challenges/{ch_id}/start", headers=headers1)
    assert start_res.status_code == 200
    attempt_id = start_res.json()["data"]["id"]

    # 3. Submit Solution
    sub_res = client.post(f"/api/career-sandbox/attempts/{attempt_id}/submit", json={
        "submission": "def user_api(): return {'status': 'success'}"
    }, headers=headers1)
    assert sub_res.status_code == 200
    assert sub_res.json()["data"]["status"] == "SUBMITTED"
