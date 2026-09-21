import io
import requests
import json
import time
import pypdf
import docx
from sqlalchemy import create_engine, text
from app.core.config import settings

BASE_URL = "http://127.0.0.1:8000/api/v1"

def make_pdf(lines):
    stream = 'BT\n/F1 12 Tf\n50 750 Td\n15 TL\n' + ''.join([f'({l}) \x27\n' for l in lines]) + 'ET\n'
    body = f"""%PDF-1.4
1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj
2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj
3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj
4 0 obj << /Length {len(stream)} >>
stream
{stream}endstream
endobj
5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj
xref
0 6
0000000000 65535 f 
trailer << /Size 6 /Root 1 0 R >>
startxref
1
%%EOF"""
    return body.encode('latin1')

def make_docx(lines):
    doc = docx.Document()
    for l in lines:
        doc.add_paragraph(l)
    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()

def run_tests():
    print("=" * 60)
    print("STARTING RESUME & ATS VALIDATION SYSTEM VERIFICATION")
    print("=" * 60)

    # 1. Register a test user
    timestamp = int(time.time() * 1000)
    email = f"resume_val_test_{timestamp}@careerpilot.ai"
    reg_res = requests.post(f"{BASE_URL}/auth/register", json={
        "email": email,
        "password": "Password123!",
        "full_name": "Validation Tester",
        "university": "State University",
        "major": "Computer Science"
    })
    assert reg_res.status_code == 201, f"Reg failed: {reg_res.text}"
    token = reg_res.json()["access_token"]
    user_id = reg_res.json()["user"]["id"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"[SETUP] Created test user: {email} (ID: {user_id})")

    # Verify no resume in DB initially if direct DB accessible
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            res = conn.execute(text(f"SELECT COUNT(*) FROM student_resumes WHERE student_id = {user_id}")).scalar()
            assert res == 0, "Expected 0 resume records initially"
        print("[PASS] Initial state: 0 resume records in PostgreSQL.")
    except Exception as e:
        print(f"[NOTICE] Direct DB inspection skipped: {e}")

    # -------------------------------------------------------------
    # TEST 1: Aadhaar Card PDF Upload (Must be rejected with HTTP 400)
    # -------------------------------------------------------------
    aadhaar_lines = [
        "Government of India",
        "Unique Identification Authority of India",
        "Enrollment No: 1234/56789/01234",
        "Name: Rahul Sharma",
        "DOB: 15/08/1998",
        "Gender: Male",
        "Address: 123 Main St, New Delhi, India",
        "1234 5678 9012",
        "Mera Aadhaar, Meri Pehchan"
    ]
    aadhaar_pdf = make_pdf(aadhaar_lines)
    files = {"file": ("aadhaar_card.pdf", aadhaar_pdf, "application/pdf")}
    res_aadhaar = requests.post(f"{BASE_URL}/student/resume/upload", files=files, headers=headers)
    print(f"[TEST 1] Aadhaar PDF Upload Response: HTTP {res_aadhaar.status_code} - {res_aadhaar.json()}")
    assert res_aadhaar.status_code == 400, f"Expected 400, got {res_aadhaar.status_code}"
    assert "not appear to be a valid resume" in res_aadhaar.json()["detail"].lower() or "valid resume" in res_aadhaar.json()["detail"].lower()
    print("[TEST 1 PASS] Aadhaar Card correctly rejected (HTTP 400).")

    # -------------------------------------------------------------
    # TEST 2: Tax Invoice PDF Upload (Must be rejected with HTTP 400)
    # -------------------------------------------------------------
    invoice_lines = [
        "TAX INVOICE",
        "Invoice No: INV-2026-001",
        "Date: 12/01/2026",
        "Billed To: ACME Corporation",
        "GSTIN: 29ABCDE1234F1Z5",
        "Total Amount Due: $1,250.00",
        "Due Date: 26/01/2026"
    ]
    invoice_pdf = make_pdf(invoice_lines)
    files = {"file": ("tax_invoice.pdf", invoice_pdf, "application/pdf")}
    res_inv = requests.post(f"{BASE_URL}/student/resume/upload", files=files, headers=headers)
    print(f"[TEST 2] Tax Invoice PDF Upload Response: HTTP {res_inv.status_code} - {res_inv.json()}")
    assert res_inv.status_code == 400
    print("[TEST 2 PASS] Tax Invoice correctly rejected (HTTP 400).")

    # -------------------------------------------------------------
    # TEST 3: Semester Marksheet PDF Upload (Must be rejected with HTTP 400)
    # -------------------------------------------------------------
    marksheet_lines = [
        "STATEMENT OF MARKS",
        "Semester Grade Report - Fall 2025",
        "Subject Code: CS101 - Operating Systems - Marks Obtained: 85 - Maximum Marks: 100",
        "Subject Code: CS102 - Database Systems - Marks Obtained: 90 - Maximum Marks: 100",
        "Tabulation Sheet Roll No: 45678"
    ]
    marksheet_pdf = make_pdf(marksheet_lines)
    files = {"file": ("marksheet.pdf", marksheet_pdf, "application/pdf")}
    res_ms = requests.post(f"{BASE_URL}/student/resume/upload", files=files, headers=headers)
    print(f"[TEST 3] Marksheet PDF Upload Response: HTTP {res_ms.status_code} - {res_ms.json()}")
    assert res_ms.status_code == 400
    print("[TEST 3 PASS] Marksheet correctly rejected (HTTP 400).")

    # -------------------------------------------------------------
    # TEST 4: Certificate of Completion PDF (Must be rejected with HTTP 400)
    # -------------------------------------------------------------
    cert_lines = [
        "CERTIFICATE OF COMPLETION",
        "This is to certify that John Doe has successfully completed",
        "the 40-hour Advanced Cloud Computing Workshop.",
        "Course Completion Certificate ID: CERT-987654"
    ]
    cert_pdf = make_pdf(cert_lines)
    files = {"file": ("certificate.pdf", cert_pdf, "application/pdf")}
    res_cert = requests.post(f"{BASE_URL}/student/resume/upload", files=files, headers=headers)
    print(f"[TEST 4] Certificate PDF Upload Response: HTTP {res_cert.status_code} - {res_cert.json()}")
    assert res_cert.status_code == 400
    print("[TEST 4 PASS] Certificate correctly rejected (HTTP 400).")

    # -------------------------------------------------------------
    # TEST 5: Random Unrelated Text PDF (Must be rejected with HTTP 400)
    # -------------------------------------------------------------
    random_lines = [
        "The Renaissance was a fervent period of European cultural, artistic, political and economic rebirth",
        "following the Middle Ages. Generally described as taking place from the 14th century to the 17th century,",
        "the Renaissance promoted the rediscovery of classical philosophy, literature and art."
    ]
    random_pdf = make_pdf(random_lines)
    files = {"file": ("random_article.pdf", random_pdf, "application/pdf")}
    res_rnd = requests.post(f"{BASE_URL}/student/resume/upload", files=files, headers=headers)
    print(f"[TEST 5] Random Article PDF Upload Response: HTTP {res_rnd.status_code} - {res_rnd.json()}")
    assert res_rnd.status_code == 400
    print("[TEST 5 PASS] Random Unrelated Document correctly rejected (HTTP 400).")

    # -------------------------------------------------------------
    # TEST 6: Genuine Resume PDF Upload (Must be accepted with HTTP 200 & dynamic ATS score)
    # -------------------------------------------------------------
    valid_resume_lines = [
        "Alex Johnson",
        "Email: alex.johnson@example.com | Phone: (555) 123-4567 | linkedin.com/in/alexjohnson | github.com/alexj",
        "Professional Summary: Dedicated Software Engineer specializing in Python, FastAPI, and Vue.js.",
        "Education: Bachelor of Technology in Computer Science, State University, 2020-2024. GPA: 3.8",
        "Technical Skills: Python, FastAPI, JavaScript, Vue, PostgreSQL, Docker, Git, REST API, Linux",
        "Experience & Projects:",
        "CareerPilot AI - Engineered full-stack career platform with FastAPI, Vue 3, and PostgreSQL.",
        "Automated deployment workflows using Docker and CI/CD pipelines, optimizing latency by 35%."
    ]
    resume_pdf = make_pdf(valid_resume_lines)
    files = {"file": ("Alex_Johnson_Resume.pdf", resume_pdf, "application/pdf")}
    res_valid = requests.post(f"{BASE_URL}/student/resume/upload", files=files, headers=headers)
    print(f"[TEST 6] Genuine Resume PDF Upload Response: HTTP {res_valid.status_code} - {res_valid.json()}")
    assert res_valid.status_code == 200, f"Valid resume upload failed: {res_valid.text}"
    valid_data = res_valid.json()
    ats_score = valid_data["ats_score"]
    assert 50 <= ats_score <= 98, f"Unexpected ATS score: {ats_score}"
    print(f"Computed ATS Score: {ats_score}%")
    print("[TEST 6 PASS] Valid Resume accepted (HTTP 200).")

    # -------------------------------------------------------------
    # TEST 7: GET /student/resume retrieves stored resume
    # -------------------------------------------------------------
    res_get = requests.get(f"{BASE_URL}/student/resume", headers=headers)
    assert res_get.status_code == 200
    assert res_get.json()["filename"] == "Alex_Johnson_Resume.pdf"
    assert res_get.json()["ats_score"] == ats_score
    print(f"[TEST 7 PASS] GET /student/resume returned stored resume (Score: {ats_score}%).")

    # -------------------------------------------------------------
    # TEST 8: Valid DOCX Resume Upload
    # -------------------------------------------------------------
    docx_bytes = make_docx(valid_resume_lines)
    files_docx = {"file": ("Alex_Johnson_Resume.docx", docx_bytes, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    res_docx = requests.post(f"{BASE_URL}/student/resume/upload", files=files_docx, headers=headers)
    assert res_docx.status_code == 200, f"DOCX resume upload failed: {res_docx.text}"
    print(f"[TEST 8 PASS] Valid DOCX Resume accepted (HTTP 200, Score: {res_docx.json()['ats_score']}%).")

    print("=" * 60)
    print("ALL RESUME VALIDATION & PERSISTENCE TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
