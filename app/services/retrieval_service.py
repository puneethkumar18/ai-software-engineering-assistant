from sqlalchemy.orm import Session
from app.vectorstore.repository import similarity_search

from app.services.embedding_service import EmbeddingService
from app.schemas.retrieval import RetrievalResult



class RetrievalService:

    def __init__(self,embedding_service: EmbeddingService,):
        self.embedding_service  = embedding_service


    async def retrieve(
            self,
            session:Session,
            query: str,
            repository_id: int,
            top_k: int = 5,
            document_type: str | None = None,
            language: str | None = None,
        )->list[RetrievalResult]:

        query_embedding = await self.embedding_service.embed(query)

        result =  similarity_search(
            session=session,
            repository_id=repository_id,
            query_embedding=query_embedding,
            top_k=top_k,
            document_type=document_type,
            language=language
        )

        return [
            RetrievalResult(
                content=chunk.content,
                source=chunk.source,
                document_type=chunk.document_type,
                language=chunk.language,
                chunk_index=chunk.chunk_index,
                start_line=chunk.start_line,
                end_line=chunk.end_line,
                distance=distance
            )
            for chunk,distance in result
        ]




