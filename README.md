# 🎯 Stackscore — ATS Resume Checker

> **AI-powered Applicant Tracking System resume analyzer** built with FastAPI, Streamlit, Groq LLM, spaCy, and Supabase.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Supabase](https://img.shields.io/badge/Supabase-Auth%20%2B%20DB-3ECF8E?style=flat&logo=supabase&logoColor=white)](https://supabase.com/)
[![Groq](https://img.shields.io/badge/Groq-llama--3.3--70b-F55036?style=flat)](https://groq.com/)

---

## 📖 Introduction

**Stackscore** is a full-stack ATS (Applicant Tracking System) resume analysis platform that gives job seekers instant, actionable feedback on how well their resume will perform against automated screening systems used by recruiters.

### What it does

- **Parses** uploaded PDF resumes using Groq's `llama-3.3-70b-versatile` LLM to extract structured data (skills, experience, projects, education, contact info).
- **Scores** resumes across **5 weighted components** — Formatting, Keywords, Content Quality, Skill Validation, and ATS Compatibility — producing a final **0–100 ATS Score**.
- **Compares** resumes against an optional job description using **semantic cosine similarity** (SentenceTransformer) + **fuzzy keyword matching** (RapidFuzz), identifying matched/missing keywords and skill gaps.
- **Validates** that listed skills are actually backed by evidence in project and experience sections (semantic similarity ≥ 0.6).
- **Generates** detailed, structured feedback cards for every detected issue, with severity levels, explanations, and exact action items.
- **Exports** a full PDF report via the server-side HTML → PDF pipeline.
- **Persists** every analysis to Supabase so users can track improvement over time.
- **Authenticates** users via email/password or Google OAuth (PKCE flow via Supabase Auth).

### ML Research (Notebooks)
The `notebooks/` directory contains the ML experimentation trail — exploratory data analysis on resume datasets, BERT embedding experiments, and a fine-tuned BERT classification model for resume category prediction.

---

## 🗂️ Project Structure

```
ATS-Resume-Checker/
├── client/                         # Streamlit frontend
│   ├── app.py                      # Entry point, routing, auth sidebar
│   ├── assets/
│   │   └── styles.css              # Custom CSS themes
│   ├── components/                 # Reusable UI components
│   │   ├── dashboard.py            # Main results orchestrator
│   │   ├── score_display.py        # Score rings & progress bars
│   │   ├── detailed_feedback.py    # Issue detail cards
│   │   ├── jd_comparision.py       # Keyword match panel
│   │   ├── skill_validation.py     # Skill evidence map
│   │   ├── strengths_issues.py     # Strengths & critical issues
│   │   ├── actions_items.py        # Actionable checklist
│   │   └── recommendations.py     # Improvement suggestions
│   ├── services/
│   │   ├── api_client.py           # HTTP client for FastAPI backend
│   │   └── supabase_client.py      # Auth client (email + Google OAuth)
│   └── views/
│       ├── landing.py              # Home/marketing page
│       ├── scorer.py               # Resume upload & analysis UI
│       ├── history.py              # Past analyses view
│       └── resources.py           # Tips & learning resources
│
├── server/                         # FastAPI backend
│   ├── main.py                     # App factory, CORS, model loading
│   ├── api/
│   │   ├── routes.py               # All /api/v1 endpoints
│   │   └── auth.py                 # JWT verification (HS256/RS256)
│   ├── core/
│   │   └── config.py              # Environment config & constants
│   ├── database/
│   │   └── db.py                  # Supabase REST client (CRUD)
│   ├── models/
│   │   └── schemas.py             # Pydantic request/response models
│   ├── services/
│   │   ├── resume_parser.py        # File validation + text extraction
│   │   ├── groq_parser.py          # LLM resume & JD parsing
│   │   ├── resume_analyzer.py      # Analysis pipeline orchestrator
│   │   ├── ats_scorer.py           # 5-component scoring engine
│   │   ├── feedback_engine.py      # Issue detection engine
│   │   ├── jd_matcher.py           # JD comparison (semantic + fuzzy)
│   │   ├── recommendation_engine.py # Improvement recommendations
│   │   ├── report_generator.py     # HTML report builder
│   │   └── pdf_export.py           # HTML → PDF converter
│   └── utlis/
│       ├── file_utlis.py           # Error classes, logging helpers
│       └── matching.py             # Fuzzy matching utilities
│
├── notebooks/                      # ML research & experimentation
|   ├── pdfs                        # Resumes Folder
│   ├── EDA.ipynb                   # Exploratory Data Analysis
│   ├── BERT.ipynb                  # BERT embedding experiments
|   ├── FINE_TUNNING.ipynb          # BERT fine-tuning pipeline     
│   └── Testing_BERT.ipynb          # BERT Testing pipeline
│
├── models/                         # Trained model artifacts
│   ├── resume_embedding.pkl        # Pre-computed resume embeddings
│   └── finetuned-bert/             # Fine-tuned BERT model weights
│
├── Dataset/                        # Training data
│   ├── cleaned_dataset.csv         # Pre-processed resume texts
│   └── resumeJD2_pairs.csv         # Resume–JD paired training data
├── ARCHITECTURE.md                 # System architecture documentation
├── requirements.txt                # All Python dependencies
└── README.md
```

---

## 🏗️ System Architecture

> For detailed Mermaid flowcharts of all layers, see [ARCHITECTURE.md](./ARCHITECTURE.md).

```
┌──────────────────────────────────────────────────────────────────┐
│                          USER (Browser)                          │
└───────────────────────────────┬──────────────────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │  Streamlit Client     │
                    │  :8501                │
                    │  Auth │ Upload │ View │
                    └───────────┬───────────┘
                                │  REST + JWT
                    ┌───────────▼───────────┐
                    │  FastAPI Server       │
                    │  :8000                │
                    │  /api/v1/*            │
                    └──┬────────┬──────┬────┘
                       │        │      │
         ┌─────────────▼─┐  ┌───▼───┐  │ ┌─────────────────┐
         │  Groq LLM     │  │Supbase│  └─► ML Models Local │
         │  llama-3.3    │  │Auth+DB│    │ finetuned-bert  │
         └───────────────┘  └───────┘    └─────────────────┘
```

### Key Design Decisions

| Concern | Solution |
|---|---|
| Resume parsing | Groq LLM (`llama-3.3-70b-versatile`) — structured JSON extraction |
| Semantic similarity | Custom fine-tuned MPNet local model (fallback: `all-MiniLM-L6-v2`) |
| NLP / NER | spaCy `en_core_web_md` (fallback: `en_core_web_sm`) |
| Keyword matching | RapidFuzz token-sort-ratio (threshold 80%) |
| Auth | Supabase JWT — supports HS256, RS256, ES256 via JWKS |
| Database | Supabase (PostgreSQL) via REST API |
| PDF export | Jinja2 HTML templates → xhtml2pdf / WeasyPrint |

---

## 🗄️ Database Schema

### Table: `analyses`

Stored in **Supabase (PostgreSQL)**. All queries are scoped by `user_id` (Supabase Auth UUID).

| Column | Type | Description |
|---|---|---|
| `id` | `uuid` (PK) | Auto-generated primary key |
| `user_id` | `uuid` | Foreign key → `auth.users.id` (RLS enforced) |
| `filename` | `text` | Uploaded resume filename |
| `ats_score` | `float8` | Overall ATS score (0–100) |
| `keyword_match` | `float8` | JD keyword match percentage |
| `missing_keywords` | `jsonb` | Array of missing JD keywords |
| `analysis_result` | `jsonb` | Full `AnalysisResponse` payload (all scores, issues, feedback) |
| `created_at` | `timestamptz` | UTC timestamp of analysis |

### Pydantic Schemas (server-side validation)

#### `AnalysisResponse`
```python
class AnalysisResponse(BaseModel):
    ATS_score: float                              # Primary score field
    ats_score: float                              # Alias for compatibility
    component_scores: ComponentScores
    issues_summary: List[str]
    detailed_feedback: List[IssueDetail]
    jd_match_analysis: Optional[JDComparison]
    skill_validation_details: Optional[SkillValidationDetails]
    keyword_match: float
    missing_keywords: List[str]
    matched_keywords: List[str]
    skills: List[str]
    interpretation: str
```

#### `ComponentScores`
```python
class ComponentScores(BaseModel):
    formatting: float          # /20 pts
    keywords: float            # /25 pts
    content: float             # /25 pts
    skill_validation: float    # /15 pts
    ats_compatibility: float   # /15 pts
```

#### `JDComparison`
```python
class JDComparison(BaseModel):
    match_percentage: float         # 0–100 combined score
    semantic_similarity: float      # cosine similarity 0–1
    matched_keywords: List[str]     # keywords found in resume
    missing_keywords: List[str]     # keywords absent from resume
    skills_gap: List[str]           # skills in JD not in resume
```

#### `SkillValidationDetails`
```python
class SkillValidationDetails(BaseModel):
    validated: List[Dict[str, Any]]  # [{'skill': str, 'projects': [str]}]
    unvalidated: List[str]           # skills without project evidence
    total: int
    validated_count: int
    validation_pct: float            # 0–100
```

#### `IssueDetail`
```python
class IssueDetail(BaseModel):
    issue_title: str
    severity_level: str        # 'High' | 'Medium' | 'Low'
    ats_impact: str            # 'High' | 'Medium' | 'Low'
    explanation: str
    where_it_appears: str
    how_to_fix: str
    action_items: List[str]
    example_improvement: str
```

---

## 📊 Scoring Model

The ATS score is computed from **5 weighted components** totaling 100 points:

| Component | Max Points | What it Measures |
|---|:---:|---|
| **Keywords** | 25 | Resume term density, skills count, JD keyword overlap |
| **Content Quality** | 25 | Action verbs, quantifiable achievements, grammar |
| **Formatting** | 20 | Section presence (experience, education, skills, summary, projects), bullet point count |
| **Skill Validation** | 15 | % of listed skills backed by project/experience evidence (cosine sim ≥ 0.6) |
| **ATS Compatibility** | 15 | Privacy risk (location), special characters, section completeness |

### Weighted Aggregation
```
base_score = (
    skills_keywords_pct  × 0.40 +   # keywords(60%) + skill_validation(40%)
    content_pct          × 0.30 +
    formatting_pct       × 0.15 +
    ats_compatibility_pct × 0.15
)
```

### Score Interpretation

| Score | Band | Interpretation |
|:---:|---|---|
| 90–100 | 🟢 Excellent | Highly optimized for ATS systems |
| 80–89 | 🟢 Great | Should perform well with most ATS |
| 70–79 | 🟡 Good | ATS-friendly with minor room for improvement |
| 60–69 | 🟡 Fair | Needs some improvements |
| 50–59 | 🟠 Below Average | Significant improvements needed |
| 0–49 | 🔴 Poor | Major revisions required |

---

## 📓 Notebooks

The `notebooks/` directory documents the full ML research pipeline.

### `EDA.ipynb` — Exploratory Data Analysis
- Distribution of resume categories in `cleaned_dataset.csv`
- Text length statistics and vocabulary analysis
- Keyword frequency analysis across job categories
- Resume–JD pairing statistics from `resumeJD2_pairs.csv`

### `BERT.ipynb` — BERT Embedding Experiments
- Generates sentence-level BERT embeddings for resume texts
- Benchmarks cosine similarity between resumes and job descriptions
- Produces `models/resume_embedding.pkl` — pre-computed embedding cache
- Evaluates `all-MiniLM-L6-v2` vs base BERT for semantic matching quality

### `FINE_TUNNING.ipynb` — BERT Fine-Tuning Pipeline
- Adds a classification head on top of BERT for resume category prediction
- Training loop on labeled resume dataset
- Exports fine-tuned weights to `models/finetuned-bert(all-mpnet-base-v2)/`
- Serves as the actual production semantic similarity embedder used by the FastAPI server

---

## 🚀 API Reference

Base URL: `http://127.0.0.1:8000/api/v1`

All endpoints (except `/health`) require:
```
Authorization: Bearer <supabase_access_token>
```

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check — confirms models are loaded |
| `POST` | `/analyze-resume` | Analyze a resume PDF (multipart/form-data) |
| `GET` | `/history` | Get the signed-in user's past analyses |
| `DELETE` | `/history/{id}` | Delete one analysis from history |
| `POST` | `/generate-pdf` | Generate PDF report from analysis data |
| `GET` | `/history/{id}/pdf` | Generate PDF from a saved history entry |

### `POST /analyze-resume`
```
Content-Type: multipart/form-data

Fields:
  resume          : File   (PDF, max 5 MB)
  job_description : string (optional — paste JD text for comparison mode)
```

Returns: `AnalysisResponse` JSON

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.10+
- A [Supabase](https://supabase.com/) project with:
  - An `analyses` table (schema above)
  - Email/password auth enabled
  - Google OAuth provider configured (optional)
- A [Groq](https://console.groq.com/) API key

### 1. Clone and install

```bash
git clone https://github.com/your-org/ATS-Resume-Checker.git
cd ATS-Resume-Checker
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

pip install -r requirements.txt

# Download spaCy models
python -m spacy download en_core_web_md
python -m spacy download en_core_web_sm
```

### 2. Configure environment

**`server/.env`**
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_JWT_SECRET=your-jwt-secret
GROQ_API_KEY=your-groq-api-key
```

**`client/.env`** (or `client/.streamlit/secrets.toml`)
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
AUTH_REDIRECT_URL=http://localhost:8501
```

### 3. Run the server

```bash
uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Run the client

```bash
streamlit run client/app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit 1.32+ |
| **Backend** | FastAPI 0.110+ · Uvicorn · Gunicorn |
| **LLM** | Groq API (`llama-3.3-70b-versatile`) |
| **NLP** | spaCy 3.7 (`en_core_web_md`) |
| **Embeddings** | `sentence-transformers` · Fine-tuned local MPNet model (fallback: `all-MiniLM-L6-v2`) |
| **ML Research** | PyTorch · Transformers (BERT) |
| **Fuzzy Matching** | RapidFuzz |
| **File Parsing** | pdfplumber · PyPDF2 · python-magic |
| **PDF Generation** | xhtml2pdf · WeasyPrint · Jinja2 |
| **Auth** | Supabase Auth (email + Google OAuth / PKCE) · PyJWT |
| **Database** | Supabase (PostgreSQL) via REST |
| **Data Validation** | Pydantic v2 |

---

## 📄 License

This project is for educational purposes only.
