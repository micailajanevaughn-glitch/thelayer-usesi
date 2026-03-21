import os, requests
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# Download fonts
FONT_DIR = "/tmp/fonts"
os.makedirs(FONT_DIR, exist_ok=True)

fonts = {
    "Inter-Regular": "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf",
}

# Use built-in Helvetica as fallback — clean and professional
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Download Inter
inter_url = "https://fonts.gstatic.com/s/inter/v13/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuLyfAZ9hiJ-Ek-_EeA.woff2"
inter_regular_url = "https://fonts.gstatic.com/s/inter/v13/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuLyfAZ9hiA.woff2"

# Use TTF from a reliable source
def download_font(url, path):
    r = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)

# Download Inter TTF
inter_ttf = "/tmp/fonts/Inter-Regular.ttf"
inter_bold_ttf = "/tmp/fonts/Inter-Bold.ttf"

download_font("https://github.com/rsms/inter/releases/download/v3.19/Inter-3.19.zip", "/tmp/inter.zip")

import zipfile
try:
    with zipfile.ZipFile("/tmp/inter.zip", 'r') as z:
        for name in z.namelist():
            if 'Inter-Regular.ttf' in name:
                with z.open(name) as src, open(inter_ttf, 'wb') as dst:
                    dst.write(src.read())
            if 'Inter-Bold.ttf' in name:
                with z.open(name) as src, open(inter_bold_ttf, 'wb') as dst:
                    dst.write(src.read())
except:
    pass

# Fallback: download directly
if not os.path.exists(inter_ttf) or os.path.getsize(inter_ttf) < 1000:
    download_font("https://fonts.gstatic.com/s/inter/v12/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuLyfAZBiA.ttf", inter_ttf)
if not os.path.exists(inter_bold_ttf) or os.path.getsize(inter_bold_ttf) < 1000:
    download_font("https://fonts.gstatic.com/s/inter/v12/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuI-pBiA.ttf", inter_bold_ttf)

try:
    pdfmetrics.registerFont(TTFont('Inter', inter_ttf))
    pdfmetrics.registerFont(TTFont('Inter-Bold', inter_bold_ttf))
    FONT = 'Inter'
    FONT_BOLD = 'Inter-Bold'
except:
    FONT = 'Helvetica'
    FONT_BOLD = 'Helvetica-Bold'

print(f"Using font: {FONT}")

TEAL = colors.HexColor('#4ecdc4')
BLACK = colors.HexColor('#1a1a1a')
MUTED = colors.HexColor('#555555')
WHITE = colors.white

OUTPUT = "/home/user/workspace/Micaila-Vaughn-Resume.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    leftMargin=0.65*inch,
    rightMargin=0.65*inch,
    topMargin=0.42*inch,
    bottomMargin=0.42*inch,
    title="Micaila Vaughn Resume",
    author="Perplexity Computer"
)

story = []

# ── STYLES ──
def style(name, font=FONT, size=10, leading=14, color=BLACK, spaceBefore=0, spaceAfter=0, leftIndent=0, bold=False, letterSpacing=0):
    return ParagraphStyle(
        name,
        fontName=FONT_BOLD if bold else font,
        fontSize=size,
        leading=leading,
        textColor=color,
        spaceBefore=spaceBefore,
        spaceAfter=spaceAfter,
        leftIndent=leftIndent,
        wordSpacing=letterSpacing,
    )

s_name = style('name', size=32, leading=36, bold=True, spaceAfter=2)
s_subtitle = style('subtitle', size=8.5, leading=12, color=MUTED, spaceAfter=4)
s_contact = style('contact', size=9, leading=13, color=MUTED, spaceAfter=0)
s_section = style('section', size=8, leading=11, color=TEAL, bold=True, spaceBefore=5, spaceAfter=2)
s_company = style('company', size=10, leading=13, color=TEAL, bold=True)
s_jobtitle = style('jobtitle', size=10, leading=13, bold=True, color=BLACK)
s_date = style('date', size=8.5, leading=12, color=MUTED)
s_location = style('location', size=8.5, leading=12, color=MUTED)
s_bullet = style('bullet', size=9, leading=13, color=BLACK, leftIndent=12, spaceAfter=2)
s_body = style('body', size=9.5, leading=14, color=BLACK)
s_edu_title = style('edu_title', size=9.5, leading=13, bold=True, color=BLACK)
s_edu_sub = style('edu_sub', size=9, leading=13, color=MUTED)
s_skill = style('skill', size=9, leading=14, color=BLACK)
s_col_header = style('col_header', size=8, leading=11, color=TEAL, bold=True, spaceAfter=4)

