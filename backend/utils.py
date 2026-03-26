import pdfplumber
import re

def extract_text(filepath):
    try:
        if filepath.lower().endswith(".pdf"):
            text = ""
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text
        elif filepath.lower().endswith(".txt"):
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        else:
            return ""
    except Exception:
        return ""

def clean_text(text):
    return re.sub(r"[^a-zA-Z0-9\s]", " ", text).lower()

def detect_skills(text, skill_list):
    found = []
    for skill in skill_list:
        if skill.lower() in text:
            found.append(skill)
    return found

def calculate_score(found_skills, skill_list):
    if not skill_list:
        return 0
    return round((len(found_skills) / len(skill_list)) * 100, 2)

def generate_suggestions(found_skills, skill_list):
    missing = list(set(skill_list) - set(found_skills))
    if not missing:
        return ["Great job! Your resume covers all key skills."]
    return [f"Consider adding {skill} experience or projects." for skill in missing]