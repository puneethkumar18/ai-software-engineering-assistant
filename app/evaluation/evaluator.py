from sqlalchemy.orm import Session

from app.evaluation.metrics import evaluate_retrieval
from app.evaluation.models import RetrievalEvaluationResult,EvaluationQuery,DatasetEvaluationResult
from app.services.retrieval_service import RetrievalService


class RetrievalEvaluator:

    def __init__(
        self,
        retrieval_service: RetrievalService,
    ):
        self.retrieval_service = retrieval_service

    async def evaluate(
        self,
        session: Session,
        query: str,
        repository_id: int,
        relevant_sources: list[str],
        top_k: int = 5,
        document_type: str | None = None,
        language: str | None = None,
    ) -> RetrievalEvaluationResult:

        results = await self.retrieval_service.retrieve(
            session=session,
            repository_id=repository_id,
            query=query,
            top_k=top_k,
            document_type=document_type,
            language=language,
        )

        return evaluate_retrieval(
            query=query,
            repository_id=repository_id,
            results=results,
            relevant_sources=relevant_sources,
        )


    async def evaluate_dataset(
        self,
        session: Session,
        dataset: list[EvaluationQuery],
        top_k: int = 5,
    ) -> DatasetEvaluationResult:

        if not dataset:
            return DatasetEvaluationResult(
                total_queries=0,
                average_precision_at_k=0.0,
                average_recall_at_k=0.0,
                mean_reciprocal_rank=0.0,
            )

        results = []

        for item in dataset:

            result = await self.evaluate(
                session=session,
                query=item.query,
                repository_id=item.repository_id,
                relevant_sources=item.relevant_sources,
                top_k=top_k,
            )

            results.append(result)

        average_precision = (
            sum(
                result.precision_at_k
                for result in results
            )
            / len(results)
        )

        average_recall = (
            sum(
                result.recall_at_k
                for result in results
            )
            / len(results)
        )

        mean_reciprocal_rank = (
            sum(
                result.reciprocal_rank
                for result in results
            )
            / len(results)
        )

        return DatasetEvaluationResult(
            total_queries=len(results),
            average_precision_at_k=average_precision,
            average_recall_at_k=average_recall,
            mean_reciprocal_rank=mean_reciprocal_rank,
        )