import io
import re
from typing import Tuple, List, Optional
from fastapi import HTTPException, status
from pypdf import PdfReader
import docx

# --------------------------------------------------------------------------
# Disqualification patterns (Non-resume documents)
# --------------------------------------------------------------------------
IDENTITY_DISQUALIFIERS = [
    r"\bunique\s+identification\s+authority\s+of\s+india\b",
    r"\buidai\b",
    r"\baadhaar\b",
    r"\baadhar\b",
    r"\badhaar\b",
    r"\be-aadhaar\b",
    r"\beaadhaar\b",
    r"\bmasked\s+aadhaar\b",
    r"\bmera\s+aadhaar\b",
    r"\bmy\s+aadhaar\b",
    r"\benrollment\s+no\b",
    r"\benrolment\s+no\b",
    r"\belectoral\s+photo\s+identity\s+card\b",
    r"\belection\s+commission\s+of\s+india\b",
    r"\bepic\s+no\b",
    r"\bvoter\s+id\b",
    r"\bvoter\s+card\b",
    r"\bincome\s+tax\s+department\b",
    r"\bpermanent\s+account\s+number\b",
    r"\bgovernment\s+of\s+india\b",
    r"\bbharat\s+sarkar\b",
    r"\bdriving\s+licen[sc]e\b",
    r"\brepublic\s+of\s+india\b",
    r"\bsocial\s+security\s+administration\b",
    r"\bpassport\s+india\b",
    r"\bindian\s+passport\b",
    r"\bration\s+card\b",
    r"\bhelp@uidai\.gov\.in\b",
    r"\buidai\.gov\.in\b"
]

FINANCIAL_DISQUALIFIERS = [
    r"\btax\s+invoice\b",
    r"\binvoice\s+(?:no|number|date|amount)\b",
    r"\bbill\s+to\b",
    r"\bbilled\s+to\b",
    r"\bship\s+to\b",
    r"\bgstin\b",
    r"\bbank\s+statement\b",
    r"\baccount\s+statement\b",
    r"\bifsc\s+code\b",
    r"\bcredit\s+balance\b",
    r"\bdebit\s+balance\b",
    r"\btransaction\s+details\b",
    r"\bpayment\s+receipt\b",
    r"\bamount\s+due\b",
    r"\bdue\s+date\b",
    r"\btotal\s+payable\b",
    r"\belectricity\s+bill\b",
    r"\bwater\s+bill\b",
    r"\butility\s+bill\b",
    r"\bsalary\s+slip\b",
    r"\bpayslip\b",
    r"\bpay\s+slip\b"
]

CERTIFICATE_DISQUALIFIERS = [
    r"\bcertificate\s+of\s+completion\b",
    r"\bthis\s+is\s+to\s+certify\s+that\b",
    r"\bhas\s+successfully\s+completed\b",
    r"\bcertificate\s+of\s+achievement\b",
    r"\bcertificate\s+of\s+appreciation\b",
    r"\bcertificate\s+of\s+participation\b",
    r"\bis\s+hereby\s+awarded\s+to\b",
    r"\bcourse\s+completion\s+certificate\b",
    r"\bbonafide\s+certificate\b",
    r"\bcharacter\s+certificate\b",
    r"\bmigration\s+certificate\b",
    r"\btransfer\s+certificate\b",
    r"\bprovisional\s+certificate\b"
]

MARKSHEET_DISQUALIFIERS = [
    r"\bstatement\s+of\s+marks\b",
    r"\bmark\s*sheet\b",
    r"\bsemester\s+grade\s+report\b",
    r"\btabulation\s+sheet\b",
    r"\bhall\s+ticket\b",
    r"\badmit\s+card\b",
    r"\bsubject\s+code\b",
    r"\bmarks\s+obtained\b",
    r"\bmaximum\s+marks\b",
    r"\binternal\s+marks\b",
    r"\bexternal\s+marks\b"
]

ALL_DISQUALIFIER_PATTERNS = (
    IDENTITY_DISQUALIFIERS + 
    FINANCIAL_DISQUALIFIERS + 
    CERTIFICATE_DISQUALIFIERS + 
    MARKSHEET_DISQUALIFIERS
)

