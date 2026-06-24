# 🏗️ System Architecture — Stackscore ATS Resume Checker

---

## 1. High-Level System Overview

```mermaid
flowchart TD
    USER["👤 User (Browser)"]
    CLIENT["🖥️ Client<br>Streamlit App<br>:8501"]
    SERVER["⚙️ Server<br>FastAPI REST API<br>:8000"]
    GROQ["🤖 Groq LLM<br>llama-3.3-70b-versatile<br>(External API)"]
    SUPABASE["🗄️ Supabase<br>Auth + PostgreSQL<br>(External Cloud)"]
    MODELS["🧠 ML Models<br>spaCy + SentenceTransformer<br>(Local: finetuned-bert)"]

    USER -->|"HTTP / Browser"| CLIENT
    CLIENT -->|"REST + JWT Bearer"| SERVER
    SERVER -->|"LLM Resume Parsing"| GROQ
    SERVER -->|"Read/Write analyses"| SUPABASE
    CLIENT -->|"Auth (email/OAuth)"| SUPABASE
    SERVER -->|"NLP inference"| MODELS
```

---

## 2. Client Architecture (Streamlit)

```mermaid
flowchart TD
    subgraph CLIENT["🖥️ client/"]
        APP["app.py<br>Entry Point & Router"]

        subgraph VIEWS["views/"]
            LANDING["landing.py<br>Marketing / Home Page"]
            SCORER["scorer.py<br>Resume Upload & Analysis UI"]
            HISTORY["history.py<br>Past Analyses View"]
            RESOURCES["resources.py<br>Tips & Learning"]
        end

        subgraph COMPONENTS["components/"]
            DASHBOARD["dashboard.py<br>Results Dashboard"]
            SCORE_DISP["score_display.py<br>Score Rings & Bars"]
            DETAILED_FB["detailed_feedback.py<br>Issue Cards"]
            JD_COMP["jd_comparision.py<br>Keyword Match Panel"]
            SKILL_VAL["skill_validation.py<br>Skill Evidence Map"]
            STRENGTHS["strengths_issues.py<br>Strengths & Critical Issues"]
            ACTION["actions_items.py<br>Actionable Checklist"]
            RECS["recommendations.py<br>Improvement Suggestions"]
        end

        subgraph SERVICES["services/"]
            API_CLIENT["api_client.py<br>HTTP to FastAPI Backend"]
            SB_CLIENT["supabase_client.py<br>Auth Client (email + Google OAuth)"]
        end

        subgraph ASSETS["assets/"]
            CSS["styles.css<br>Custom UI Themes"]
        end
    end

    APP -->|"route: landing"| LANDING
    APP -->|"route: scorer"| SCORER
    APP -->|"route: history"| HISTORY
    APP -->|"route: resources"| RESOURCES

    SCORER -->|"POST /api/v1/analyze-resume"| API_CLIENT
    SCORER -->|"POST /api/v1/generate-pdf"| API_CLIENT
    HISTORY -->|"GET /api/v1/history"| API_CLIENT
    HISTORY -->|"DELETE /api/v1/history/:id"| API_CLIENT

    SCORER --> DASHBOARD
    DASHBOARD --> SCORE_DISP
    DASHBOARD --> DETAILED_FB
    DASHBOARD --> JD_COMP
    DASHBOARD --> SKILL_VAL
    DASHBOARD --> STRENGTHS
    DASHBOARD --> ACTION
    DASHBOARD --> RECS

    APP -->|"sign in / sign up / OAuth"| SB_CLIENT
```

---

## 3. Server Architecture (FastAPI)

