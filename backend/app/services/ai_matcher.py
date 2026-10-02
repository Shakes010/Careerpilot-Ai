import math
from typing import List, Dict, Any, Tuple

try:
    from sentence_transformers import SentenceTransformer, util
    model = SentenceTransformer('all-MiniLM-L6-v2')
    HAS_ST = True
except Exception:
    HAS_ST = False
    model = None

def compute_cosine_similarity(text1: str, text2: str) -> float:
    if HAS_ST and model:
        try:
            emb1 = model.encode(text1, convert_to_tensor=True)
            emb2 = model.encode(text2, convert_to_tensor=True)
            sim = float(util.cos_sim(emb1, emb2)[0][0])
            return max(0.0, min(1.0, sim))
        except Exception:
            pass

    # Fallback term frequency cosine similarity
    words1 = set(text1.lower().replace(",", " ").split())
    words2 = set(text2.lower().replace(",", " ").split())
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    sim = len(intersection) / math.sqrt(len(words1) * len(words2))
    return round(sim, 2)

def match_skills_against_job(
    student_skills: List[Dict[str, Any]], # [{skill_name, trust_score, badge_tier}]
    job_required_skills: List[str] # ["Python", "FastAPI", ...]
) -> Tuple[int, List[Dict[str, Any]], List[str]]:
    if not job_required_skills:
        return 80, [], []

    matched_skills = []
    missing_skills = []

    student_skill_dict = {s["skill_name"].lower(): s for s in student_skills}

    matched_weights = 0
    total_required = len(job_required_skills)

    for req in job_required_skills:
        req_lower = req.lower()
        if req_lower in student_skill_dict:
            sk_info = student_skill_dict[req_lower]
            matched_skills.append({
                "skill_name": req,
                "badge_tier": sk_info.get("badge_tier", "declared"),
                "trust_score": sk_info.get("trust_score", 20)
            })
            # Verified badges yield full weight, declared yield partial weight
            tier_mult = 1.0 if sk_info.get("badge_tier") == "verified" else 0.65
            score_factor = (sk_info.get("trust_score", 20) / 100.0) * tier_mult
            matched_weights += score_factor
        else:
            # Check fuzzy / semantic similarity
            best_sim = 0.0
            best_match = None
            for s_name, sk_info in student_skill_dict.items():
                sim = compute_cosine_similarity(req, s_name)
                if sim > best_sim and sim > 0.6:
                    best_sim = sim
                    best_match = (req, sk_info)
            
            if best_match:
                sk_info = best_match[1]
                matched_skills.append({
                    "skill_name": req,
                    "badge_tier": sk_info.get("badge_tier", "declared"),
                    "trust_score": sk_info.get("trust_score", 20)
                })
                matched_weights += 0.5
            else:
                missing_skills.append(req)

    overall_score = int(min(100, max(0, (matched_weights / total_required) * 100))) if total_required > 0 else 50
    return overall_score, matched_skills, missing_skills
