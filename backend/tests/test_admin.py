import pytest
from app.models.user import User, UserRole
from app.core.security import get_password_hash

@pytest.fixture
def admin_user(db_session):
    user = User(
        email="admin@careerpilot.ai",
        password_hash=get_password_hash("AdminPass123!"),
        full_name="System Admin",
        role=UserRole.ADMIN
    )
    db_session.add(user)
    db_session.commit()
    return user

def test_admin_login_and_metrics(client, admin_user):
    res = client.post("/api/admin/auth/login", json={
        "email": "admin@careerpilot.ai",
        "password": "AdminPass123!"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    token = data["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch Metrics
    metrics_res = client.get("/api/admin/dashboard", headers=headers)
    assert metrics_res.status_code == 200
    assert "pending_verifications" in metrics_res.json()["data"]

def test_recruiter_verification_workflow(client, admin_user):
    # 1. Register Recruiter -> Company PENDING
    reg = client.post("/api/auth/recruiter/register", json={
        "full_name": "Applicant Recruiter",
        "email": "applicant@startup.io",
        "password": "Password123!",
        "company_name": "Startup IO"
    }).json()
    company_id = reg["data"]["company_id"]

    # 2. Login Admin
    admin_login = client.post("/api/admin/auth/login", json={
        "email": "admin@careerpilot.ai",
        "password": "AdminPass123!"
    }).json()
    admin_headers = {"Authorization": f"Bearer {admin_login['data']['access_token']}"}

    # 3. Get Pending Queue
    queue_res = client.get("/api/admin/companies/pending", headers=admin_headers)
    assert queue_res.status_code == 200

    # 4. Admin Approves Verification
    verify_res = client.patch(f"/api/admin/companies/{company_id}/verify", json={
        "verification_notes": "Official startup documents verified."
    }, headers=admin_headers)
    assert verify_res.status_code == 200
    assert verify_res.json()["data"]["verification_status"] == "VERIFIED"

def test_skill_library_crud(client, admin_user):
    admin_login = client.post("/api/admin/auth/login", json={
        "email": "admin@careerpilot.ai",
        "password": "AdminPass123!"
    }).json()
    headers = {"Authorization": f"Bearer {admin_login['data']['access_token']}"}

    # Create Skill
    create_res = client.post("/api/admin/skills", json={
        "name": "GraphQL",
        "category": "Backend Engineering",
        "description": "API query language."
    }, headers=headers)
    assert create_res.status_code == 201
    skill_id = create_res.json()["data"]["id"]

    # List Skills
    list_res = client.get("/api/admin/skills?search=GraphQL")
    assert list_res.status_code == 200
    assert list_res.json()["data"]["pagination"]["total"] >= 1

    # Delete Skill
    del_res = client.delete(f"/api/admin/skills/{skill_id}", headers=headers)
    assert del_res.status_code == 200
