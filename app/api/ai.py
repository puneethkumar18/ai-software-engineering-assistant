from fastapi import APIRouter,Depends,HTTPException 

from app.schemas.ai import AIRequest,AIResponse,AISource
from app.services.rag_service import RAGService
from app.services.embedding_service import EmbeddingService
from app.services.retrieval_service import RetrievalService
from app.services.ai_service import AIService
from app.repositories.repository import get_repository

from app.core.dependencies import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/ai",tags=["AI"])



@router.post("/ask",response_model=AIResponse)
async def ask_ai(request:AIRequest,session:Session=Depends(get_db)):

    repository = get_repository(
        session=session,
        repository_id=request.repository_id
    )

    if repository is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found.",
        )

    embedding_service = EmbeddingService()

    rag_service = RAGService(
        retrieval_service=RetrievalService(embedding_service=embedding_service),
        ai_service=AIService()
    )

    answer, results = await rag_service.generate_answer(
        session=session,
        repository_id=request.repository_id,
        query=request.message,
    )
    
    sources = [
        AISource(
            source=result.source,
            start_line=result.start_line,
            end_line=result.end_line,
        )
        for result in results
    ]

    return AIResponse(
        response=answer,
        sources=sources,
    )