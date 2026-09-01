import pytest
from datetime import date, timedelta
from app.models.company import VerificationStatus
from app.models.company import Company

def test_cross_company_ownership_protection(client, db_session):
    # Recruiter A (Company Alpha)
    reg_a = client.post("/api/auth/recruiter/register", json={
        "full_name": "Recruiter A",
        "email": "recruiterA@alpha.com",
        "password": "Password123!",
        "company_name": "Company Alpha"
    }).json()
    headers_a = {"Authorization": f"Bearer {reg_a['data']['access_token']}"}

    # Recruiter B (Company Beta)
    reg_b = client.post("/api/auth/recruiter/register", json={
        "full_name": "Recruiter B",
        "email": "recruiterB@beta.com",
        "password": "Password123!",
        "company_name": "Company Beta"
    }).json()
    headers_b = {"Authorization": f"Bearer {reg_b['data']['access_token']}"}

    # Recruiter A creates a job
    job_res = client.post("/api/recruiter/jobs", json={
        "title": "Alpha Confidential Job",
        "description": "Exclusive job for Company Alpha.",
        "location": "Bengaluru",
        "application_deadline": str(date.today() + timedelta(days=20))
    }, headers=headers_a).json()
    job_id = job_res["data"]["id"]

    # Recruiter B attempts to view Recruiter A's job -> 403 Forbidden
    res_b_view = client.get(f"/api/recruiter/jobs/{job_id}", headers=headers_b)
    assert res_b_view.status_code == 403

    # Recruiter B attempts to edit Recruiter A's job -> 403 Forbidden
    res_b_edit = client.put(f"/api/recruiter/jobs/{job_id}", json={"title": "Hacked Title"}, headers=headers_b)
    assert res_b_edit.status_code == 403

    # Recruiter B attempts to delete Recruiter A's job -> 403 Forbidden
    res_b_del = client.delete(f"/api/recruiter/jobs/{job_id}", headers=headers_b)
    assert res_b_del.status_code == 403

def test_unverified_company_cannot_publish_job(client, db_session):
    # Recruiter registering creates PENDING company by default
    reg = client.post("/api/auth/recruiter/register", json={
        "full_name": "Pending Recruiter",
        "email": "pending@unverified.com",
        "password": "Password123!",
        "company_name": "Unverified Startup"
    }).json()
    headers = {"Authorization": f"Bearer {reg['data']['access_token']}"}
    company_id = reg["data"]["company_id"]

    # Create job draft
    job_res = client.post("/api/recruiter/jobs", json={
        "title": "Draft Job by Unverified Company",
        "description": "This job cannot be published until verified.",
        "location": "Delhi",
        "application_deadline": str(date.today() + timedelta(days=15))
    }, headers=headers).json()
    job_id = job_res["data"]["id"]

    # Attempt to publish -> 400 Bad Request
    pub_res = client.patch(f"/api/recruiter/jobs/{job_id}/publish", headers=headers)
    assert pub_res.status_code == 400
    assert "Your company must be verified before publishing jobs" in pub_res.json()["detail"]

    # Manually verify company in db fixture to simulate Admin Approval
    company = db_session.query(Company).filter(Company.id == company_id).first()
    company.verification_status = VerificationStatus.VERIFIED
    db_session.commit()

    # Now publishing succeeds -> 200 OK
    pub_ok = client.patch(f"/api/recruiter/jobs/{job_id}/publish", headers=headers)
    assert pub_ok.status_code == 200
    assert pub_ok.json()["data"]["status"] == "PUBLISHED"
