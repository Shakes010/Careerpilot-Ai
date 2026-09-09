import pytest
from app.models.user import User, UserRole
from app.core.security import get_password_hash

@pytest.fixture
def sample_user(db_session):
    user = User(
        email="student@careerpilot.ai",
        password_hash=get_password_hash("StudentPass123!"),
        full_name="Test Student User",
        role=UserRole.STUDENT
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

def test_send_notification_and_list_by_user(client, sample_user):
    # 1. Send notification
    payload = {
        "user_id": sample_user.id,
        "title": "Welcome Alert",
        "message": "Welcome to CareerPilot AI platform!"
    }
    response = client.post("/api/notifications/", json=payload)
    assert response.status_code == 201
    res_data = response.json()
    assert res_data["success"] is True
    assert res_data["data"]["title"] == "Welcome Alert"
    assert res_data["data"]["is_read"] is False
    notification_id = res_data["data"]["id"]

    # 2. Get notifications by user ID
    list_res = client.get(f"/api/notifications/user/{sample_user.id}")
    assert list_res.status_code == 200
    list_data = list_res.json()
    assert list_data["success"] is True
    assert len(list_data["data"]) == 1
    assert list_data["data"][0]["id"] == notification_id

def test_send_notification_invalid_user(client):
    payload = {
        "user_id": "nonexistent-user-id",
        "title": "Invalid Test",
        "message": "Should fail with 404"
    }
    response = client.post("/api/notifications/", json=payload)
    assert response.status_code == 404

def test_list_notifications_invalid_user(client):
    response = client.get("/api/notifications/user/nonexistent-user-id")
    assert response.status_code == 404

def test_get_my_notifications_and_mark_read(client, sample_user):
    # 1. Send a notification to sample_user
    client.post("/api/notifications/", json={
        "user_id": sample_user.id,
        "title": "Unread Notification",
        "message": "Check your dashboard updates."
    })

    # 2. Login as sample_user to get access token
    login_res = client.post("/api/auth/login", json={
        "email": "student@careerpilot.ai",
        "password": "StudentPass123!"
    })
    assert login_res.status_code == 200
    token = login_res.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Fetch /me notifications
    me_res = client.get("/api/notifications/me", headers=headers)
    assert me_res.status_code == 200
    me_data = me_res.json()["data"]
    assert me_data["unread_count"] == 1
    assert len(me_data["notifications"]) == 1
    notification_id = me_data["notifications"][0]["id"]

    # 4. Mark notification as read
    read_res = client.patch(f"/api/notifications/{notification_id}/read", json={"is_read": True})
    assert read_res.status_code == 200
    assert read_res.json()["data"]["is_read"] is True

    # 5. Fetch /me notifications again to confirm unread_count is 0
    me_res_updated = client.get("/api/notifications/me", headers=headers)
    assert me_res_updated.json()["data"]["unread_count"] == 0

def test_mark_read_invalid_notification(client):
    response = client.patch("/api/notifications/invalid-notification-id/read", json={"is_read": True})
    assert response.status_code == 404