# --------------------------------------------------------------------------
# Positive Resume Structural Signals
# --------------------------------------------------------------------------
RESUME_SECTION_PATTERNS = [
    (r"\b(?:education|academic\s+background|academics|qualifications|scholastic)\b", "education"),
    (r"\b(?:experience|work\s+experience|employment|work\s+history|internship|professional\s+experience)\b", "experience"),
    (r"\b(?:skills|technical\s+skills|core\s+competencies|technologies|tools|programming\s+languages|expertise)\b", "skills"),
    (r"\b(?:projects|academic\s+projects|key\s+projects|personal\s+projects|portfolio)\b", "projects"),
    (r"\b(?:summary|professional\s+summary|profile\s+summary|career\s+objective|about\s+me|executive\s+summary|resume\s+summary)\b", "summary"),
    (r"\b(?:certifications|achievements|honors|publications|extracurricular)\b", "certifications"),
    (r"\b(?:contact|email|phone|linkedin|github|portfolio)\b", "contact")
]

DEGREE_PATTERNS = [
    r"\b(?:mca|b\.?tech|b\.?e\.?|b\.?sc|m\.?sc|m\.?tech|bca|bachelor|bachelors|master|masters|ph\.?d|diploma|degree|student|undergraduate|postgraduate)\b"
]

CONTACT_PATTERNS = [
    r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", # Email
    r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", # Phone
    r"(?:linkedin\.com\/in\/|github\.com\/)[a-zA-Z0-9_-]+" # Professional Profiles
]

ACTION_VERBS = [
    "developed", "built", "designed", "implemented", "created", "engineered",
    "optimized", "managed", "led", "architected", "deployed", "analyzed",
    "maintained", "collaborated", "automated", "integrated", "configured"
]

TECH_KEYWORDS = [
    "python", "java", "c++", "c#", "javascript", "typescript", "html", "css",
    "fastapi", "django", "flask", "react", "vue", "angular", "node", "express",
    "sql", "postgresql", "mysql", "mongodb", "sqlite", "redis", "docker",
    "kubernetes", "aws", "azure", "gcp", "git", "github", "ci/cd", "rest",
    "api", "graphql", "machine learning", "data science", "pytorch", "tensorflow",
    "scikit-learn", "pandas", "numpy", "agile", "scrum", "linux"
]


def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    """Extract raw text from uploaded PDF or DOCX file bytes."""
    text = ""
    lower_name = filename.lower()

    if lower_name.endswith(".pdf"):
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The uploaded document does not appear to be a valid resume/CV. Please upload your resume in PDF format."
            )
    elif lower_name.endswith(".docx"):
        try:
            doc = docx.Document(io.BytesIO(file_bytes))
            for p in doc.paragraphs:
                if p.text:
                    text += p.text + "\n"
            for table in doc.tables:
                for row in table.rows:
                    row_text = " ".join(c.text.strip() for c in row.cells if c.text.strip())
                    if row_text:
                        text += row_text + "\n"
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The uploaded document does not appear to be a valid resume/CV. Please upload your resume in PDF format."
            )
    elif lower_name.endswith(".doc"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Legacy .doc format is not supported. Please upload a standard .pdf or .docx document."
        )
    else:
        try:
            text = file_bytes.decode("utf-8", errors="ignore")
        except Exception:
            text = ""

    return text.strip()


def validate_resume_text(text: str) -> Tuple[bool, str]:
    """
    Validate whether the given text corresponds to a genuine Resume/CV.
    Rejects identity docs (Aadhaar, IDs), invoices, marksheets, certificates, and generic non-resumes.
    """
    if not text or len(text.strip()) < 15:
        return False, "The uploaded document does not appear to be a valid resume/CV. Please upload your resume in PDF format."

    lower_text = text.lower()

    # 1. Check for negative disqualifiers (Aadhaar, IDs, Invoices, Certificates, Marksheets)
    for pattern in ALL_DISQUALIFIER_PATTERNS:
        if re.search(pattern, lower_text, re.IGNORECASE):
            return False, "The uploaded document does not appear to be a valid resume/CV. Please upload your resume in PDF format."

    # 2. Check detected resume sections
    matched_sections = set()
    for pattern, section_name in RESUME_SECTION_PATTERNS:
        if re.search(pattern, lower_text, re.IGNORECASE):
            matched_sections.add(section_name)

    # 3. Check contact signals
    has_contact = any(re.search(cp, text, re.IGNORECASE) for cp in CONTACT_PATTERNS)

    # 4. Check education / degree signals
    has_degree = any(re.search(dp, lower_text, re.IGNORECASE) for dp in DEGREE_PATTERNS)

    # 5. Check technical keyword count
    tech_count = sum(1 for kw in TECH_KEYWORDS if re.search(r"\b" + re.escape(kw) + r"\b", lower_text))

    # 6. Check resume intent keyword (e.g. "resume", "cv", "curriculum vitae")
    has_resume_word = bool(re.search(r"\b(?:resume|cv|curriculum\s+vitae)\b", lower_text))

    is_valid = (
        len(matched_sections) >= 2 or
        (has_resume_word and (has_degree or "summary" in matched_sections or tech_count >= 1)) or
        (len(matched_sections) >= 1 and (has_degree or has_contact or tech_count >= 1)) or
        (has_degree and tech_count >= 2)
    )

    if not is_valid:
        return False, "The uploaded document does not appear to be a valid resume/CV. Please upload your resume in PDF format."

    return True, ""


