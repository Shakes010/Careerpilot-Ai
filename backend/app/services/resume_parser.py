import re
import io
from typing import Dict, Any, List
import pdfplumber

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
    return text

def parse_resume_text(text: str, available_skills: List[str]) -> Dict[str, Any]:
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    
    # 1. Email extraction
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    email = email_match.group(0) if email_match else ""

    # 2. Phone extraction
    phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    phone = phone_match.group(0) if phone_match else ""

    # 3. Name heuristic (first non-empty line or near top)
    full_name = lines[0] if lines else "Candidate"
    if len(full_name.split()) > 4 or "@" in full_name:
        full_name = "Candidate"

    # 4. Education extraction
    degree_keywords = ["B.Tech", "M.Tech", "BCA", "MCA", "B.S.", "M.S.", "Bachelor", "Master", "Computer Science", "Information Technology"]
    extracted_education = []
    for line in lines:
        if any(kw.lower() in line.lower() for kw in degree_keywords):
            extracted_education.append(line)

    # 5. Skill matching against system skills table
    matched_skills = []
    text_lower = text.lower()
    for skill_name in available_skills:
        # Match whole word pattern where possible
        pattern = r'\b' + re.escape(skill_name.lower()) + r'\b'
        if re.search(pattern, text_lower):
            matched_skills.append(skill_name)

    # 6. Structured JSON output for pre-filling (does not auto-commit)
    return {
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "education": extracted_education[:3],
        "extracted_skills": matched_skills,
        "raw_text_preview": text[:500] + "..." if len(text) > 500 else text,
        "parsed_sections": {
            "summary": lines[1] if len(lines) > 1 else "",
            "skills": matched_skills,
            "education_details": extracted_education
        }
    }

def analyze_resume_quality(resume_data: Dict[str, Any]) -> Dict[str, Any]:
    score = 0
    feedback = []

    skills = resume_data.get("extracted_skills", [])
    if len(skills) >= 5:
        score += 35
        feedback.append("Good skill density (5+ relevant skills identified).")
    else:
        feedback.append(f"Low skill count ({len(skills)} skills). Add key technical skills like Python, SQL, or Web frameworks.")

    education = resume_data.get("education", [])
    if education:
        score += 25
        feedback.append("Academic education background clearly mentioned.")
    else:
        feedback.append("Missing explicit degree or university name in education section.")

    if resume_data.get("email") and resume_data.get("phone"):
        score += 20
        feedback.append("Complete contact information provided.")
    else:
        feedback.append("Missing complete contact details (email/phone).")

    raw_text = resume_data.get("raw_text_preview", "")
    if len(raw_text) > 200:
        score += 20
        feedback.append("Resume section length and formatting structure are appropriate.")

    return {
        "overall_score": min(score, 100),
        "feedback_points": feedback,
        "recommendations": [
            "Highlight evidence-backed projects for top claimed skills.",
            "Include GitHub repository links for verified code review.",
            "Quantify project achievements with metrics where possible."
        ]
    }
