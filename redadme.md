# Smart Talent Selection  
### AI-Powered Resume Intelligence & Candidate Ranking Platform

---

## 1. Executive Summary

Smart Talent Selection is an AI-driven web application designed to automate and optimize the resume screening process. The platform enables recruiters to upload multiple resumes along with a job description and receive an intelligent, relevance-based ranking of candidates within seconds.

The system leverages Natural Language Processing (NLP) and semantic similarity algorithms to enhance hiring efficiency, reduce manual effort, and support data-driven recruitment decisions.

---

## 2. Problem Statement

Organizations often receive a large volume of resumes for a single job opening. Manual screening is:

- Time-consuming  
- Subjective and inconsistent  
- Resource-intensive  
- Prone to human bias  

There is a clear need for an automated system that can efficiently analyze candidate resumes and rank them based on job relevance in a scalable and objective manner.

---

## 3. Proposed Solution

Smart Talent Selection addresses this challenge by providing:

- Multi-resume upload capability
- Automated text extraction from PDF/DOCX files
- Semantic similarity analysis between resumes and job description
- AI-based candidate scoring
- Ranked results dashboard with match percentages
- Professional user interface for recruiter workflow

The system computes similarity scores using TF-IDF vectorization and cosine similarity to measure contextual alignment between candidate profiles and job requirements.

---

## 4. Key Features

- 📄 Multiple Resume Upload
- 📊 AI-Based Candidate Ranking
- 🧠 Semantic Matching Engine
- ⚡ Fast Real-Time Processing
- 📈 Professional Results Dashboard
- 🖥 Responsive and Modern UI

---

## 5. Technology Stack

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### Backend
- Python 3
- Flask (Web Framework)
- Jinja2 (Templating Engine)

### AI / NLP Layer
- Scikit-learn
- TF-IDF Vectorizer
- Cosine Similarity Algorithm

### Document Processing
- PyPDF2 (PDF Parsing)
- python-docx (DOCX Parsing)

---

## 6. System Architecture Overview

User Input (Resumes + Job Description)
        ↓
Flask Backend Processing
        ↓
Text Extraction Layer
        ↓
NLP Vectorization (TF-IDF)
        ↓
Cosine Similarity Scoring
        ↓
Ranking Engine
        ↓
Results Dashboard (Frontend)

---

## 7. Setup Instructions (Local Deployment)

Step 1: Clone the Repository
git clone https://github.com/mufeedami02-droid/smart-talent-selection.git
cd smart-talent-selection
Step 2: Create a Virtual Environment
python -m venv venv
Step 3: Activate the Virtual Environment
Windows
venv\Scripts\activate
macOS / Linux
source venv/bin/activate
Step 4: Install Required Dependencies

Install all required Python libraries.

pip install flask scikit-learn PyPDF2 python-docx
Step 5: Verify Project Structure

Ensure your project directory looks like this:

smart-talent-selection
│
├── main.py
├── README.md
│
├── templates
│   ├── index.html
│   └── result.html
│
└── static (optional)
Step 6: Run the Application

Start the Flask server using the following command:

python main.py
Step 7: Open the Application

After running the server, open your browser and go to:

http://127.0.0.1:5000

You will now see the Smart Talent Selection interface, where recruiters can upload resumes and analyze candidate rankings.

Step 8: Upload Resumes and Job Description

Enter a Job Description

Upload multiple resumes (PDF or DOCX)

Click Analyze

View AI-based candidate ranking results