def calculate_ats_score(
    text: str,
    user_full_name: Optional[str] = None,
    profile_skills_count: int = 0,
    profile_edu_count: int = 0
) -> Tuple[int, str]:
    """
    Calculate a realistic, dynamic ATS score (0-100) based on extracted content and student profile alignment.
    Score breakdown:
    - Base valid structure: 45 pts
    - Section Completeness: up to 20 pts
    - Technical Keywords & Skills: up to 20 pts
    - Action Verbs & Project Impact: up to 10 pts
    - Education & Credentials: up to 10 pts
    - Contact Information: up to 5 pts
    """
    lower_text = text.lower()
    score = 45 # Base score for an authenticated, validated resume

    # 1. Section Completeness (up to 20 pts)
    if re.search(r"\b(?:education|academic|academics|qualifications)\b", lower_text) or profile_edu_count > 0:
        score += 5
    if re.search(r"\b(?:experience|work\s+experience|internship|projects|portfolio)\b", lower_text):
        score += 5
    if re.search(r"\b(?:skills|technical\s+skills|technologies|tools|languages)\b", lower_text) or profile_skills_count > 0:
        score += 5
    if re.search(r"\b(?:summary|objective|about|profile|resume)\b", lower_text):
        score += 5

    # 2. Technical Skills & Keywords (up to 20 pts)
    matched_techs = [kw for kw in TECH_KEYWORDS if re.search(r"\b" + re.escape(kw) + r"\b", lower_text)]
    tech_score = min(20, (len(matched_techs) * 3) + (profile_skills_count * 2))
    score += tech_score

    # 3. Action Verbs & Impact (up to 10 pts)
    matched_actions = [v for v in ACTION_VERBS if re.search(r"\b" + re.escape(v) + r"\b", lower_text)]
    action_score = min(7, len(matched_actions) * 2)
    has_metrics = bool(re.search(r"\b\d+%\b|\b\d+\s*(?:k|ms|s|users|requests|gpa)\b", lower_text))
    if has_metrics:
        action_score += 3
    score += action_score

    # 4. Education & Credentials (up to 10 pts)
    if any(re.search(dp, lower_text) for dp in DEGREE_PATTERNS) or profile_edu_count > 0:
        score += 7
    if re.search(r"\b(?:gpa|cgpa|percentage|honors|magna|cum\s+laude)\b", lower_text):
        score += 3

    # 5. Contact Information (up to 5 pts)
    if re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text):
        score += 2
    if re.search(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text):
        score += 1
    if re.search(r"(?:linkedin|github)\.com", lower_text):
        score += 2

    # Cap score cleanly between 50 and 98
    ats_score = max(50, min(96, score))

    # Generate a professional executive summary from content
    extracted_summary = generate_summary_from_text(text, user_full_name, matched_techs)

    return ats_score, extracted_summary


def generate_summary_from_text(
    text: str, 
    user_name: Optional[str] = None, 
    tech_skills: Optional[List[str]] = None
) -> str:
    """Extract or generate a clean executive summary from resume content."""
    summary_match = re.search(
        r"(?:summary|professional\s+summary|profile|career\s+objective)[\s:]*\n+([^\n]+(?:\n+[^\n]+){1,3})",
        text,
        re.IGNORECASE
    )
    if summary_match:
        candidate_summary = summary_match.group(1).strip()
        candidate_summary = re.sub(r"\s+", " ", candidate_summary)
        if len(candidate_summary) > 40:
            return candidate_summary[:300]

    name_str = user_name or "Candidate"
    skills_preview = ", ".join([s.title() for s in (tech_skills or [])[:5]])
    if skills_preview:
        return f"{name_str}'s parsed resume highlighting proficiency in {skills_preview}, relevant educational qualifications, and project execution experience."
    else:
        return f"{name_str}'s uploaded professional resume. Parsed technical qualifications, project work, and educational credentials."
