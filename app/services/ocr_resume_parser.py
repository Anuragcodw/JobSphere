import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Dell\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

POPPLER_PATH = r"C:\Users\Dell\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"

SKILL_KEYWORDS = [
    "python", "java", "javascript", "html", "css", "react", "node",
    "sql", "mysql", "postgres", "mongodb",
    "data analysis", "machine learning", "ai", "deep learning",
    "django", "flask", "power bi", "excel",
]


def parse_resume_file(pdf_path):
    text_output = ""

    pages = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)

    for page in pages:
        ocr_text = pytesseract.image_to_string(page)
        text_output += "\n" + ocr_text.lower()

    text = text_output.lower()

    found_skills = [skill for skill in SKILL_KEYWORDS if skill in text]
    found_skills = list(set(found_skills))

    exp = None

    match = re.search(r"(\d+)\s*\+?\s*years?", text)
    if match:
        exp = int(match.group(1))
    else:
        
        alt = re.search(r"(\d+)\s*(yrs|yr)", text)
        if alt:
            exp = int(alt.group(1))

    education = ""

    edu_patterns = [
        r"(b\.?tech|Btech|bachelor of technology)",
        r"(b\.?sc|Bsc|bachelor of science)",
        r"(b\.?com|Bcom|bachelor of commerce)",
        r"(b\.?a|Ba|bachelor of arts)",
        r"(m\.?tech|Mtech|master of technology)",
        r"(m\.?sc|Msc|master of science)",
        r"(diploma|Intermediate|12th|10th)"
    ]

    for p in edu_patterns:
        m = re.search(p, text, re.I)
        if m:
            education = m.group(1)
            break

    return {
        "text": text,
        "skills": found_skills,
        "experience_years": exp,
        "education": education
    }