```mermaid
flowchart TD
    subgraph SERVER["⚙️ server/"]

        MAIN["main.py<br>FastAPI App + CORS<br>Lifespan: loads spaCy + SentenceTransformer"]

        subgraph API["api/"]
            ROUTES["routes.py<br>APIRouter /api/v1"]
            AUTH["auth.py<br>JWT Verification<br>HS256 / RS256 / ES256 via JWKS"]
        end

        subgraph CORE["core/"]
            CONFIG["config.py<br>Env vars, model names, score weights"]
        end

        subgraph SERVICES["services/"]
            PARSER["resume_parser.py<br>File Validation + Text Extraction<br>pdfplumber -> PyPDF2 fallback"]
            GROQ_P["groq_parser.py<br>LLM Calls: parse_resume() + parse_job_description()<br>Model: llama-3.3-70b-versatile"]
            ANALYZER["resume_analyzer.py<br>Orchestrates full analysis pipeline"]
            ATS_S["ats_scorer.py<br>Component Scores:<br>Formatting 20pt | Keywords 25pt<br>Content 25pt | Skill Validation 15pt<br>ATS Compat 15pt"]
            FEEDBACK["feedback_engine.py<br>Detects structured IssueDetail objects<br>missing sections, weak verbs, etc."]
            JD_MATCH["jd_matcher.py<br>Semantic + Keyword Comparison<br>60% keyword overlap + 40% cosine similarity"]
            RECO["recommendation_engine.py<br>Generates improvement recommendations"]
            REPORT["report_generator.py<br>Builds HTML report pages"]
            PDF_EXP["pdf_export.py<br>Renders HTML -> PDF bytes"]
        end

        subgraph DATABASE["database/"]
            DB["db.py<br>Supabase REST Client<br>save_analysis / get_user_history / delete_analysis"]
        end

        subgraph MODELS_S["models/"]
            SCHEMAS["schemas.py<br>Pydantic Models:<br>AnalysisResponse, ComponentScores,<br>JDComparison, SkillValidationDetails, IssueDetail"]
        end
    end

    MAIN --> ROUTES
    ROUTES -->|"Depends(get_current_user)"| AUTH
    ROUTES -->|"POST /analyze-resume"| PARSER
    PARSER -->|"raw text"| GROQ_P
    GROQ_P -->|"structured resume dict"| ANALYZER
    ANALYZER --> ATS_S
    ANALYZER --> FEEDBACK
    ANALYZER --> JD_MATCH
    ANALYZER --> RECO
    ROUTES -->|"save result"| DB
    ROUTES -->|"POST /generate-pdf"| REPORT
    REPORT --> PDF_EXP
    ROUTES --> SCHEMAS
```

---

## 4. Analysis Pipeline (Request Flow — Sequence Diagram)

```mermaid
sequenceDiagram
    participant U as User
    participant C as Streamlit Client
    participant S as FastAPI Server
    participant G as Groq LLM
    participant DB as Supabase DB

    U->>C: Upload resume PDF + optional JD text
    C->>S: POST /api/v1/analyze-resume Bearer JWT multipart/form-data
    S->>S: Validate JWT (Supabase JWKS / HS256)
    S->>S: validate_file() — size & MIME check
    S->>S: extract_text_from_pdf() — pdfplumber -> PyPDF2 fallback
    S->>G: parse_resume(raw_text) -> llama-3.3-70b
    G-->>S: Structured JSON (skills, experience, projects)
    opt JD provided
        S->>G: parse_job_description(jd_text)
        G-->>S: JD JSON (required_skills, keywords)
        S->>S: compare_resume_with_jd() — cosine + fuzzy
    end
    S->>S: validate_skills_with_projects() — cosine similarity >= 0.6
    S->>S: calculate_overall_score() — 5 component scores
    S->>S: analyze_issues() -> List IssueDetail
    S->>S: generate_issues_summary()
    S->>DB: save_analysis(user_id, filename, result)
    S-->>C: AnalysisResponse JSON
    C->>U: Render dashboard (scores, issues, JD match)
    opt PDF Export
        U->>C: Click Generate PDF
        C->>S: POST /api/v1/generate-pdf
        S->>S: generate_html_reports() -> generate_combined_pdf()
        S-->>C: PDF bytes application/pdf
        C->>U: Download ats_report.pdf
    end
```

---

## 5. Scoring Model

