from pydantic import BaseModel


class EvaluationQuery(BaseModel):
    query: str
    repository_id: int
    relevant_sources: list[str]


class RetrievalEvaluationResult(BaseModel):
    query: str
    repository_id: int
    retrieved_sources: list[str]
    relevant_sources: list[str]
    precision_at_k: float
    recall_at_k: float
    reciprocal_rank: float


class DatasetEvaluationResult(BaseModel):
    total_queries: int
    average_precision_at_k: float
    average_recall_at_k: float
    mean_reciprocal_rank: float