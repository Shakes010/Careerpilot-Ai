import pytest
from app.models.user import User, UserRole
from app.models.admin import FlaggedActivity, FlagTargetType, FlagStatus
from app.core.security import get_password_hash, create_access_token

@pytest.fixture
def admin_user(db_session):
    u = User(
        email="admin@careerpilot.ai",
        password_hash=get_password_hash("AdminPass123!"),
        full_name="System Admin",
        role=UserRole.ADMIN
    )
    db_session.add(u)
    db_session.commit()
    return u

@pytest.fixture
def target_user(db_session):
    u = User(
        email="target@careerpilot.ai",
        password_hash=get_password_hash("Password123!"),
        full_name="Target Student",
        role=UserRole.STUDENT
    )
    db_session.add(u)
    db_session.commit()
    return u

@pytest.fixture
def demo_flagged_report(db_session, target_user):
    flag = FlaggedActivity(
        target_type=FlagTargetType.USER,
        target_id=target_user.id,
        reason="Suspicious spam activity reported.",
        risk_score=85.0,
        status=FlagStatus.PENDING
    )
    db_session.add(flag)
    db_session.commit()
    return flag

def get_admin_headers(admin_user):
    token = create_access_token(data={"sub": admin_user.id, "role": admin_user.role.value})
    return {"Authorization": f"Bearer {token}"}

# --- FEATURE 36: USER MANAGEMENT TESTS ---
def test_user_management_list_and_status_update(client, admin_user, target_user):
    headers = get_admin_headers(admin_user)

    # 1. List Users
    list_res = client.get("/api/admin/users?role=STUDENT", headers=headers)
    assert list_res.status_code == 200
    assert list_res.json()["data"]["pagination"]["total"] >= 1

    # 2. Suspend User
    suspend_res = client.patch(f"/api/admin/users/{target_user.id}/status", json={
        "is_active": False,
        "notes": "Suspended for policy violation."
    }, headers=headers)
    assert suspend_res.status_code == 200
    assert suspend_res.json()["data"]["is_active"] is False

    # 3. Re-activate User
    activate_res = client.patch(f"/api/admin/users/{target_user.id}/status", json={
        "is_active": True,
        "notes": "Account verified and restored."
    }, headers=headers)
    assert activate_res.status_code == 200
    assert activate_res.json()["data"]["is_active"] is True

# --- FEATURE 40: ANALYTICS TELEMETRY TESTS ---
def test_analytics_overview_telemetry(client, admin_user):
    headers = get_admin_headers(admin_user)
    res = client.get("/api/admin/analytics/overview", headers=headers)
    assert res.status_code == 200
    data = res.json()["data"]
    assert "active_students" in data
    assert "active_recruiters" in data
    assert "total_jobs" in data
    assert "verified_companies" in data

# --- FEATURE 41: FLAGGED QUEUE TESTS ---
def test_flagged_queue_resolution(client, admin_user, demo_flagged_report):
    headers = get_admin_headers(admin_user)

    # 1. List Flagged Activities
    queue_res = client.get("/api/admin/flagged-queue", headers=headers)
    assert queue_res.status_code == 200
    assert queue_res.json()["data"]["pagination"]["total"] >= 1

    # 2. Resolve Flagged Report -> WARNING_ISSUED
    resolve_res = client.patch(f"/api/admin/flagged-queue/{demo_flagged_report.id}/resolve", json={
        "status": "WARNING_ISSUED",
        "resolution_notes": "Official warning sent to user."
    }, headers=headers)
    assert resolve_res.status_code == 200
    assert resolve_res.json()["data"]["status"] == "WARNING_ISSUED"