# ── HELPER ──
def section_rule():
    return HRFlowable(width="100%", thickness=1, color=TEAL, spaceAfter=6, spaceBefore=2)

def bullet(text):
    return Paragraph(f"— {text}", s_bullet)

def spacer(h=4):
    return Spacer(1, h)

# ══════════════════════════════════════════
# NAME + HEADER
# ══════════════════════════════════════════
story.append(Paragraph("Micaila Vaughn", s_name))
story.append(Spacer(1, 4))

subtitle_style = ParagraphStyle('sub2', fontName=FONT, fontSize=8, leading=11,
                                 textColor=MUTED, spaceAfter=6, letterSpacing=2)
story.append(Paragraph("LIGHTING INDUSTRY STRATEGY  ·  AI &amp; SYSTEMS INTEGRATION  ·  REVENUE OPERATIONS", subtitle_style))

contact_style = ParagraphStyle('con2', fontName=FONT, fontSize=9, leading=13,
                                textColor=MUTED, spaceAfter=8)
story.append(Paragraph("303.981.7338    micailajanevaughn@gmail.com    linkedin.com/in/micailavaughn", contact_style))

story.append(HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=10))

# ══════════════════════════════════════════
# PROFESSIONAL EXPERIENCE
# ══════════════════════════════════════════
story.append(Paragraph("PROFESSIONAL EXPERIENCE", s_section))
story.append(section_rule())

# ── Job entry helper — stacked layout ──
def job(date, company, location, title, bullets):
    from reportlab.platypus import KeepTogether
    # Header row: company left, date right
    header = Table(
        [[Paragraph(f'<b>{company}</b> <font color="#888888" size="8">· {location}</font>', ParagraphStyle('jh', fontName=FONT_BOLD, fontSize=10, leading=13, textColor=colors.HexColor('#1a1a1a'))),
          Paragraph(date, ParagraphStyle('dr', fontName=FONT, fontSize=8.5, leading=13, textColor=MUTED, alignment=2))]],
        colWidths=[4.8*inch, 2.0*inch]
    )
    header.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    block = [header, Paragraph(title, ParagraphStyle('jt', fontName=FONT_BOLD, fontSize=9.5, leading=13, textColor=TEAL, spaceAfter=3))]
    for b in bullets:
        block.append(bullet(b))
    block.append(Spacer(1, 8))
    story.append(KeepTogether(block))

job("Feb 2026 — Present", "Teloric", "Denver, CO", "Founder / Principal Consultant", [
    "Identified the gap between AI/BI capability and real-world operations — building systems, training frameworks, and infrastructure that deliver immediate ROI and position organizations to compete for the next generation of clients and talent",
])

job("Aug 2021 — Feb 2026", "Coronet", "Denver, CO (Remote)", "Northwest Regional Sales Manager, Western U.S. & Canada", [
    "Doubled geographic sales territory — realigned West Coast rep agency networks across 10+ markets, replacing underperforming partnerships and rebuilding coverage in Seattle, San Francisco, Portland, and Vancouver",
    "Identified institutional knowledge gap that the company's own ERP could not surface — built AI-powered onboarding, training, and rep sales systems using prompt libraries, knowledge bases, and structured workflows that teams actually adopted",
    "Replaced conventional sales calls with curated pop-up showcase events targeting lighting designers and niche specifiers — generated $3–5M in identifiable project business per cycle",
    "Rebuilt specifier relationships across the Western U.S. — converted A&D community into consistent, high-value project pipeline through sustained engagement and brand presence",
])

