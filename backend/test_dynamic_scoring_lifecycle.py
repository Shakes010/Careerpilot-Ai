import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_dynamic_scoring_lifecycle():
    print("=" * 60)
    print("TESTING EXACT DYNAMIC SCORING LIFECYCLE SCENARIO")
    print("=" * 60)

    # A. Create & register a brand new student
    timestamp = int(time.time() * 1000)
    email = f"scoring_lifecycle_{timestamp}@careerpilot.ai"
    reg_res = requests.post(f"{BASE_URL}/auth/register", json={
        "email": email,
        "password": "Password123!",
        "full_name": f"Scoring Test User {timestamp}",
        "university": "NIT Calicut",
        "major": "Computer Science"
    })
    assert reg_res.status_code == 201, f"Registration failed: {reg_res.text}"
    token = reg_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"[STEP A PASS] Created new student: {email}")

    # B & C. Fetch initial profile, dashboard, education, skills, resume, preferences
    res_prof = requests.get(f"{BASE_URL}/student/profile", headers=headers)
    assert res_prof.status_code == 200
    prof = res_prof.json()

    res_dash = requests.get(f"{BASE_URL}/student/dashboard", headers=headers)
    assert res_dash.status_code == 200
    dash = res_dash.json()

    res_edu = requests.get(f"{BASE_URL}/student/education", headers=headers)
    assert res_edu.status_code == 200
    assert len(res_edu.json()) == 0, "Expected 0 education records"

    res_sk = requests.get(f"{BASE_URL}/student/skills", headers=headers)
    assert res_sk.status_code == 200
    assert len(res_sk.json()) == 0, "Expected 0 skills records"

    res_res = requests.get(f"{BASE_URL}/student/resume", headers=headers)
    assert res_res.status_code == 200
    assert res_res.json() is None, "Expected None for resume"

    res_pref = requests.get(f"{BASE_URL}/student/preferences", headers=headers)
    assert res_pref.status_code == 200
    assert res_pref.json() is None, "Expected None for career preferences"
    print("[STEP B & C PASS] Verified initial records: Resume=None, Skills=0, Verified Skills=0, Education=0, Career Preferences=None")

    # D & E. Verify Readiness Index is 0% and Skill Trust Score is 0%
    print(f"-> Initial Readiness Index: {prof['career_readiness_score']}%")
    print(f"-> Initial Skill Trust Score: {prof['skill_trust_meter']}%")
    print(f"-> Initial Verified Skills Count: {prof['verified_skills_count']}")

    assert prof["career_readiness_score"] == 0, f"Expected 0% readiness, got {prof['career_readiness_score']}%"
    assert prof["skill_trust_meter"] == 0.0, f"Expected 0.0% skill trust, got {prof['skill_trust_meter']}%"
    assert prof["verified_skills_count"] == 0, f"Expected 0 verified skills, got {prof['verified_skills_count']}"
    assert dash["completion_percentage"] == 0, f"Expected 0% completion, got {dash['completion_percentage']}%"
    print("[STEP D & E PASS] Verified new student scores are strictly 0% (NOT 60% or 70%).")

    # F. Add one education record and verify readiness score changes
    res_edu_add = requests.post(f"{BASE_URL}/student/education", json={
        "degree": "B.Tech Computer Science",
        "institution": "National Institute of Technology",
        "start_year": 2022,
        "end_year": 2026,
        "grade": "8.9 CGPA"
    }, headers=headers)
    assert res_edu_add.status_code == 201
    edu_id = res_edu_add.json()["id"]

    res_prof_f = requests.get(f"{BASE_URL}/student/profile", headers=headers)
    score_f = res_prof_f.json()["career_readiness_score"]
    print(f"-> Score after adding 1 Education record: {score_f}%")
    assert score_f > 0, f"Expected score > 0 after education, got {score_f}%"
    assert score_f == 15, f"Expected 15%, got {score_f}%"
    print("[STEP F PASS] Readiness score increased after adding education record.")

    # G. Add an unverified skill and verify Skill Trust Score does not incorrectly show 70%
    res_sk_unver = requests.post(f"{BASE_URL}/student/skills", json={
        "skill_name": "Docker",
        "category": "Cloud & DevOps",
        "proficiency": "Intermediate",
        "is_verified": False
    }, headers=headers)
    assert res_sk_unver.status_code == 201
    unver_sk_id = res_sk_unver.json()["id"]

    res_prof_g = requests.get(f"{BASE_URL}/student/profile", headers=headers)
    trust_g = res_prof_g.json()["skill_trust_meter"]
    readiness_g = res_prof_g.json()["career_readiness_score"]
    verified_g = res_prof_g.json()["verified_skills_count"]
    print(f"-> Trust score after 1 unverified skill: {trust_g}% (Verified count: {verified_g}, Readiness: {readiness_g}%)")
    assert trust_g != 70.0, f"Skill trust must NOT show 70%! Got {trust_g}%"
    assert 0 < trust_g < 20.0, f"Expected partial trust ~13.3%, got {trust_g}%"
    assert verified_g == 0, f"Verified count should be 0, got {verified_g}"
    print("[STEP G PASS] Unverified skill calculated proportional partial confidence without showing 70%.")

    # H. Add a verified skill and verify Skill Trust Score and Verified Skills count increase
    res_sk_ver = requests.post(f"{BASE_URL}/student/skills", json={
        "skill_name": "Python",
        "category": "Programming Languages",
        "proficiency": "Advanced",
        "is_verified": True
    }, headers=headers)
    assert res_sk_ver.status_code == 201
    ver_sk_id = res_sk_ver.json()["id"]

    res_prof_h = requests.get(f"{BASE_URL}/student/profile", headers=headers)
    trust_h = res_prof_h.json()["skill_trust_meter"]
    verified_h = res_prof_h.json()["verified_skills_count"]
    readiness_h = res_prof_h.json()["career_readiness_score"]
    print(f"-> Trust score after 1 verified + 1 unverified skill: {trust_h}% (Verified count: {verified_h}, Readiness: {readiness_h}%)")
    assert trust_h > trust_g, f"Trust score should have increased from {trust_g}% to {trust_h}%"
    assert verified_h == 1, f"Expected 1 verified skill, got {verified_h}"
    print("[STEP H PASS] Verified skill increased Skill Trust Score and Verified Skills count.")

    # I. Upload a valid resume and verify resume contributes to readiness
    res_resume = requests.post(f"{BASE_URL}/student/resume/upload", data={
        "summary": "Valid technical resume for student software engineer with Python and Docker experience."
    }, headers=headers)
    assert res_resume.status_code == 200
    resume_id = res_resume.json()["id"]

    res_prof_i = requests.get(f"{BASE_URL}/student/profile", headers=headers)
    readiness_i = res_prof_i.json()["career_readiness_score"]
    print(f"-> Readiness score after uploading resume: {readiness_i}%")
    assert readiness_i > readiness_h, f"Readiness should have increased after resume from {readiness_h}% to {readiness_i}%"
    print("[STEP I PASS] Valid resume upload contributed to Readiness Index.")

    # J. Add career preferences and verify readiness updates
    res_pref_save = requests.put(f"{BASE_URL}/student/preferences", json={
        "preferred_role": "Backend Software Engineer",
        "preferred_industry": "Cloud & AI Tech",
        "preferred_location": "Remote / Bengaluru",
        "employment_type": "Full-Time",
        "work_mode": "Hybrid",
        "expected_salary": "$90,000 / year"
    }, headers=headers)
    assert res_pref_save.status_code == 200

    res_prof_j = requests.get(f"{BASE_URL}/student/profile", headers=headers)
    readiness_j = res_prof_j.json()["career_readiness_score"]
    print(f"-> Readiness score after setting career preferences: {readiness_j}%")
    assert readiness_j > readiness_i, f"Readiness should increase after preferences from {readiness_i}% to {readiness_j}%"
    print("[STEP J PASS] Career preferences added and increased Readiness Index.")

    # K. Delete resume, skill, and education and verify scores decrease accordingly
    # Delete resume
    del_res = requests.delete(f"{BASE_URL}/student/resume/{resume_id}", headers=headers)
    assert del_res.status_code == 204
    res_prof_k1 = requests.get(f"{BASE_URL}/student/profile", headers=headers)
    readiness_k1 = res_prof_k1.json()["career_readiness_score"]
    print(f"-> Readiness after deleting resume: {readiness_k1}% (was {readiness_j}%)")
    assert readiness_k1 < readiness_j, "Readiness should have decreased after deleting resume!"

    # Delete verified skill
    del_sk = requests.delete(f"{BASE_URL}/student/skills/{ver_sk_id}", headers=headers)
    assert del_sk.status_code == 204
    res_prof_k2 = requests.get(f"{BASE_URL}/student/profile", headers=headers)
    trust_k2 = res_prof_k2.json()["skill_trust_meter"]
    verified_k2 = res_prof_k2.json()["verified_skills_count"]
    print(f"-> Trust score after deleting verified skill: {trust_k2}% (Verified count: {verified_k2})")
    assert trust_k2 < trust_h, "Trust score should have decreased after deleting verified skill!"
    assert verified_k2 == 0, "Verified skills count should have decreased to 0!"

    # Delete education
    del_edu = requests.delete(f"{BASE_URL}/student/education/{edu_id}", headers=headers)
    assert del_edu.status_code == 204
    res_prof_k3 = requests.get(f"{BASE_URL}/student/profile", headers=headers)
    readiness_k3 = res_prof_k3.json()["career_readiness_score"]
    print(f"-> Readiness after deleting education: {readiness_k3}%")
    assert readiness_k3 < readiness_k1, "Readiness should have decreased after deleting education!"
    print("[STEP K PASS] Deleting resume, skill, and education dynamically decreased scores.")

    # L & M. Re-login / auth check to simulate browser refresh and session reload
    res_me = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    assert res_me.status_code == 200
    me_prof = res_me.json()["profile"]
    assert me_prof["career_readiness_score"] == readiness_k3
    assert me_prof["skill_trust_meter"] == trust_k2
    assert me_prof["verified_skills_count"] == verified_k2
    print(f"[STEP L & M PASS] Reloaded session from PostgreSQL correctly: Readiness={me_prof['career_readiness_score']}%, Trust={me_prof['skill_trust_meter']}%, Verified={me_prof['verified_skills_count']}")

    print("=" * 60)
    print("ALL DYNAMIC SCORING LIFECYCLE TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    test_dynamic_scoring_lifecycle()
