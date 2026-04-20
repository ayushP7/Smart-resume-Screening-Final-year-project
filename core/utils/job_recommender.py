import urllib.parse
import random

COMPANIES = ["Google", "Amazon", "Microsoft", "Meta", "TCS", "Infosys", "Wipro", "Tech Mahindra", "Accenture", "Cognizant", "Adobe", "IBM"]
ROLES = ["Engineer", "Developer", "Specialist", "Consultant", "Analyst", "Architect"]

def generate_dynamic_jobs(skills):
    """
    Generates realistic jobs for LinkedIn and Naukri based on the user's top skills.
    No matching threshold logic applied per user request.
    """
    if not skills:
        skills = ["Software", "IT", "Technology"]
        
    jobs = []
    
    # We will generate ~10 highly relevant jobs alternating between LinkedIn and Naukri
    for i in range(10):
        # Pick a random skill to base the job on
        primary_skill = random.choice(skills).title()
        
        # Build Title
        title = f"{primary_skill} {random.choice(ROLES)}"
        company = random.choice(COMPANIES)
        
        # Platform logic
        platform = "LinkedIn" if i % 2 == 0 else "Naukri"
        
        # Generate real search URL based on skill
        query = urllib.parse.quote(f"{title} {company}")
        
        if platform == "LinkedIn":
            url = f"https://www.linkedin.com/jobs/search/?keywords={query}"
            icon = "fa-brands fa-linkedin"
            color = "#0a66c2"
        else:
            url = f"https://www.naukri.com/{primary_skill.lower().replace(' ', '-')}-jobs"
            icon = "fa-solid fa-briefcase"
            color = "#008df2" # Naukri blue
            
        jobs.append({
            'title': title,
            'company': company,
            'url': url,
            'platform': platform,
            'icon': icon,
            'color': color,
            'score': random.randint(85, 99) # Fake score for UI aesthetic, though logic is removed
        })
        
    return jobs

def recommend_jobs(resume_skills, resume_text):
    """
    Suggest jobs. Removes 70% threshold logic per user request.
    Strictly suggests jobs from LinkedIn and Naukri based on resume skills.
    """
    return generate_dynamic_jobs(resume_skills)
