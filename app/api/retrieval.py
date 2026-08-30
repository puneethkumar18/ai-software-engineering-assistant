from fastapi import APIRouter,Depends
from app.schemas.retrieval import RetrievalRequest, RetrievalResult
from sqlalchemy.orm import Session
from app.services.embedding_service import EmbeddingService
from app.services.retrieval_service import RetrievalService
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/retrieval",
    tags=["Retrieval"],
)

@router.post("/search",response_model=list[RetrievalResult])
async def search(request: RetrievalRequest,session: Session = Depends(get_db)):
    embedding_service = EmbeddingService()

    retrieval_service = RetrievalService(
        embedding_service
    )

    return await retrieval_service.retrieve(
        session=session,
        repository_id=request.repository_id,
        query=request.query,
        top_k=request.tok_k,
        document_type=request.document_type,
        language=request.language,
    )