job("June 2019 — July 2021", "Luxxbox", "United States (Remote)", "Senior Sales Manager", [
    "Grew U.S. revenue 35% — built nationwide rep agency network, go-to-market strategy, and sales infrastructure from zero for an unknown international manufacturer entering the U.S. market",
    "Developed rep sales portal and CRM structure to support pipeline tracking and lead management at scale — systems handed off and still in use after departure",
    "Positioned brand inside the design community through targeted events and touchpoints — placed an unknown international line in front of the specifiers and reps who drive project decisions",
])

job("Jan 2018 — June 2019", "Calyx Theory", "Denver, CO — Experiential / UX Design", "Founder", [
    "Embedded with design-driven clients — Boyd, ALVA Lighting, MakeWest — to identify gaps in brand positioning, specification engagement, and market development, delivering strategies that drove new client acquisition",
    "Mapped full operational workflow for Vonmod — surfaced breakdown points across client acquisition, quoting, and production, then built an ERP from the ground up (Trello to Innergy) that exposed how documentation gaps directly impact revenue",
])

job("Feb 2011 — Dec 2017", "Visual Interest", "Denver, CO", "Associate Sales & Marketing Director", [
    "Top-producing salesperson six consecutive years — led outside specification sales team as primary liaison for 80+ manufacturers, contributing to ~59% agency revenue growth during tenure",
    "Created SparkLab to solve a structural agency problem: 100+ competing manufacturer lines, limited specifier attention — designed an experiential model that moved specifications and is still running 10 years later, widely referenced and widely copied",
    "Negotiated merger of Pure Lighting LLC into Visual Interest — structured as a 4-year buyout, transitioned all manufacturer partnerships, and launched the agency's boutique decorative lighting arm",
])

job("May 2007 — June 2011", "Pure Lighting LLC", "Denver, CO", "Founder / Owner", [
    "Founded and scaled an independent boutique architectural lighting rep agency from zero — built 200+ client accounts across developers, distributors, contractors, architects, lighting designers, and end users, growing to a successful merger in 2011",
])

# ══════════════════════════════════════════
# EDUCATION & CERTIFICATIONS
# ══════════════════════════════════════════
story.append(Paragraph("EDUCATION &amp; CERTIFICATIONS", s_section))
story.append(section_rule())

edu_entries = [
    ("Bachelor of Industrial Design", "Lighting & Furniture Focus", "Art Institute of Colorado"),
    ("Interior Design & Construction Management Studies", "", "Colorado State University"),
    ("NLP Practitioner Certification", "", ""),
    ("AI Business Strategy & Implementation", "Continuing Education — In Progress", ""),
]

for title, subtitle, school in edu_entries:
    story.append(Paragraph(title, s_edu_title))
    if subtitle:
        story.append(Paragraph(subtitle, s_edu_sub))
    if school:
        story.append(Paragraph(school, s_edu_sub))
    story.append(Spacer(1, 4))

# ══════════════════════════════════════════
# EXPERTISE + TECHNICAL SKILLS (two col)
# ══════════════════════════════════════════
expertise = [
    "Systems Integration & Operations",
    "CRM / ERP Optimization",
    "Workflow Automation",
    "Cross-Functional Leadership",
    "Specification Sales",
    "AI Workflow Integration",
    "Project Pipeline Visibility",
]

tech_skills = [
    "Microsoft Suite", "Microsoft Copilot & Sales", "ChatGPT",
    "Claude", "Perplexity AI", "Google Gemini",
    "Notebook LM", "Trello", "Miro",
    "Figma", "Salesforce", "HubSpot",
    "Make / Zapier", "Notion AI", "Asana",
    "GitHub", "Jira", "Bluebeam Revu",
    "Adobe Suite", "Basic AutoCAD",
]

# ══════════════════════════════════════════
# VOLUNTEERING
# ══════════════════════════════════════════
story.append(Paragraph("VOLUNTEERING", s_section))
story.append(section_rule())

