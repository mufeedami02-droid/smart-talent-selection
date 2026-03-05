from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import fitz
import re
import uuid
from docx import Document
from sentence_transformers import SentenceTransformer, util
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

candidates = []
ranked_candidates = []

MAX_FILE_SIZE = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = [".pdf", ".docx", ".txt"]

SKILLS = [
    "Python", "Java", "JavaScript", "React", "Django",
    "FastAPI", "SQL", "MySQL", "PostgreSQL", "MongoDB",
    "AWS", "Docker", "Machine Learning", "REST", "Git"
]

# ---------------- LOAD MODEL ---------------- #
model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------- TEXT EXTRACTION ---------------- #

def extract_text(file_path: Path, extension: str):
    text = ""
    try:
        if extension == ".pdf":
            with fitz.open(file_path) as doc:
                for page in doc[:5]:
                    text += page.get_text()

        elif extension == ".docx":
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"

        elif extension == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

    except Exception:
        return ""

    return text.strip()[:5000]

# ---------------- EXTRACTION ---------------- #

def extract_skills(text):
    text_lower = text.lower()
    return [skill for skill in SKILLS if skill.lower() in text_lower]

def extract_experience(text):
    matches = re.findall(r'(\d+)\+?\s*(years|yrs)', text.lower())
    years = [int(m[0]) for m in matches]
    return max(years) if years else 0

# ---------------- SCORING ---------------- #

def semantic_match(resume_embedding, jd_embedding):
    similarity = util.cos_sim(resume_embedding, jd_embedding)
    score = float(similarity[0][0])
    return max(0, min(100, round(score * 100, 2)))

def calculate_skill_match(candidate_skills, jd_skills):
    if not jd_skills:
        return 0, []

    matched = set(s.lower() for s in candidate_skills) & \
              set(s.lower() for s in jd_skills)

    percent = round((len(matched) / len(jd_skills)) * 100, 2)
    return percent, list(matched)

def experience_score(years):
    if years >= 8: return 100
    if years >= 5: return 80
    if years >= 3: return 60
    if years >= 1: return 40
    return 20

def get_recommendation(score):
    if score >= 75: return "Strong Hire"
    if score >= 60: return "Consider"
    if score >= 40: return "Maybe"
    return "Reject"

def final_match(candidate, jd_embedding, jd_skills):

    skill_percent, matched_skills = calculate_skill_match(
        candidate["skills"], jd_skills
    )

    semantic_percent = semantic_match(
        candidate["embedding"], jd_embedding
    )

    exp_percent = experience_score(candidate["experience"])

    final_percent = (
        0.5 * skill_percent +
        0.3 * semantic_percent +
        0.2 * exp_percent
    )

    candidate.update({
        "skills_score": skill_percent,
        "semantic_score": semantic_percent,
        "experience_score": exp_percent,
        "final_percent": round(final_percent, 2),
        "matched_skills": matched_skills,
        "recommendation": get_recommendation(final_percent)
    })

# ---------------- ROUTES ---------------- #

# 🟢 PAGE 1
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request
    })

# 🟢 PROCESS + REDIRECT
@app.post("/analyze")
async def analyze(
    request: Request,
    files: List[UploadFile] = File(...),
    jd_text: str = Form(...)
):
    global candidates, ranked_candidates

    candidates.clear()
    ranked_candidates.clear()

    jd_skills = extract_skills(jd_text)
    jd_embedding = model.encode(jd_text, convert_to_tensor=True)

    for file in files:
        file_ext = Path(file.filename).suffix.lower()

        if file_ext not in ALLOWED_EXTENSIONS:
            continue

        contents = await file.read()

        if len(contents) > MAX_FILE_SIZE:
            continue

        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = UPLOAD_FOLDER / unique_filename

        with open(file_path, "wb") as buffer:
            buffer.write(contents)

        extracted_text = extract_text(file_path, file_ext)

        if not extracted_text:
            continue

        embedding = model.encode(extracted_text, convert_to_tensor=True)

        candidate = {
            "name": file.filename,
            "filename": file.filename,
            "skills": extract_skills(extracted_text),
            "experience": extract_experience(extracted_text),
            "embedding": embedding
        }

        final_match(candidate, jd_embedding, jd_skills)

        # Remove embedding before sending to frontend
        candidate.pop("embedding")

        candidates.append(candidate)

    ranked_candidates = sorted(
        candidates,
        key=lambda x: x["final_percent"],
        reverse=True
    )

    return RedirectResponse(url="/results", status_code=303)

# 🔵 PAGE 2
@app.get("/results", response_class=HTMLResponse)
async def results(request: Request):
    return templates.TemplateResponse("results.html", {
        "request": request,
        "candidates": ranked_candidates
    })

@app.get("/clear")
async def clear_data():
    candidates.clear()
    ranked_candidates.clear()
    return RedirectResponse(url="/", status_code=303)