
import json
from typing import List, Dict, Any, Tuple

def normalize_skill(s: str) -> str:
    return s.strip().lower()

def skills_list_from_user(user) -> List[str]:
    """
    Use user's parsed_skills (string JSON) or method get_skills_list()
    """
    sk = []
    try:
        if hasattr(user, "get_skills_list"):
            sk = user.get_skills_list()
        else:
            sk = json.loads(user.parsed_skills or "[]")
    except Exception:
        sk = []
    return [normalize_skill(x) for x in sk if x]

def skills_list_from_job(job) -> List[str]:
    try:
        if hasattr(job, "get_required_skills"):
            arr = job.get_required_skills()
        else:
            arr = json.loads(job.required_skills or "[]")
    except Exception:
        arr = []
    return [normalize_skill(x) for x in arr if x]

def compute_skill_overlap(user_skills: List[str], job_skills: List[str]) -> Tuple[int, List[str]]:
    user_set = set(user_skills)
    job_set = set(job_skills)
    matched = sorted(list(user_set & job_set))
    return len(matched), matched

def compute_match_score(user, job, experience_weight=0.4) -> Dict[str, Any]:
    """
    Returns dict:
    {
      'job_id': job.id,
      'score': float (0..100),
      'matched_skills': [...],
      'total_required': int,
      'skill_score': float (0..1),
      'experience_adjustment': float (multiplier)
    }
    """
    u_sk = skills_list_from_user(user)
    j_sk = skills_list_from_job(job)

    total_required = max(1, len(j_sk))
    matched_count, matched = compute_skill_overlap(u_sk, j_sk)

    skill_ratio = matched_count / total_required

    exp_mult = 1.0
    try:
        if getattr(job, "min_experience", None) is not None and getattr(user, "experience_years", None) is not None:
            if user.experience_years < job.min_experience:
              
                exp_mult = 0.6
            else:
                exp_mult = 1.0
    except Exception:
        exp_mult = 1.0

    raw = skill_ratio * exp_mult
    score = round(raw * 100, 1)

    return {
        "job_id": getattr(job, "id", None),
        "score": score,
        "matched_skills": matched,
        "total_required": total_required,
        "skill_score": round(skill_ratio, 3),
        "experience_adjustment": exp_mult
    }

def rank_jobs_for_user(user, jobs_iterable, top_n=20):
    results = []
    for j in jobs_iterable:
        r = compute_match_score(user, j)
        r["job"] = j
        results.append(r)
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]