vol_entries = [
    ("WILD Denver", "Board Member", "Jan 2021 — Present"),
    ("WILD — Women in Lighting & Design National", "AI Integration & Tools Lead", "Jul 2024 — Present"),
    ("A Little Help", "Technology Assistance for Elderly", "Apr 2023 — Present"),
    ("Brilliance Awards", "Brand Development & Marketing", "Feb 2015 — Nov 2017"),
    ("Women in Design Denver", "Director of Social Media", "Jan 2012 — Apr 2014"),
]

for org, role, dates in vol_entries:
    vol_row = Table(
        [[Paragraph(f'<b>{org}</b>', ParagraphStyle('vh', fontName=FONT_BOLD, fontSize=9.5, leading=13, textColor=TEAL)),
          Paragraph(dates, ParagraphStyle('vd', fontName=FONT, fontSize=8.5, leading=13, textColor=MUTED, alignment=2))]],
        colWidths=[4.8*inch, 2.0*inch]
    )
    vol_row.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(vol_row)
    story.append(Paragraph(role, ParagraphStyle('vr', fontName=FONT, fontSize=9, leading=12, textColor=BLACK, spaceAfter=5)))

story.append(Spacer(1, 2))

# Merge expertise + tech skills into one SKILLS section — 3 columns
all_skills = expertise + [""] + tech_skills  # empty string = visual separator

def skills_col(items):
    paras = []
    for item in items:
        if item == "":
            paras.append(Spacer(1, 6))
        else:
            p = ParagraphStyle('sk', fontName=FONT, fontSize=8.5, leading=13, textColor=BLACK)
            paras.append(Paragraph(f"● {item}", p))
    return paras

story.append(Paragraph("SKILLS", s_section))
story.append(section_rule())

# Two blocks: expertise left, tech skills right (2 cols)
from reportlab.platypus import KeepInFrame

# Expertise col header + items
exp_block = [Paragraph("Core Expertise", ParagraphStyle('ch', fontName=FONT_BOLD, fontSize=8, leading=11, textColor=MUTED, spaceAfter=4))]
for item in expertise:
    exp_block.append(Paragraph(f"● {item}", ParagraphStyle('sk', fontName=FONT, fontSize=8.5, leading=13, textColor=BLACK)))

# Tech skills col header + items in 2 sub-columns via nested table
half = (len(tech_skills) + 1) // 2
ts_left = tech_skills[:half]
ts_right = tech_skills[half:]

tech_header = Paragraph("Tools & Platforms", ParagraphStyle('ch', fontName=FONT_BOLD, fontSize=8, leading=11, textColor=MUTED, spaceAfter=4))

def mini_col(items):
    paras = []
    for item in items:
        paras.append(Paragraph(f"● {item}", ParagraphStyle('sk', fontName=FONT, fontSize=8.5, leading=13, textColor=BLACK)))
    return paras

ts_lf = KeepInFrame(2.0*inch, 300, mini_col(ts_left), mode='shrink')
ts_rf = KeepInFrame(2.0*inch, 300, mini_col(ts_right), mode='shrink')
tech_inner = Table([[ts_lf, ts_rf]], colWidths=[2.0*inch, 2.0*inch])
tech_inner.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 0),
    ('RIGHTPADDING', (0,0), (-1,-1), 2),
    ('TOPPADDING', (0,0), (-1,-1), 0),
    ('BOTTOMPADDING', (0,0), (-1,-1), 0),
]))

tech_block = [tech_header, tech_inner]

lf_exp = KeepInFrame(2.4*inch, 300, exp_block, mode='shrink')
rf_tech = KeepInFrame(4.2*inch, 300, tech_block, mode='shrink')

skills_table = Table([[lf_exp, rf_tech]], colWidths=[2.4*inch, 4.3*inch])
skills_table.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 0),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 0),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(skills_table)

# ── BUILD ──
doc.build(story)
print(f"Saved: {OUTPUT}")
