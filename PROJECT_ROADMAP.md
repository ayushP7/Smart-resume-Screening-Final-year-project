# Smart Resume Screening & Job Recommendation System
## Project Roadmap and Architectural Overview

### 1. Project Objective
The goal of this project is to build a professional, enterprise-grade SaaS application that leverages AI-driven parsing to help candidates bridge the gap between their resumes and modern ATS (Applicant Tracking Systems).

---

### 2. Technology Stack
- **Backend Framework**: Django 6.0 (High-security Python Web Framework)
- **Frontend Architecture**: Traditional HTML5 / Vanilla CSS3 (Custom Design System)
- **UI Components**: FontAwesome 6 (Pro Icons), Google Fonts (Inter/Outfit)
- **Data Persistence**: SQLite3 (Development) / PostgreSQL (Ready for Production)
- **Parsing Libraries**: PyPDF2 (PDF Extraction), python-docx (Word Processing)
- **Deployment Stack**: WhiteNoise (Static serving), Gunicorn (App Server), Render/Railway (Hosting)

---

### 3. Core Architecture
The project is structured into modular components to ensure scalability:

#### A. The Parser Engine (`core/utils/parser.py`)
Dissects uploaded resumes to extract:
- **Technical Skills**: Cross-referenced against a pool of 150+ tech terms.
- **Personal Info**: Email, Phone, and Professional Links (LinkedIn/GitHub).
- **ATS Scoring**: A strict metric-based score (0-100) that evaluates word count, skill density, and quantifiable impact.

#### B. The Weighted JD Matcher (`core/utils/jd_matcher.py`)
A sophisticated scoring engine that evaluates compatibility using six distinct factors:
1. Technical Skills (40 pts)
2. Soft Skills (15 pts)
3. Keyword density (15 pts)
4. Experience Level (15 pts)
5. Education Level (10 pts)
6. Domain Context (5 pts)

#### C. Smart Recommender (`core/utils/job_recommender.py`)
Generates real-time opportunity feeds from **LinkedIn** and **Naukri**. It features a balanced mix of Tech Giants (MNCs) and fast-growing Startups.

---

### 4. Implementation Roadmap

#### Phase 1: Foundation & Identity
- Initialized Django project and core application.
- Established a **Themed Design System** (CSS variables for Light/Dark mode).
- Built a Cinematic Welcome Overlay for premium user experience.

#### Phase 2: Resume Intelligence
- Developed the PDF/Docx parser.
- Implemented the ATS Scoring algorithm.
- Created the Resume Analysis Dashboard with dynamic SVG score rings.

#### Phase 3: Compatibility Engine
- Built the JD Matcher portal.
- Developed the multi-factor weighted breakdown logic.
- Implemented "Leveling" UI to ensure Step 1 and Step 2 panels are perfectly symmetrical.

#### Phase 4: Job Market Integration
- Integrated real-time job fetching via **Arbeitnow API** (Global/Remote).
- Implemented **Adzuna API** support for targeted Indian market opportunities.
- Developed high-precision **Platform-Native Search Links** for LinkedIn and Naukri.
- Enabled "Active Job" filtering (7-day max age) for maximum relevance.


#### Phase 5: SaaS Polish & Deployment
- Finalized high-visibility 2px borders for Light Theme.
- Prepared `Procfile` and `requirements.txt`.
- Configured WhiteNoise for professional asset management.

---

### 5. Future Scope
- **LLM Integration**: Replacing regex parsers with GPT/Gemini models for deeper semantic understanding.
- **Email Notifications**: Weekly job alerts based on saved resumes.
- **Portfolio Generator**: Automated generation of a web-viewable portfolio from resume data.

---
**Build By**: Antigravity AI Coding Assistant
**Project State**: Enterprise-Ready / Deployment Primed
