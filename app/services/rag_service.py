
from sqlalchemy.orm import Session

from app.services.ai_service import AIService
from app.services.context_service import build_context, build_rag_prompt
from app.services.retrieval_service import RetrievalService


class RAGService:

    def __init__(
        self,
        retrieval_service: RetrievalService,
        ai_service: AIService,
    ):
        self.retrieval_service = retrieval_service
        self.ai_service = ai_service

    async def generate_answer(
        self,
        session: Session,
        repository_id: int,
        query:str,
        top_k: int = 5,
        document_type: str | None = None,
        language: str | None = None,
    ):
        results = await self.retrieval_service.retrieve(
            session=session,
            repository_id=repository_id,
            query=query,
            top_k=top_k,
            document_type=document_type,
            language=language
        )

        context = build_context(results=results)

        prompt = build_rag_prompt(query=query,rag_context=context)

        answer = await self.ai_service.ask(prompt=prompt)

        return answer , results


        

