"""
jd_matcher.py — Professional Multi-Factor Resume vs JD Scoring Engine
======================================================================
Scoring breakdown (total = 100):
  1. Technical Skills Match     → 40 pts  (from expanded skill pool)
  2. Soft Skills / Work Traits  → 15 pts  (leadership, communication, teamwork…)
  3. Tools & Technologies       → 15 pts  (cloud, version control, CI/CD…)
  4. Experience Level Alignment → 15 pts  (fresher / junior / mid / senior)
  5. Education Qualification    → 10 pts  (degree level match)
  6. Domain / Industry Context  →  5 pts  (data science, web dev, devops…)

Each factor contributes its weighted proportion. The final score is 0–100.
"""

import re
from collections import defaultdict

# ─────────────────────────────────────────────
# 1.  EXPANDED TECHNICAL SKILLS (150+ terms)
# ─────────────────────────────────────────────
TECH_SKILLS = {
    # Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "c", "go",
    "golang", "rust", "kotlin", "swift", "dart", "r", "scala", "perl",
    "ruby", "php", "bash", "shell scripting", "matlab", "vba",
    # Web Frontend
    "html", "css", "react", "reactjs", "react.js", "angular", "angularjs",
    "vue", "vuejs", "next.js", "nuxt", "svelte", "jquery", "bootstrap",
    "tailwind", "sass", "scss", "webpack",
    # Web Backend
    "node.js", "nodejs", "express", "expressjs", "django", "flask",
    "fastapi", "spring", "spring boot", "laravel", "rails", "asp.net",
    ".net", "servlet", "graphql", "rest api", "restful", "soap",
    # Databases
    "sql", "mysql", "postgresql", "postgres", "sqlite", "oracle",
    "mongodb", "mongoose", "redis", "cassandra", "dynamodb", "firebase",
    "elasticsearch", "neo4j", "hive", "hbase",
    # Cloud & DevOps
    "aws", "gcp", "azure", "docker", "kubernetes", "k8s", "terraform",
    "ansible", "jenkins", "github actions", "ci/cd", "linux", "unix",
    "nginx", "apache", "heroku", "vercel", "netlify",
    # ML / AI / Data
    "machine learning", "deep learning", "nlp", "natural language processing",
    "computer vision", "tensorflow", "pytorch", "keras", "scikit-learn",
    "sklearn", "pandas", "numpy", "scipy", "matplotlib", "seaborn",
    "xgboost", "lightgbm", "data analysis", "data science", "data engineering",
    "feature engineering", "model deployment", "mlops", "spark", "hadoop",
    "airflow", "etl", "power bi", "tableau", "excel",
    # Version Control & Collaboration
    "git", "github", "gitlab", "bitbucket", "svn", "jira", "confluence",
    "trello", "notion",
    # Methodologies
    "agile", "scrum", "kanban", "devops", "tdd", "bdd", "microservices",
    "design patterns", "oop", "solid", "system design",
    # Testing
    "unit testing", "integration testing", "selenium", "cypress",
    "jest", "pytest", "junit", "postman",
}

# Synonym map: normalise any of these → canonical name
SKILL_ALIASES = {
    "js": "javascript", "ts": "typescript", "py": "python",
    "react.js": "react", "reactjs": "react", "vuejs": "vue",
    "node.js": "nodejs", "node js": "nodejs", "express.js": "expressjs",
    "ml": "machine learning", "ai": "machine learning",
    "cv": "computer vision", "scikit learn": "scikit-learn", "sklearn": "scikit-learn",
    "k8s": "kubernetes", "postgres": "postgresql",
    "spring boot": "spring", "asp.net": ".net",
    "github actions": "ci/cd", "jenkins": "ci/cd",
    "gcp": "google cloud", "google cloud platform": "google cloud",
    "aws": "amazon web services",
    "natural language processing": "nlp",
}

# ─────────────────────────────────────────────
# 2.  SOFT SKILLS
# ─────────────────────────────────────────────
SOFT_SKILLS = {
    "communication", "teamwork", "team player", "collaboration", "leadership",
    "problem solving", "problem-solving", "critical thinking", "adaptability",
    "time management", "creativity", "attention to detail", "ownership",
    "self-motivated", "proactive", "fast learner", "quick learner",
    "presentation", "interpersonal", "client handling", "stakeholder management",
    "decision making", "analytical", "multitasking", "organized",
}

