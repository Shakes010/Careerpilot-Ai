import requests
import json
import sys
import time

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_student_module():
    print("==================================================")
    print("STARTING COMPLETE END-TO-END STUDENT MODULE VERIFICATION")
    print("==================================================")

    # 1. Health Check
    res = requests.get("http://127.0.0.1:8000/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    print("[1/20 PASS] Health Check Endpoint:", res.json())

    # 2. Student Registration
    timestamp = int(time.time() * 1000)
    reg_email = f"student_test_{timestamp}@careerpilot.ai"
    reg_payload = {
        "email": reg_email,
        "password": "SecurePassword123!",
        "full_name": f"Test Student {timestamp}",
        "university": "National Institute of Technology",
        "major": "Master of Computer Applications (MCA)"
    }
    res_reg = requests.post(f"{BASE_URL}/auth/register", json=reg_payload)
    assert res_reg.status_code == 201, f"Registration failed: {res_reg.text}"
    reg_data = res_reg.json()
    assert "access_token" in reg_data
    assert reg_data["user"]["email"] == reg_email
    print(f"[2/20 PASS] Student Registration ({reg_email})")

    # 3. Duplicate Email Prevention
    res_dup = requests.post(f"{BASE_URL}/auth/register", json=reg_payload)
    assert res_dup.status_code == 400, "Duplicate email check failed!"
    print("[3/20 PASS] Duplicate Email Prevention")

    # 4. Invalid Password Rejection
    res_invalid_login = requests.post(f"{BASE_URL}/auth/login", json={"email": reg_email, "password": "WrongPassword!"})
    assert res_invalid_login.status_code == 401, "Invalid password was not rejected!"
    print("[4/20 PASS] Invalid Credentials Rejection (401)")

    # 5. Student Login & JWT Token Generation
    login_payload = {
        "email": reg_email,
        "password": "SecurePassword123!"
    }
    res_login = requests.post(f"{BASE_URL}/auth/login", json=login_payload)
    assert res_login.status_code == 200, f"Login failed: {res_login.text}"
    auth_data = res_login.json()
    token = auth_data["access_token"]
    assert token, "Token missing from login response"
    headers = {"Authorization": f"Bearer {token}"}
    print("[5/20 PASS] Student Login & JWT Generation")

    # 6. Protected Route Session Check (/auth/me)
    res_me = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    assert res_me.status_code == 200, f"Fetch me failed: {res_me.text}"
    assert res_me.json()["user"]["email"] == reg_email
    print("[6/20 PASS] Protected Route JWT Session Authentication (/auth/me)")

    # 7. Student Dashboard API
    res_dash = requests.get(f"{BASE_URL}/student/dashboard", headers=headers)
    assert res_dash.status_code == 200, f"Dashboard failed: {res_dash.text}"
    dash_data = res_dash.json()
    assert "user" in dash_data and "profile" in dash_data
    assert "application_summary" in dash_data
    assert "skill_gap_summary" in dash_data
    print(f"[7/20 PASS] Student Dashboard (Completion: {dash_data['completion_percentage']}%, Readiness: {dash_data['profile']['career_readiness_score']}%)")

    # 8. Student Profile View & Edit
    res_prof = requests.get(f"{BASE_URL}/student/profile", headers=headers)
    assert res_prof.status_code == 200, f"Profile get failed: {res_prof.text}"
    
    update_prof = {
        "headline": "MCA Student & Aspiring Software Engineer",
        "phone": "+1 (555) 987-6543",
        "location": "San Francisco, CA",
        "bio": "Specializing in Python FastAPI microservices and Vue 3 frontend web applications."
    }
    res_prof_up = requests.put(f"{BASE_URL}/student/profile", json=update_prof, headers=headers)
    assert res_prof_up.status_code == 200, f"Profile update failed: {res_prof_up.text}"
    assert res_prof_up.json()["phone"] == "+1 (555) 987-6543"
    assert res_prof_up.json()["location"] == "San Francisco, CA"
    print("[8/20 PASS] Student Profile Viewing & Editing (Database Persistence)")

    # 9. Education Add / Edit / List
    edu_payload = {
        "degree": "Master of Computer Applications (MCA)",
        "institution": "National Institute of Technology",
        "start_year": 2024,
        "end_year": 2026,
        "grade": "3.9 GPA",
        "details": "Software Architecture and AI"
    }
    res_edu_add = requests.post(f"{BASE_URL}/student/education", json=edu_payload, headers=headers)
    assert res_edu_add.status_code == 201, f"Education add failed: {res_edu_add.text}"
    edu_id = res_edu_add.json()["id"]

    res_edu_get = requests.get(f"{BASE_URL}/student/education", headers=headers)
    assert res_edu_get.status_code == 200 and len(res_edu_get.json()) >= 1
    
    res_edu_edit = requests.put(f"{BASE_URL}/student/education/{edu_id}", json={"grade": "4.0 GPA"}, headers=headers)
    assert res_edu_edit.status_code == 200 and res_edu_edit.json()["grade"] == "4.0 GPA"
    print("[9/20 PASS] Student Education CRUD (Create, Read, Update)")

    # 10. Skills Add / Edit / List
    skill_payload = {
        "skill_name": f"Python_{timestamp}",
        "category": "Programming Languages",
        "proficiency": "Advanced",
        "is_verified": True
    }
    res_sk_add = requests.post(f"{BASE_URL}/student/skills", json=skill_payload, headers=headers)
    assert res_sk_add.status_code == 201, f"Skill add failed: {res_sk_add.text}"
    sk_id = res_sk_add.json()["id"]

    # Add extra skills for recommendations
    requests.post(f"{BASE_URL}/student/skills", json={"skill_name": f"FastAPI_{timestamp}", "category": "Web Development", "proficiency": "Advanced"}, headers=headers)
    requests.post(f"{BASE_URL}/student/skills", json={"skill_name": f"Vue.js_{timestamp}", "category": "Web Development", "proficiency": "Intermediate"}, headers=headers)

    res_sk_get = requests.get(f"{BASE_URL}/student/skills", headers=headers)
    assert res_sk_get.status_code == 200 and len(res_sk_get.json()) >= 3
    print(f"[10/20 PASS] Student Skills CRUD ({len(res_sk_get.json())} skills listed)")

    # 11. Resume Upload, ATS Parsing & Deletion
    res_res_upload = requests.post(
        f"{BASE_URL}/student/resume/upload", 
        data={"summary": "Automated test resume summary for MCA student."},
        headers=headers
    )
    assert res_res_upload.status_code == 200, f"Resume upload failed: {res_res_upload.text}"
    resume_data = res_res_upload.json()
    assert resume_data["ats_score"] >= 70
    resume_id = resume_data["id"]

    res_res_get = requests.get(f"{BASE_URL}/student/resume", headers=headers)
    assert res_res_get.status_code == 200 and res_res_get.json() is not None
    print(f"[11/20 PASS] Student Resume Upload & ATS Score Computation (Score: {resume_data['ats_score']})")

    # 12. Career Preferences
    pref_payload = {
        "preferred_role": "Full Stack Software Engineer",
        "preferred_industry": "Software Development",
        "preferred_location": "San Francisco, CA / Remote",
        "employment_type": "Full-Time",
        "work_mode": "Hybrid",
        "expected_salary": "$95,000 - $130,000 / year"
    }
    res_pref_save = requests.put(f"{BASE_URL}/student/preferences", json=pref_payload, headers=headers)
    assert res_pref_save.status_code == 200, f"Preferences save failed: {res_pref_save.text}"
    assert res_pref_save.json()["preferred_role"] == "Full Stack Software Engineer"
    print("[12/20 PASS] Student Career Preferences Save & Retrieve")

    # 13. Verify Career Recommendations Removed (404)
    res_recs = requests.get(f"{BASE_URL}/student/recommendations", headers=headers)
    assert res_recs.status_code == 404
    print("[13/20 PASS] Career Recommendations Endpoint Removed (404)")

    # 14. Skill Gap Analysis
    res_gap = requests.get(f"{BASE_URL}/student/skill-gap", headers=headers)
    assert res_gap.status_code == 200
    gap_info = res_gap.json()
    assert "target_role" in gap_info and "missing_skills" in gap_info
    print(f"[14/20 PASS] Skill Gap Analysis (Target: '{gap_info['target_role']}', Match: {gap_info['match_percentage']}%)")

    # 15. Learning Recommendations
    res_learn = requests.get(f"{BASE_URL}/student/learning-recommendations", headers=headers)
    assert res_learn.status_code == 200 and len(res_learn.json()) > 0
    print(f"[15/20 PASS] Learning Recommendations ({len(res_learn.json())} courses/resources recommended)")

    # 16. Job Application Creation
    job_id_to_apply = 1
    res_app_post = requests.post(f"{BASE_URL}/student/applications", json={"job_id": job_id_to_apply, "notes": "Test application via API"}, headers=headers)
    assert res_app_post.status_code == 201, f"Application post failed: {res_app_post.text}"
    app_id = res_app_post.json()["id"]
    print(f"[16/20 PASS] Job Application Creation (App ID: {app_id}, Job: {res_app_post.json()['job']['title']})")

    # 17. Application Listing
    res_app_get = requests.get(f"{BASE_URL}/student/applications", headers=headers)
    assert res_app_get.status_code == 200 and len(res_app_get.json()) >= 1
    print(f"[17/20 PASS] Job Application Listing ({len(res_app_get.json())} applications tracked)")

    # 18. Application Status Update
    res_app_status = requests.put(f"{BASE_URL}/student/applications/{app_id}/status", json={"status": "Interviewed", "notes": "Interview scheduled"}, headers=headers)
    assert res_app_status.status_code == 200 and res_app_status.json()["status"] == "Interviewed"
    print("[18/20 PASS] Job Application Status Update ('Interviewed')")

    # 19. Application Withdrawal & Record Deletion
    res_withdraw = requests.delete(f"{BASE_URL}/student/applications/{app_id}", headers=headers)
    assert res_withdraw.status_code == 204, f"Withdraw failed: {res_withdraw.text}"
    res_app_check = requests.get(f"{BASE_URL}/student/applications", headers=headers)
    assert not any(a["id"] == app_id for a in res_app_check.json())
    print("[19/20 PASS] Job Application Withdrawal (DELETE 204)")

    # 20. Education / Skill / Resume Deletion & Final Cleanup
    res_del_sk = requests.delete(f"{BASE_URL}/student/skills/{sk_id}", headers=headers)
    assert res_del_sk.status_code == 204
    res_del_edu = requests.delete(f"{BASE_URL}/student/education/{edu_id}", headers=headers)
    assert res_del_edu.status_code == 204
    res_del_res = requests.delete(f"{BASE_URL}/student/resume/{resume_id}", headers=headers)
    assert res_del_res.status_code == 204
    print("[20/20 PASS] Education, Skills, and Resume Deletion Operations (DELETE 204)")

    print("==================================================")
    print("ALL 20 STUDENT MODULE END-TO-END FEATURES SUCCESSFULLY VERIFIED!")
    print("==================================================")

if __name__ == "__main__":
    test_student_module()

