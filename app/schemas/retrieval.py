from pydantic import BaseModel,Field

class RetrievalResult(BaseModel):
    content: str
    source: str
    document_type: str
    language: str | None = None
    chunk_index: int
    start_line: int | None = None
    end_line: int | None = None
    distance: float


class RetrievalRequest(BaseModel):
    repository_id:int = Field(
        ...,
        gt=0
    )
    query:str = Field(
        ...,
        min_length=1,
        description="Question or search query",
    )

    tok_k:int=Field(
        default=5,
        ge=1,
        le=20,
        description="Number of results to retrieve",
    )
    document_type: str | None = None

    language:str | None = None