# ─────────────────────────────────────────────
# 3.  EDUCATION LEVEL PATTERNS
# ─────────────────────────────────────────────
EDU_LEVELS = {
    "phd": 4, "ph.d": 4, "doctorate": 4,
    "master": 3, "m.tech": 3, "m.e": 3, "mba": 3, "msc": 3, "ms": 3, "m.s": 3,
    "bachelor": 2, "b.tech": 2, "b.e": 2, "bsc": 2, "b.sc": 2, "b.e.": 2,
    "diploma": 1, "associate": 1,
}

# ─────────────────────────────────────────────
# 4.  EXPERIENCE LEVEL PATTERNS
# ─────────────────────────────────────────────
# Ordered: higher wins
EXP_LEVELS = [
    ("senior",   ["senior", "lead", "principal", "architect", "head of", "vp", "director",
                  r"\b[5-9]\+?\s*years?\b", r"\b[1-9][0-9]\+?\s*years?\b"]),
    ("mid",      ["mid-level", "mid level", r"\b[3-4]\+?\s*years?\b"]),
    ("junior",   ["junior", "associate", r"\b[1-2]\+?\s*years?\b", "1 year"]),
    ("fresher",  ["fresher", "fresh graduate", "entry.?level", "0.?year", "intern", r"\bno experience\b"]),
]


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def _normalise_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text.lower().strip())


def _apply_aliases(token: str) -> str:
    return SKILL_ALIASES.get(token, token)


def _extract_skill_set(text: str, skill_pool: set) -> set:
    """
    Extract skills from `text` that are present in `skill_pool`.
    Handles multi-word skills and alias normalisation.
    """
    t = _normalise_text(text)
    found = set()
    for skill in skill_pool:
        # whole-word / phrase match
        pattern = r'(?<![a-z])' + re.escape(skill) + r'(?![a-z])'
        if re.search(pattern, t):
            found.add(_apply_aliases(skill))

    # Also check aliases against text
    for alias, canonical in SKILL_ALIASES.items():
        if canonical in skill_pool or alias in skill_pool:
            pattern = r'(?<![a-z])' + re.escape(alias) + r'(?![a-z])'
            if re.search(pattern, t):
                found.add(canonical)
    return found


def _extract_soft_skills(text: str) -> set:
    return _extract_skill_set(text, SOFT_SKILLS)


def _detect_experience_level(text: str) -> str:
    t = _normalise_text(text)
    for level, patterns in EXP_LEVELS:
        for p in patterns:
            if re.search(p, t):
                return level
    return "mid"


def _detect_education_level(text: str) -> int:
    """Returns numeric education level (0–4)."""
    t = _normalise_text(text)
    best = 0
    for keyword, level in EDU_LEVELS.items():
        if keyword in t and level > best:
            best = level
    return best


def _extract_ngrams(text: str, n: int) -> set:
    """Extract word n-grams from text for broader domain matching."""
    words = re.findall(r'[a-z]+', text.lower())
    return {' '.join(words[i:i+n]) for i in range(len(words) - n + 1)}


