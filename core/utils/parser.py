import PyPDF2
import docx
import re
import os

# Predefined list of technical skills (expanded to match jd_matcher)
TECHNICAL_SKILLS = [
    'python', 'java', 'c++', 'javascript', 'typescript', 'html', 'css', 'react', 'angular', 'vue',
    'node.js', 'express', 'django', 'flask', 'spring', 'sql', 'mysql', 'postgresql',
    'mongodb', 'aws', 'docker', 'kubernetes', 'git', 'linux', 'machine learning',
    'deep learning', 'nlp', 'data analysis', 'pandas', 'numpy', 'scipy', 'pytorch',
    'tensorflow', 'agile', 'scrum', 'rest api', 'graphql', 'c#', '.net', 'php', 'ruby'
]

def extract_text_from_pdf(file_obj):
    text = ""
    try:
        reader = PyPDF2.PdfReader(file_obj)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_text_from_docx(file_obj):
    try:
        doc = docx.Document(file_obj)
        return " ".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error reading DOCX: {e}")
        return ""

def extract_skills(text):
    text = text.lower()
    skills = set()
    for skill in TECHNICAL_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            skills.add(skill)
    return list(skills)

def extract_personal_info(text):
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    email = email_match.group(0) if email_match else "Not Found"

    phone_match = re.search(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', text)
    phone = phone_match.group(0) if phone_match else "Not Found"

    linkedin_github = bool(re.search(r'(linkedin\.com|github\.com|portfolio)', text, re.I))

    return {
        'email': email,
        'phone': phone,
        'linkedin_github': linkedin_github
    }

def extract_experience_level(text):
    text = text.lower()
    senior_patterns = r'(senior|lead|principal|architect|manager|head of|yrs of exp|years of exp|experience: [5-9]|experience: [1-9][0-9])'
    junior_patterns = r'(junior|associate|jr|entry level|staff)'
    fresher_patterns = r'(fresher|graduate|student|intern|training|certification)'

    if re.search(senior_patterns, text):
        return 'senior'
    if re.search(fresher_patterns, text):
        return 'fresher'
    if re.search(junior_patterns, text):
        return 'junior'
    
    return 'mid'

def calculate_ats_score(parsed_data):
    score = 0
    breakdown = []
    
    # 1. Contact Info (20 max)
    if parsed_data['personal_info']['email'] != "Not Found": score += 10
    else: breakdown.append("Missing Email Address (-10 points)")
        
    if parsed_data['personal_info']['phone'] != "Not Found": score += 5
    else: breakdown.append("Missing Phone Number (-5 points)")
        
    if parsed_data['personal_info']['linkedin_github']: score += 5
    else: breakdown.append("Missing LinkedIn or GitHub profile (-5 points)")
        
    # 2. Key Sections (30 max)
    if parsed_data['sections']['experience']: score += 15
    else: breakdown.append("Missing 'Experience' or 'Work History' section (-15 points)")
        
    if parsed_data['sections']['education']: score += 10
    else: breakdown.append("Missing 'Education' section (-10 points)")
        
    if parsed_data['sections']['summary']: score += 5
    else: breakdown.append("Missing 'Summary' or 'Objective' (-5 points)")

    # 3. Skills Matrix (30 points)
    skills_count = len(parsed_data['skills'])
    if skills_count >= 15: score += 30
    elif skills_count >= 8: score += 20
    elif skills_count >= 3: 
        score += 10
        breakdown.append(f"Low skill density ({skills_count} found, 8+ recommended) (-10) points")
    else: 
        breakdown.append("Critically low skill density (-30 points)")

    # 4. Quantifiable Impact & Formatting (20 points)
    impact = parsed_data['metrics']['impact_count']
    if impact >= 5: score += 15
    elif impact >= 2: 
        score += 8
        breakdown.append("Low measurable impact/numbers in descriptions (-7 points)")
    else: 
        breakdown.append("No numbers or percentages found. Add quantifiable metrics! (-15 points)")

    wc = parsed_data['metrics']['word_count']
    if 300 <= wc <= 1200: score += 5
    else: breakdown.append(f"Word count ({wc}) outside ideal ATS range of 300-1200 (-5 points)")

    return {
        "score": score,
        "breakdown": breakdown
    }

def parse_resume(file_obj, filename):
    file_obj.seek(0)
    if filename.lower().endswith('.pdf'):
        text = extract_text_from_pdf(file_obj)
    elif filename.lower().endswith('.docx'):
        text = extract_text_from_docx(file_obj)
    else:
        text = file_obj.read().decode('utf-8', errors='ignore')

    skills = extract_skills(text)
    personal_info = extract_personal_info(text)
    seniority = extract_experience_level(text)
    
    # Advanced extraction
    has_education = bool(re.search(r'\b(education|university|college|degree|bachelor|master|phd|b\.tech|b\.e)\b', text, re.I))
    has_experience = bool(re.search(r'\b(experience|employment|work history|career|professional background)\b', text, re.I))
    has_summary = bool(re.search(r'\b(summary|objective|profile|about me)\b', text, re.I))
    
    impact_matches = len(re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?%?\b|\$\d+', text))
    word_count = len(text.split())

    parsed_data = {
        'text': text,
        'skills': skills,
        'personal_info': personal_info,
        'seniority': seniority,
        'sections': {
            'education': has_education,
            'experience': has_experience,
            'summary': has_summary
        },
        'metrics': {
            'impact_count': impact_matches,
            'word_count': word_count
        }
    }
    
    # Execute strict scoring logic
    ats_results = calculate_ats_score(parsed_data)
    parsed_data['ats_score'] = ats_results['score']
    parsed_data['ats_breakdown'] = ats_results['breakdown']

    return parsed_data

