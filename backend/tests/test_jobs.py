import pytest
from datetime import date, timedelta

def test_job_crud_and_lifecycle(client):
    reg = client.post("/api/auth/recruiter/register", json={
        "full_name": "Job Manager",
        "email": "hiring@innovate.com",
        "password": "Password123!",
        "company_name": "Innovate AI"
    }).json()
    token = reg["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create Job as Draft
    create_payload = {
        "title": "Backend Python Engineer",
        "description": "Looking for FastAPI and PostgreSQL backend developers.",
        "employment_type": "FULL_TIME",
        "location": "Remote",
        "work_mode": "REMOTE",
        "experience_min": 1,
        "experience_max": 3,
        "salary_min": 800000,
        "salary_max": 1200000,
        "number_of_openings": 2,
        "application_deadline": str(date.today() + timedelta(days=30)),
        "skills": ["Python", "FastAPI", "SQLAlchemy"]
    }
    res = client.post("/api/recruiter/jobs", json=create_payload, headers=headers)
    assert res.status_code == 201
    job_data = res.json()["data"]
    job_id = job_data["id"]
    assert job_data["status"] == "DRAFT"
    assert len(job_data["skills"]) == 3

    # 2. Get Job Details
    res_get = client.get(f"/api/recruiter/jobs/{job_id}", headers=headers)
    assert res_get.status_code == 200
    assert res_get.json()["data"]["title"] == "Backend Python Engineer"

    # 3. Edit Draft Job
    res_edit = client.put(f"/api/recruiter/jobs/{job_id}", json={
        "title": "Senior Backend Python Engineer",
        "salary_max": 1500000
    }, headers=headers)
    assert res_edit.status_code == 200
    assert res_edit.json()["data"]["title"] == "Senior Backend Python Engineer"

    # 4. Search and Filter Jobs
    res_list = client.get("/api/recruiter/jobs?search=Python&status=DRAFT", headers=headers)
    assert res_list.status_code == 200
    assert res_list.json()["data"]["pagination"]["total"] == 1

    # 5. Delete Draft Job
    res_del = client.delete(f"/api/recruiter/jobs/{job_id}", headers=headers)
    assert res_del.status_code == 200
    assert res_del.json()["success"] is True

def test_job_validation_rules(client):
    reg = client.post("/api/auth/recruiter/register", json={
        "full_name": "Validator",
        "email": "val@check.com",
        "password": "Password123!",
        "company_name": "Check Corp"
    }).json()
    headers = {"Authorization": f"Bearer {reg['data']['access_token']}"}

    # Invalid experience range (min > max)
    invalid_exp = {
        "title": "Invalid Exp Job",
        "description": "Valid job description content goes here.",
        "location": "Bengaluru",
        "experience_min": 5,
        "experience_max": 2,
        "application_deadline": str(date.today() + timedelta(days=10))
    }
    res = client.post("/api/recruiter/jobs", json=invalid_exp, headers=headers)
    assert res.status_code == 422
