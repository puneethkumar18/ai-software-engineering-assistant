from app.schemas.retrieval import RetrievalResult
from app.evaluation.models import RetrievalEvaluationResult


def precision_at_k(
    retrieved: list[str],
    relevant: set[str],
) -> float:

    if not retrieved:
        return 0.0

    relevant_retrieved = sum(
        1
        for source in retrieved
        if source in relevant
    )

    return relevant_retrieved / len(retrieved)


def recall_at_k(
    retrieved: list[str],
    relevant: set[str],
) -> float:

    if not relevant:
        return 0.0

    relevant_retrieved = sum(
        1
        for source in retrieved
        if source in relevant
    )

    return relevant_retrieved / len(relevant)


def reciprocal_rank(
    retrieved: list[str],
    relevant: set[str],
) -> float:

    for rank, source in enumerate(
        retrieved,
        start=1,
    ):

        if source in relevant:
            return 1.0 / rank

    return 0.0


def evaluate_retrieval(
    query: str,
    repository_id: int,
    results: list[RetrievalResult],
    relevant_sources: list[str],
) -> RetrievalEvaluationResult:

    retrieved_sources = [
        result.source
        for result in results
    ]

    relevant = set(relevant_sources)

    return RetrievalEvaluationResult(
        query=query,
        repository_id=repository_id,
        retrieved_sources=retrieved_sources,
        relevant_sources=relevant_sources,
        precision_at_k=precision_at_k(
            retrieved=retrieved_sources,
            relevant=relevant,
        ),
        recall_at_k=recall_at_k(
            retrieved=retrieved_sources,
            relevant=relevant,
        ),
        reciprocal_rank=reciprocal_rank(
            retrieved=retrieved_sources,
            relevant=relevant,
        ),
    )