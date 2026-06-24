import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    local_env = Path(__file__).resolve().parents[1] / '.env'
    root_env = Path(__file__).resolve().parents[2] / '.env'
    if local_env.exists():
        load_dotenv(local_env, override=True)
    elif root_env.exists():
        load_dotenv(root_env, override=True)
    else:
        load_dotenv(override=True)
except ImportError:
    pass

#api metadata
APP_TITLE='STACKSCORE - ATS Resume Checker API'
APP_VERSION='1.0.0'
APP_DESCRIPTION='Analyse resumes against job description using nlp + ml'

ALLOWED_ORIGINS = [
    'https://appapppy-ktwxupi73vqhjzweksze9d.streamlit.app/'
]  

#file 
MAX_FILE_SIZE_MB=5
MAX_FILE_SIZE_BYTES=MAX_FILE_SIZE_MB*1024*1024
ALLOWED_FILE_TYPES = {
    "application/pdf" : "pdf",        # PDF files only
}


ALLOWED_EXTENSIONS = {'.pdf'}

SPACY_MODEL_PRIMARY="en_core_web_md"
SPACY_MODEL_SECONDARY="en_core_web_sm"
SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L6-v2"

# Score component weights — this is business logic treated as config
SCORE_WEIGHTS = {
    "formatting": 20, "keywords": 25, "content": 25,
    "skill_validation": 15, "ats_compatibility": 15,
}

JD_KEYWORD_WEIGHT=0.6
JD_SEMANTIC_WEIGHT=0.4

SUPABASE_URL       = os.getenv('SUPABASE_URL', '')
SUPABASE_KEY       = os.getenv('SUPABASE_KEY', '')          # service_role — DB writes (bypasses RLS)
SUPABASE_ANON_KEY  = os.getenv('SUPABASE_ANON_KEY', '')     # public anon — frontend auth calls
SUPABASE_JWT_SECRET= os.getenv('SUPABASE_JWT_SECRET', '')   # used by backend to verify access tokens
GROQ_API_KEY       = os.getenv('GROQ_API_KEY', '')