# ─────────────────────────────────────────────
# MAIN FUNCTION
# ─────────────────────────────────────────────
def match_resume_to_jd(resume_skills: list, jd_text: str, resume_full_text: str = "") -> dict:
    """
    Multi-factor scoring:
      Factor 1 – Technical Skills    40%
      Factor 2 – Soft Skills         15%
      Factor 3 – Tools & Keywords    15%
      Factor 4 – Experience Level    15%
      Factor 5 – Education Level     10%
      Factor 6 – Domain Context       5%
    Returns 0–100 score.
    """

    # ── Normalise inputs ──────────────────────
    jd_lower     = _normalise_text(jd_text)
    resume_lower = _normalise_text(resume_full_text) if resume_full_text else ""
    resume_set   = {_apply_aliases(s.lower()) for s in resume_skills}

    # ── Factor 1: Technical Skills (40 pts) ──
    jd_tech   = _extract_skill_set(jd_text, TECH_SKILLS)
    res_tech  = _extract_skill_set(resume_full_text, TECH_SKILLS) if resume_full_text else resume_set

    if jd_tech:
        matched_tech = jd_tech & res_tech
        missing_tech = jd_tech - res_tech
        f1_score = (len(matched_tech) / len(jd_tech)) * 40
    else:
        # No extractable tech skills — give partial credit for resume skills
        matched_tech = set()
        missing_tech = set()
        f1_score = 20  # neutral if JD has no detectable tech skills

    # ── Factor 2: Soft Skills (15 pts) ───────
    jd_soft  = _extract_soft_skills(jd_text)
    res_soft = _extract_soft_skills(resume_full_text) if resume_full_text else set()
    if jd_soft:
        matched_soft = jd_soft & res_soft
        f2_score = (len(matched_soft) / len(jd_soft)) * 15
        matched_soft_list = sorted(matched_soft)
        missing_soft_list = sorted(jd_soft - res_soft)
    else:
        f2_score = 7.5          # neutral — JD mentions no soft skills
        matched_soft_list = []
        missing_soft_list = []

    # ── Factor 3: Tools & Domain Keywords (15 pts) ──
    # Use important JD unigrams+bigrams that appear in resume
    jd_unigrams  = set(re.findall(r'\b[a-z]{3,}\b', jd_lower))
    res_unigrams = set(re.findall(r'\b[a-z]{3,}\b', resume_lower)) if resume_lower else set()
    # Remove common stop words
    STOP = {'and','the','with','for','are','this','that','have','from','your',
            'will','you','our','all','but','their','also','what','who','can',
            'not','more','been','use','its','which','has','into','they','out',
            'how','one','over','such','must','may','should','any','other',
            'able','both','each','then','than','very','well','include','including',
            'experience','required','skills','knowledge','working','minimum',
            'years','year','etc','via','per','within','based','across'}
    jd_kw  = jd_unigrams  - STOP
    res_kw = res_unigrams - STOP
    if jd_kw:
        overlap_kw = jd_kw & res_kw
        f3_score = min((len(overlap_kw) / len(jd_kw)) * 15, 15)  # cap at 15
    else:
        f3_score = 7.5

    # ── Factor 4: Experience Level (15 pts) ──
    jd_level  = _detect_experience_level(jd_text)
    res_level = _detect_experience_level(resume_full_text) if resume_full_text else "mid"

    level_order = {"fresher": 0, "junior": 1, "mid": 2, "senior": 3}
    jd_lvl_n  = level_order.get(jd_level, 2)
    res_lvl_n = level_order.get(res_level, 2)
    diff = abs(jd_lvl_n - res_lvl_n)
    if diff == 0:
        f4_score = 15       # perfect match
    elif diff == 1:
        f4_score = 10       # one level off (e.g. mid vs junior)
    elif diff == 2:
        f4_score = 5        # two levels off
    else:
        f4_score = 2        # three levels off (fresher applying for senior)

    # ── Factor 5: Education Level (10 pts) ───
    jd_edu  = _detect_education_level(jd_text)
    res_edu = _detect_education_level(resume_full_text) if resume_full_text else 0

    if jd_edu == 0:
        f5_score = 10       # JD doesn't specify education → full marks
    elif res_edu >= jd_edu:
        f5_score = 10       # meets or exceeds requirement
    elif res_edu == jd_edu - 1:
        f5_score = 6        # one level below
    elif res_edu == jd_edu - 2:
        f5_score = 3
    else:
        f5_score = 0

    # ── Factor 6: Domain Context (5 pts) ─────
    DOMAINS = {
        "data science":   ["data science", "data scientist", "analytics", "ml engineer"],
        "web development":["web development", "frontend", "backend", "full stack", "fullstack"],
        "devops":         ["devops", "cloud engineer", "infra", "sre", "reliability"],
        "mobile":         ["mobile", "android", "ios", "flutter", "react native"],
        "ai/ml":          ["artificial intelligence", "machine learning engineer", "ai engineer"],
        "security":       ["cybersecurity", "security engineer", "penetration", "infosec"],
    }
    f6_score = 0
    for domain, markers in DOMAINS.items():
        jd_in_domain  = any(m in jd_lower for m in markers)
        res_in_domain = any(m in resume_lower for m in markers) if resume_lower else False
        if jd_in_domain and res_in_domain:
            f6_score = 5
            break
        elif jd_in_domain and not res_in_domain:
            f6_score = 0
            break
    else:
        f6_score = 2.5      # General/unknown domain — neutral

    # ── Aggregate ─────────────────────────────
    raw = f1_score + f2_score + f3_score + f4_score + f5_score + f6_score
    final_score = min(100, max(0, round(raw)))

    # ── Build detailed output ─────────────────
    all_matched = sorted(matched_tech | set(matched_soft_list))
    all_missing = sorted(missing_tech | set(missing_soft_list))
    jd_skills_found = sorted(jd_tech | jd_soft)

    breakdown = {
        "technical_skills":  round(f1_score, 1),
        "soft_skills":       round(f2_score, 1),
        "keyword_match":     round(f3_score, 1),
        "experience_level":  round(f4_score, 1),
        "education_level":   round(f5_score, 1),
        "domain_context":    round(f6_score, 1),
    }

    return {
        "score":          final_score,
        "matched":        all_matched,
        "missing":        all_missing,
        "jd_skills_found": jd_skills_found,
        "jd_level":       jd_level,
        "resume_level":   res_level,
        "breakdown":      breakdown,
    }
