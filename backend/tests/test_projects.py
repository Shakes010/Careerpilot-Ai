import pytest

def test_project_creation_and_task_assignment(client):
    # Register Recruiter User
    reg = client.post("/api/auth/recruiter/register", json={
        "full_name": "Project Lead",
        "email": "lead@collab.com",
        "password": "Password123!",
        "company_name": "Collab Labs"
    }).json()
    token = reg["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create Project
    proj_res = client.post("/api/projects", json={
        "title": "Open AI Career Assistant",
        "description": "Building an AI-driven resume reviewer tool.",
        "category": "AI & Data Science",
        "technology_stack": "Python, FastAPI, Vue.js",
        "maximum_members": 5
    }, headers=headers)
    assert proj_res.status_code == 201
    proj_id = proj_res.json()["data"]["id"]

    # 2. Get Details
    get_res = client.get(f"/api/projects/{proj_id}")
    assert get_res.status_code == 200
    assert get_res.json()["data"]["title"] == "Open AI Career Assistant"

    # 3. Create Task
    user_id = reg["data"]["user_id"]
    task_res = client.post(f"/api/projects/{proj_id}/tasks", json={
        "title": "Setup FastAPI Backend Skeleton",
        "description": "Initialize database connection and user router.",
        "assigned_to": user_id,
        "priority": "HIGH"
    }, headers=headers)
    assert task_res.status_code == 201
    task_id = task_res.json()["data"]["id"]

    # 4. Update Task Status
    up_res = client.patch(f"/api/projects/{proj_id}/tasks/{task_id}/status?status=IN_PROGRESS", headers=headers)
    assert up_res.status_code == 200
    assert up_res.json()["data"]["status"] == "IN_PROGRESS"
