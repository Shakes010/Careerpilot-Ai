import pytest

def test_company_profile_get_and_update(client):
    # Register recruiter
    reg = client.post("/api/auth/recruiter/register", json={
        "full_name": "Company Admin",
        "email": "admin@techcorp.com",
        "password": "Password123!",
        "company_name": "Tech Corp Pvt Ltd"
    }).json()
    
    token = reg["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Get Profile
    get_res = client.get("/api/recruiter/company", headers=headers)
    assert get_res.status_code == 200
    comp_data = get_res.json()["data"]
    assert comp_data["name"] == "Tech Corp Pvt Ltd"
    assert comp_data["verification_status"] == "PENDING"

    # Update Profile
    update_res = client.put("/api/recruiter/company", json={
        "industry": "Software Engineering",
        "company_size": "100-500 employees",
        "location": "Bengaluru, India",
        "description": "Leading cloud solutions company."
    }, headers=headers)
    assert update_res.status_code == 200
    updated_data = update_res.json()["data"]
    assert updated_data["industry"] == "Software Engineering"
    assert updated_data["location"] == "Bengaluru, India"
