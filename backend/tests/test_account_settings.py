import pytest
from app.models.user import User, UserRole
from app.core.security import get_password_hash, create_access_token

@pytest.fixture
def sample_user(db_session):
    u = User(
        email="testuser@careerpilot.ai",
        password_hash=get_password_hash("Password123!"),
        full_name="Test Account User",
        role=UserRole.STUDENT
    )
    db_session.add(u)
    db_session.commit()
    return u

@pytest.fixture
def existing_user(db_session):
    u = User(
        email="existing@careerpilot.ai",
        password_hash=get_password_hash("Password123!"),
        full_name="Existing User",
        role=UserRole.RECRUITER
    )
    db_session.add(u)
    db_session.commit()
    return u

def get_user_headers(user):
    token = create_access_token(data={"sub": user.id, "role": user.role.value})
    return {"Authorization": f"Bearer {token}"}

# --- CHANGE PASSWORD TESTS ---
def test_change_password_success(client, sample_user):
    headers = get_user_headers(sample_user)

    # 1. Change password with correct current password
    res = client.put("/api/auth/change-password", json={
        "current_password": "Password123!",
        "new_password": "NewSecurePassword456!"
    }, headers=headers)
    assert res.status_code == 200
    assert res.json()["success"] is True

    # 2. Login with new password
    login_res = client.post("/api/auth/login", json={
        "email": sample_user.email,
        "password": "NewSecurePassword456!"
    })
    assert login_res.status_code == 200

def test_change_password_invalid_current_password(client, sample_user):
    headers = get_user_headers(sample_user)

    res = client.put("/api/auth/change-password", json={
        "current_password": "WrongPassword!",
        "new_password": "NewPassword123!"
    }, headers=headers)
    assert res.status_code == 400
    assert "Current password is incorrect" in res.json()["detail"]

# --- CHANGE EMAIL TESTS ---
def test_change_email_success(client, sample_user):
    headers = get_user_headers(sample_user)

    res = client.put("/api/auth/change-email", json={
        "new_email": "updated.email@careerpilot.ai",
        "password": "Password123!"
    }, headers=headers)
    assert res.status_code == 200
    assert res.json()["data"]["email"] == "updated.email@careerpilot.ai"

def test_change_email_duplicate_rejection(client, sample_user, existing_user):
    headers = get_user_headers(sample_user)

    res = client.put("/api/auth/change-email", json={
        "new_email": existing_user.email,
        "password": "Password123!"
    }, headers=headers)
    assert res.status_code == 400
    assert "already in use" in res.json()["detail"]
