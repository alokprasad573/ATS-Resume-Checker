import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware




from server.core.config import ( ALLOWED_ORIGINS, APP_DESCRIPTION, APP_TITLE, APP_VERSION, 
                                 SPACY_MODEL_PRIMARY, SPACY_MODEL_SECONDARY, SENTENCE_TRANSFORMER_MODEL)
# from server.api.routes import router 

logger = logging.getLogger('stackscore-ats-resume-checker')

@asynccontextmanager
async def lifespan (app: FastAPI):
    logger.info ('Starting STACKSCORE - ATS Resume Checker API...')
    logger.info(f'Loading spaCy models : {SPACY_MODEL_PRIMARY}')
    import spacy 
    try:
        app.state.nlp = spacy.load(SPACY_MODEL_PRIMARY)
        logger.info(f'Loaded {SPACY_MODEL_PRIMARY}')
    except OSError:
        logger.warning(f'{SPACY_MODEL_PRIMARY} not found, falling back to {SPACY_MODEL_SECONDARY}')
        app.state.nlp = spacy.load(SPACY_MODEL_SECONDARY)
        logger.info(f'Loaded {SPACY_MODEL_SECONDARY}')
        
    logger.info(f'Loading SentenceTransformmer: {SENTENCE_TRANSFORMER_MODEL}')
    from sentence_transformers import SentenceTransformer
    app.state.embedder = SentenceTransformer(SENTENCE_TRANSFORMER_MODEL)
    logger.info(f'Loaded SentenceTransformmer {SENTENCE_TRANSFORMER_MODEL}')
      
    logger.info(f'Server is ready...')
    yield
    
    logger.info('Server is shutting down the api...')
    
app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    lifespan=lifespan,
    docs_url='/docs',
    redoc_url='/redoc'
)
        
app.add_middleware(
    CORSMiddleware,
    allow_origins=[*ALLOWED_ORIGINS, 'http://localhost:8501' ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# app.include_router(router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        'server.main:app',
        host = '0.0.0.0',
        port = 8000,
        reload = True
    )
    
                                 