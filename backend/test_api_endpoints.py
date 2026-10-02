import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_full_platform_flow():
    print("--- 1. Testing Auth & CS/IT Eligibility Check ---")
    reg_payload = {
        "email": f"student_{uuid.uuid4().hex[:6]}@example.com",
        "password": "Password123!",
        "role": "student",
        "full_name": "Sensha Student",
        "degree": "B.Tech Computer Science",
        "graduation_year": 2026,
        "college_name": "Tech Institute"
    }
    res = client.post("/auth/register", json=reg_payload)
    assert res.status_code == 200, f"Register failed: {res.text}"
    token_data = res.json()
    assert token_data["is_eligible"] == True
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"Auth Success! Token issued for {reg_payload['email']}")

    print("--- 2. Testing Student Profile & Career Passport ---")
    res = client.get("/profile/student", headers=headers)
    assert res.status_code == 200
    passport_res = client.get("/profile/career-passport", headers=headers)
    assert passport_res.status_code == 200
    print("Career Passport retrieved successfully.")

    print("--- 3. Testing Skills & Assessment Checkpoint Order Enforcement ---")
    # Fetch skills
    skills_res = client.get("/skills")
    skills = skills_res.json()
    assert len(skills) > 0
    py_skill = next((s for s in skills if s["skill_name"] == "Python"), skills[0])

    # Add skill
    add_sk = client.post("/skills/my-skills", headers=headers, json={"skill_id": py_skill["id"], "self_rating": 4})
    assert add_sk.status_code == 200

    # Get python assessment
    ass_res = client.get("/assessments")
    assessments = ass_res.json()
    assert len(assessments) > 0
    target_ass = assessments[0]

    det_res = client.get(f"/assessments/{target_ass['id']}")
    cps = det_res.json()["checkpoints"]
    assert len(cps) >= 2

    start_res = client.post(f"/assessments/{target_ass['id']}/start", headers=headers)
    attempt_id = start_res.json()["attempt_id"]

    # TRY SUBMITTING CHECKPOINT 2 BEFORE CHECKPOINT 1 -> MUST FAIL WITH HTTP 400!
    cp2 = cps[1]
    err_res = client.post(
        f"/assessments/attempts/{attempt_id}/checkpoints/{cp2['id']}/submit",
        headers=headers,
        json={"submitted_code": "def foo(): pass", "paste_event_count": 0, "paste_char_count": 0, "time_spent_seconds": 10}
    )
    assert err_res.status_code == 400, f"Expected 400 for out-of-order checkpoint, got: {err_res.status_code}"
    print(f"Out-of-Order Checkpoint Blocked Correctly: {err_res.json()['detail']}")

    # Submit Checkpoint 1 properly
    cp1 = cps[0]
    ok_res = client.post(
        f"/assessments/attempts/{attempt_id}/checkpoints/{cp1['id']}/submit",
        headers=headers,
        json={"submitted_code": "def reverse_words(s): return ' '.join(s.split()[::-1])", "paste_event_count": 0, "paste_char_count": 0, "time_spent_seconds": 15}
    )
    assert ok_res.status_code == 200
    print("Checkpoint 1 Submitted cleanly.")

    print("--- 4. Testing Project Collaboration & Verified Completion ---")
    proj_res = client.post(
        "/projects",
        headers=headers,
        json={"title": "AI Career Assistant", "description": "Full stack project", "tech_stack": ["Python", "FastAPI"]}
    )
    assert proj_res.status_code == 200
    proj_id = proj_res.json()["id"]

    verify_res = client.post(f"/projects/{proj_id}/verify", headers=headers)
    assert verify_res.status_code == 200
    print("Project Verified and Skill Trust Meter recalculated.")

    print("--- 5. Testing Recruiter Registration & Domain Match Analysis ---")
    rec_email = f"recruiter_{uuid.uuid4().hex[:6]}@techcorp.com"
    rec_reg = client.post("/auth/register", json={
        "email": rec_email,
        "password": "RecruiterPass123!",
        "role": "recruiter",
        "full_name": "Sid Recruiter"
    })
    rec_token = rec_reg.json()["access_token"]
    rec_headers = {"Authorization": f"Bearer {rec_token}"}

    comp_res = client.post("/recruiter/register-company", headers=rec_headers, json={
        "name": "Tech Corp",
        "industry": "Software",
        "email": "hr@techcorp.com",
        "website": "https://techcorp.com"
    })
    assert comp_res.status_code == 200
    assert "Domain match verified" in comp_res.json()["verification_notes"]
    print(f"Recruiter Company Registered: {comp_res.json()['verification_notes']}")

    print("--- 6. Testing Razorpay Payment Sandbox Signature Verification ---")
    plans_res = client.get("/payments/plans")
    plans = plans_res.json()
    prem_plan = next((p for p in plans if p["tier"] == "premium"), plans[0])

    order_res = client.post("/payments/create-order", headers=rec_headers, json={"plan_id": prem_plan["id"]})
    assert order_res.status_code == 200
    order_id = order_res.json()["order_id"]

    verify_res = client.post("/payments/verify", headers=rec_headers, json={
        "plan_id": prem_plan["id"],
        "razorpay_order_id": order_id,
        "razorpay_payment_id": "pay_mock123456",
        "razorpay_signature": "sandbox_test_signature"
    })
    assert verify_res.status_code == 200
    assert verify_res.json()["status"] == "success"
    print("Razorpay Payment Webhook Verified Server-Side Successfully!")

    print("\n==================================================")
    print("ALL API ENDPOINT & CONTRACT TESTS PASSED PERFECTLY!")
    print("==================================================")

if __name__ == "__main__":
    test_full_platform_flow()
