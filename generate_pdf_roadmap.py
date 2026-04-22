from fpdf import FPDF
import datetime

class RoadmapPDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 20)
        self.set_text_color(168, 85, 247) # Theme Purple
        self.cell(0, 20, 'Project Roadmap & Architecture Guide', border=False, align='C')
        self.ln(25)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(169, 169, 169)
        self.cell(0, 10, f'Page {self.page_no()} | Smart Resume Screening Project | Generated on {datetime.datetime.now().strftime("%Y-%m-%d")}', align='C')

    def chapter_title(self, label):
        self.set_font('helvetica', 'B', 14)
        self.set_text_color(30, 41, 59) # Slate 800
        self.cell(0, 10, label, align='L')
        self.ln(8)
        self.line(self.get_x(), self.get_y(), 200, self.get_y())
        self.ln(5)

    def chapter_body(self, text):
        self.set_font('helvetica', '', 11)
        self.set_text_color(71, 85, 105) # Slate 600
        self.multi_cell(0, 6, text)
        self.ln()

def generate():
    pdf = RoadmapPDF()
    pdf.add_page()

    # 1. Overview
    pdf.chapter_title('1. Project Overview')
    pdf.chapter_body(
        "Smart Resume Screening is an enterprise-grade SaaS application designed to empower job seekers. "
        "It provides a neural parsing engine that dissects resume structures, identifies missing technical competencies, "
        "and suggests live job opportunities with high-precision matching logic."
    )

    # 2. Tech Stack
    pdf.chapter_title('2. Technology Stack')
    pdf.chapter_body(
        "- Backend: Django 6.0 (High-security Python framework)\n"
        "- Frontend: HTML5 / Vanilla CSS3 with Theme Persistence Engine\n"
        "- UI: FontAwesome 6 Pro Icons and Google Fonts (Inter/Outfit)\n"
        "- Libraries: PyPDF2, python-docx, WhiteNoise, Gunicorn\n"
        "- Persistence: Managed SQLite/PostgreSQL Ready"
    )

    # 3. Component Architecture
    pdf.chapter_title('3. Component Architecture')
    pdf.chapter_body(
        "Parser Engine (parser.py): Dissects documents into structured data using regex and text extraction.\n\n"
        "JD Matcher (jd_matcher.py): A multi-factor scoring engine evaluating Technical Skills (40%), Soft Skills (15%), "
        "Keywords (15%), Experience (15%), Education (10%), and Domain (5%).\n\n"
        "Smart Recommender (job_recommender.py): A dual-path aggregator providing 30+ opportunities from LinkedIn "
        "and Naukri, balancing established MNCs and high-growth Startups."
    )

    # 4. Roadmap (5 Phases)
    pdf.chapter_title('4. Implementation Roadmap')
    pdf.chapter_body(
        "Phase 1: Foundation & SaaS Identity (Authentication, UI Variables, Splash Screens)\n\n"
        "Phase 2: Resume Intelligence (PDF/Docx Parsing, ATS Metric Scoring, Analysis Dashboard)\n\n"
        "Phase 3: Compatibility Engine (JD Matcher Portal, Weighted Logic, Symmetrical Grid UI)\n\n"
        "Phase 4: Market Integration (30x Job Expansion, Startup vs MNC logic, Platform-Specific URLs)\n\n"
        "Phase 5: SaaS Polish & Deployment (2px Border Enforcements, Procfile, Static Management)"
    )

    # 5. UI Philosophy
    pdf.chapter_title('5. Design & UI Philosophy')
    pdf.chapter_body(
        "The project follows a 'Cinematic SaaS' aesthetic. In Dark Mode, it uses semi-transparent glassmorphism "
        "to maintain depth. In Light Mode, it enforces high-contrast 2px solid accents to ensure accessibility and "
        "professional clarity. The UI is alive with micro-animations and color-coded step indicators."
    )

    pdf.output('Project_Roadmap_and_Architecture.pdf')
    print("PDF Generated Successfully: Project_Roadmap_and_Architecture.pdf")

if __name__ == "__main__":
    generate()
