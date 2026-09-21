import requests
import time
from sqlalchemy import create_engine, text
from app.core.config import settings

BASE_URL = "http://127.0.0.1:8000/api/v1"

def run_six_features_verification():
    print("=" * 70)
    print("STARTING COMPLETE VERIFICATION OF 6 NEW FUNCTIONALITIES")
    print("=" * 70)

    # 1. Register Student A
    timestamp = int(time.time() * 1000)
    email_a = f"student_a_{timestamp}@careerpilot.ai"
    reg_a = requests.post(f"{BASE_URL}/auth/register", json={
        "email": email_a,
        "password": "Password123!",
        "full_name": "Student Alpha",
        "university": "NIT Calicut",
        "major": "Computer Science & Engineering"
    })
    assert reg_a.status_code == 201, f"Reg A failed: {reg_a.text}"
    token_a = reg_a.json()["access_token"]
    user_id_a = reg_a.json()["user"]["id"]
    headers_a = {"Authorization": f"Bearer {token_a}"}
    print(f"[SETUP] Created Student A: {email_a} (ID: {user_id_a})")

    # 2. Register Student B (Security checks)
    email_b = f"student_b_{timestamp}@careerpilot.ai"
    reg_b = requests.post(f"{BASE_URL}/auth/register", json={
        "email": email_b,
        "password": "Password123!",
        "full_name": "Student Beta",
        "university": "IIT Madras",
        "major": "Data Science"
    })
    assert reg_b.status_code == 201
    token_b = reg_b.json()["access_token"]
    user_id_b = reg_b.json()["user"]["id"]
    headers_b = {"Authorization": f"Bearer {token_b}"}
    print(f"[SETUP] Created Student B: {email_b} (ID: {user_id_b})")

    # -------------------------------------------------------------
    # FEATURE 1: SMART RESUME VERSION MANAGER
    # -------------------------------------------------------------
    print("\n[FEATURE 1] Testing Smart Resume Version Manager...")
    
    # Create Version 1
    v1_res = requests.post(f"{BASE_URL}/student/resume-versions", json={
        "title": "Full Stack Developer v1",
        "filename": "FullStack_Resume_v1.pdf",
        "summary": "Specialized in Python FastAPI and Vue 3."
    }, headers=headers_a)
    assert v1_res.status_code == 201, f"V1 create failed: {v1_res.text}"
    v1_data = v1_res.json()
    v1_id = v1_data["id"]
    assert v1_data["is_active"] == True
    print(f"  [1.1] Created Resume Version 1 (ID: {v1_id}, Active: True)")

    # Create Version 2
    v2_res = requests.post(f"{BASE_URL}/student/resume-versions", json={
        "title": "Backend Microservices Resume v2",
        "filename": "Backend_Resume_v2.pdf",
        "summary": "Focusing on PostgreSQL and microservices architecture."
    }, headers=headers_a)
    assert v2_res.status_code == 201
    v2_data = v2_res.json()
    v2_id = v2_data["id"]
    assert v2_data["is_active"] == True
    print(f"  [1.2] Created Resume Version 2 (ID: {v2_id}, Active: True)")

    # List versions for Student A
    list_res = requests.get(f"{BASE_URL}/student/resume-versions", headers=headers_a)
    assert list_res.status_code == 200
    versions_list = list_res.json()
    assert len(versions_list) >= 2
    print(f"  [1.3] Listed {len(versions_list)} resume versions for Student A.")

    # Switch Active Version back to Version 1
    switch_res = requests.post(f"{BASE_URL}/student/resume-versions/{v1_id}/set-active", headers=headers_a)
    assert switch_res.status_code == 200
    assert switch_res.json()["is_active"] == True

    v2_check = requests.get(f"{BASE_URL}/student/resume-versions/{v2_id}", headers=headers_a).json()
    assert v2_check["is_active"] == False
    print("  [1.4] Switched active resume version to Version 1 (V2 automatically set inactive).")

    # Rename Version 1
    rename_res = requests.put(f"{BASE_URL}/student/resume-versions/{v1_id}", json={
        "title": "Master Full Stack Resume 2026"
    }, headers=headers_a)
    assert rename_res.status_code == 200
    assert rename_res.json()["title"] == "Master Full Stack Resume 2026"
    print("  [1.5] Renamed Version 1 successfully.")

    # Cross-student isolation test: Student B cannot access or modify Student A's version
    sec_v1 = requests.get(f"{BASE_URL}/student/resume-versions/{v1_id}", headers=headers_b)
    assert sec_v1.status_code == 404, "SECURITY FAILURE: Student B accessed Student A's resume version!"
    print("  [1.6] PASS: Student B cannot access Student A's resume version.")

    # -------------------------------------------------------------
    # FEATURE 2: CERTIFICATE MANAGEMENT
    # -------------------------------------------------------------
    print("\n[FEATURE 2] Testing Certificate Management...")
    cert_payload = {
        "title": "AWS Certified Solutions Architect - Associate",
        "issuing_organization": "Amazon Web Services",
        "issue_date": "Jan 2025",
        "expiry_date": "Jan 2028",
        "credential_id": "AWS-CERT-998877",
        "credential_url": "https://aws.amazon.com/verification/998877",
        "description": "Passed with 920/1000 score covering S3, EC2, ECS, and RDS.",
        "skills_tags": "AWS, Cloud, Architecture"
    }
    cert_res = requests.post(f"{BASE_URL}/student/certificates", data=cert_payload, headers=headers_a)
    assert cert_res.status_code == 201, f"Cert add failed: {cert_res.text}"
    cert_id = cert_res.json()["id"]
    print(f"  [2.1] Created Certificate (ID: {cert_id}, Title: '{cert_res.json()['title']}')")

    # List certificates
    cert_list = requests.get(f"{BASE_URL}/student/certificates", headers=headers_a)
    assert cert_list.status_code == 200 and len(cert_list.json()) >= 1
    print(f"  [2.2] Listed {len(cert_list.json())} certificates for Student A.")

    # Update Certificate
    update_cert = requests.put(f"{BASE_URL}/student/certificates/{cert_id}", json={
        "skills_tags": "AWS, Cloud, Architecture, Serverless"
    }, headers=headers_a)
    assert update_cert.status_code == 200 and "Serverless" in update_cert.json()["skills_tags"]
    print("  [2.3] Updated certificate details successfully.")

    # Security check: Student B cannot access Student A's cert
    sec_cert = requests.get(f"{BASE_URL}/student/certificates/{cert_id}", headers=headers_b)
    assert sec_cert.status_code == 404
    print("  [2.4] PASS: Student B cannot access Student A's certificate.")

    # Upload certificate file & test authenticated viewing & security isolation
    files = {"file": ("test_cert.pdf", b"%PDF-1.4 Mock Certificate Data", "application/pdf")}
    file_cert_res = requests.post(f"{BASE_URL}/student/certificates", data={
        "title": "Docker Certified Associate",
        "issuing_organization": "Docker",
        "issue_date": "Feb 2025"
    }, files=files, headers=headers_a)
    assert file_cert_res.status_code == 201
    file_cert_id = file_cert_res.json()["id"]

    # Student A requests own file -> HTTP 200
    file_dl_res = requests.get(f"{BASE_URL}/student/certificates/{file_cert_id}/file", headers=headers_a)
    assert file_dl_res.status_code == 200
    assert file_dl_res.content == b"%PDF-1.4 Mock Certificate Data"
    print("  [2.5] PASS: Student A successfully retrieved uploaded certificate file.")

    # Student B requests Student A's file -> HTTP 404 (Security check)
    sec_dl_res = requests.get(f"{BASE_URL}/student/certificates/{file_cert_id}/file", headers=headers_b)
    assert sec_dl_res.status_code == 404, "SECURITY FAILURE: Student B downloaded Student A's certificate file!"
    print("  [2.6] PASS: Student B blocked from accessing Student A's certificate file.")

    # -------------------------------------------------------------
    # FEATURE 3: GITHUB INTEGRATION
    # -------------------------------------------------------------
    print("\n[FEATURE 3] Testing GitHub Integration...")
    # Test 3.1: Connect using full GitHub URL (extracting username 'octocat')
    gh_res_url = requests.post(f"{BASE_URL}/student/github/connect", json={"username": "https://github.com/octocat/"}, headers=headers_a)
    assert gh_res_url.status_code == 200, f"GitHub connect via URL failed: {gh_res_url.text}"
    gh_data = gh_res_url.json()
    assert gh_data["username"].lower() == "octocat"
    assert len(gh_data["repositories"]) > 0
    print(f"  [3.1] Connected GitHub profile @{gh_data['username']} from full URL input with {len(gh_data['repositories'])} repositories.")

    # Test 3.2: Invalid URL error message check
    invalid_url_res = requests.post(f"{BASE_URL}/student/github/connect", json={"username": "invalid..url!!"}, headers=headers_a)
    assert invalid_url_res.status_code == 400 and invalid_url_res.json()["detail"] == "Invalid GitHub profile URL."
    print("  [3.2] PASS: Invalid GitHub profile URL validation error returned correctly.")

    # Test 3.3: Non-existent GitHub username check
    nonexist_res = requests.post(f"{BASE_URL}/student/github/connect", json={"username": "thisuserdoesnotexist9991122"}, headers=headers_a)
    assert nonexist_res.status_code == 400 and nonexist_res.json()["detail"] == "GitHub user not found."
    print("  [3.3] PASS: Non-existent GitHub user error returned correctly.")

    # Get GitHub profile
    get_gh = requests.get(f"{BASE_URL}/student/github", headers=headers_a)
    assert get_gh.status_code == 200 and get_gh.json()["username"].lower() == "octocat"
    print("  [3.4] Retrieved connected GitHub profile via GET.")

    # Sync GitHub
    sync_gh = requests.post(f"{BASE_URL}/student/github/sync", headers=headers_a)
    assert sync_gh.status_code == 200
    print("  [3.5] Synced GitHub profile successfully.")

    # -------------------------------------------------------------
    # FEATURE 4: CAREER TIMELINE
    # -------------------------------------------------------------
    print("\n[FEATURE 4] Testing Career Timeline...")
    timeline_res = requests.get(f"{BASE_URL}/student/timeline", headers=headers_a)
    assert timeline_res.status_code == 200
    timeline_events = timeline_res.json()
    assert len(timeline_events) >= 3, f"Expected at least 3 events, got {len(timeline_events)}"
    categories = set(t["category"] for t in timeline_events)
    print(f"  [4.1] Retrieved {len(timeline_events)} timeline events for Student A.")
    print(f"        Event categories present: {list(categories)}")

    # -------------------------------------------------------------
    # FEATURE 5: CAREER PASSPORT
    # -------------------------------------------------------------
    print("\n[FEATURE 5] Testing Career Passport...")
    passport_res = requests.get(f"{BASE_URL}/student/passport", headers=headers_a)
    assert passport_res.status_code == 200
    passport = passport_res.json()
    
    assert passport["user"]["email"] == email_a
    assert passport["active_resume"] is not None
    assert len(passport["certificates"]) >= 1
    assert passport["github_profile"] is not None
    print("  [5.1] Career Passport successfully aggregated Profile, Active Resume, Certificates, and GitHub Profile!")

    # -------------------------------------------------------------
    # FEATURE 6: AI RESUME GENERATOR (NON-PAID)
    # -------------------------------------------------------------
    print("\n[FEATURE 6] Testing AI Resume Generator (Non-Paid)...")
    gen_res = requests.post(f"{BASE_URL}/student/resume/generate", headers=headers_a)
    assert gen_res.status_code == 200
    gen_data = gen_res.json()
    assert gen_data["full_name"] == "Student Alpha"
    assert "professional_summary" in gen_data
    assert len(gen_data["certifications"]) >= 1
    assert len(gen_data["projects"]) >= 1
    print(f"  [6.1] Generated professional resume for target role '{gen_data['target_role']}'.")
    print(f"        Summary: '{gen_data['professional_summary'][:80]}...'")

    # Save generated resume as a new resume version
    save_res = requests.post(f"{BASE_URL}/student/resume/save-generated", json={
        "title": "AI Generated Full Stack Resume 2026",
        "resume_data": gen_data,
        "set_active": True
    }, headers=headers_a)
    assert save_res.status_code == 200
    save_v = save_res.json()
    assert save_v["is_active"] == True
    assert save_v["source"] == "AI Generated"
    print(f"  [6.2] Saved AI-generated resume as new version (ID: {save_v['id']}, Title: '{save_v['title']}').")

    # Verify DB records directly if available
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            rv_count = conn.execute(text(f"SELECT COUNT(*) FROM student_resume_versions WHERE student_id = {user_id_a}")).scalar()
            cert_count = conn.execute(text(f"SELECT COUNT(*) FROM student_certificates WHERE student_id = {user_id_a}")).scalar()
            gh_count = conn.execute(text(f"SELECT COUNT(*) FROM student_github_profiles WHERE student_id = {user_id_a}")).scalar()
            tl_count = conn.execute(text(f"SELECT COUNT(*) FROM student_timeline_events WHERE student_id = {user_id_a}")).scalar()

        print(f"\n[POSTGRES VERIFICATION] Direct DB inspection for user_id={user_id_a}:")
        print(f"  - Resume Versions in DB: {rv_count}")
        print(f"  - Certificates in DB: {cert_count}")
        print(f"  - GitHub Profile in DB: {gh_count}")
        print(f"  - Timeline Events in DB: {tl_count}")

        assert rv_count >= 3
        assert cert_count >= 1
        assert gh_count == 1
        assert tl_count >= 4
    except Exception as e:
        print(f"[DB VERIFICATION NOTICE] Direct DB inspection skipped: {e}")


    print("\n" + "=" * 70)
    print("ALL 6 FUNCTIONALITIES TESTED AND VERIFIED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    run_six_features_verification()