```mermaid
flowchart LR
    subgraph COMPONENTS["Score Components (100 pts total)"]
        FMT["Formatting<br>/20 pts<br>Sections, bullets, structure"]
        KW["Keywords<br>/25 pts<br>Resume terms + JD overlap"]
        CONT["Content Quality<br>/25 pts<br>Action verbs + achievements"]
        SKV["Skill Validation<br>/15 pts<br>Skills backed by projects"]
        ATS["ATS Compatibility<br>/15 pts<br>Privacy, special chars, completeness"]
    end

    subgraph PENALTIES["Penalties and Bonuses"]
        P1["Missing JD keywords<br>-5 to -15 pts"]
        P2["Location/privacy risk<br>-2 to -5 pts"]
        P3["Grammar errors<br>-variable pts"]
        B1["Perfect grammar bonus<br>+1 pt"]
        B2["Excellent skill validation<br>+1 to 2 pts"]
    end

    FMT & KW & CONT & SKV & ATS --> BASE["Base Score<br>weighted sum"]
    BASE --> FINAL["Final ATS Score<br>0 to 100"]
    P1 & P2 & P3 --> FINAL
    B1 & B2 --> FINAL
```

---

## 6. Notebook Pipeline (ML Research)

```mermaid
flowchart TD
    subgraph DATASET["Dataset/"]
        CSV1["cleaned_dataset.csv<br>Pre-processed resume texts"]
        CSV2["resumeJD2_pairs.csv<br>Resume-JD paired data"]
    end

    subgraph NOTEBOOKS["notebooks/"]
        EDA["EDA.ipynb<br>Exploratory Data Analysis<br>- Category distribution<br>- Text length stats<br>- Keyword frequency analysis"]
        BERT["BERT.ipynb<br>BERT Embedding Experiments<br>- Sentence-level embeddings<br>- Cosine similarity benchmarks<br>- resume_embedding.pkl"]
        FINE["FINE_TUNNING.ipynb<br>Fine-tuning Pipeline<br>- BERT classification head<br>- Resume category prediction<br>- models/finetuned-bert/ output"]
    end

    subgraph MODELS_OUT["models/"]
        EMB["resume_embedding.pkl<br>Pre-computed embeddings cache"]
        BERT_M["finetuned-bert/<br>Fine-tuned BERT weights"]
    end

    CSV1 --> EDA
    CSV2 --> EDA
    EDA -->|"cleaned insights"| BERT
    BERT -->|"embedding strategy"| FINE
    BERT --> EMB
    FINE --> BERT_M
    BERT_M -.->|"loaded by"| SERVER["Server<br>finetuned-bert (local)<br>SentenceTransformer"]
```

---

## 7. Authentication Flow

```mermaid
flowchart TD
    USER["User"]

    subgraph AUTH_METHODS["Authentication Methods"]
        EMAIL["Email + Password<br>via Supabase Auth"]
        GOOGLE["Google OAuth 2.0<br>PKCE Flow"]
    end

    subgraph SUPABASE_AUTH["Supabase Auth"]
        AUTH_SERVER["Auth Server<br>issues JWT"]
        ANON_KEY["SUPABASE_ANON_KEY<br>client-side"]
        JWT_SECRET["SUPABASE_JWT_SECRET<br>server-side verification"]
    end

    subgraph BACKEND_AUTH["Backend JWT Verification"]
        BEARER["HTTPBearer<br>extracts token"]
        VERIFY["_verify_token()<br>HS256 or RS256/ES256 via JWKS"]
        USER_ID["user_id extracted<br>from JWT sub claim"]
    end

    USER --> EMAIL & GOOGLE
    EMAIL & GOOGLE --> AUTH_SERVER
    AUTH_SERVER -->|"access_token + refresh_token"| USER
    USER -->|"Bearer token in header"| BEARER
    BEARER --> VERIFY
    VERIFY --> USER_ID
    USER_ID -->|"scoped DB queries"| DB["Supabase DB<br>RLS by user_id"]
```
