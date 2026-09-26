from fastapi import FastAPI
from app.core.config import settings

from app.api.ai import router as ai_Router
from app.api.retrieval import router as retrieval_router
from app.api.repository import router as repository_router
from app.api.agent import router as agent_router


from app.core.logging_config import setup_logging


setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

app.include_router(router=ai_Router)
app.include_router(router=retrieval_router)
app.include_router(router=repository_router)
app.include_router(router=agent_router)

@app.get("/health")
def health():
    return {"status":"ok"}