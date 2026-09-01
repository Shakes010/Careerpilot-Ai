import pytest

def test_recruiter_registration(client):
    payload = {
        "full_name": "Test Recruiter",
        "email": "testrecruiter@company.com",
        "password": "Password123!",
        "phone": "+91 99999 88888",
        "designation": "HR Lead",
        "company_name": "Acme Software Corp",
        "company_website": "https://acmesoftware.com"
    }
    response = client.post("/api/auth/recruiter/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == "testrecruiter@company.com"
    assert data["data"]["role"] == "RECRUITER"
    assert data["data"]["company_verification_status"] == "PENDING"
    assert "access_token" in data["data"]

def test_duplicate_email_registration(client):
    payload = {
        "full_name": "Original User",
        "email": "unique@company.com",
        "password": "Password123!",
        "company_name": "Acme Corp"
    }
    res1 = client.post("/api/auth/recruiter/register", json=payload)
    assert res1.status_code == 201

    payload_dup = {
        "full_name": "Duplicate User",
        "email": "unique@company.com",
        "password": "Password123!",
        "company_name": "Another Company"
    }
    res2 = client.post("/api/auth/recruiter/register", json=payload_dup)
    assert res2.status_code == 400
    data = res2.json()
    assert "Email is already registered" in data["detail"]

def test_recruiter_login_success(client):
    reg_payload = {
        "full_name": "Login User",
        "email": "loginuser@company.com",
        "password": "Password123!",
        "company_name": "Login Corp"
    }
    client.post("/api/auth/recruiter/register", json=reg_payload)

    login_payload = {
        "email": "loginuser@company.com",
        "password": "Password123!"
    }
    response = client.post("/api/auth/recruiter/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]

def test_recruiter_login_invalid_password(client):
    reg_payload = {
        "full_name": "Invalid Pass User",
        "email": "invalidpass@company.com",
        "password": "Password123!",
        "company_name": "Pass Corp"
    }
    client.post("/api/auth/recruiter/register", json=reg_payload)

    login_payload = {
        "email": "invalidpass@company.com",
        "password": "WrongPassword!"
    }
    response = client.post("/api/auth/recruiter/login", json=login_payload)
    assert response.status_code == 401

def test_unauthenticated_protected_route_access(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401
