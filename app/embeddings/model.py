from pydantic import BaseModel


class EmbeddedChunk(BaseModel):
    repository_id:int
    content:str
    source: str
    document_type: str
    language: str | None = None
    chunk_index: int
    start_line: int | None = None
    end_line: int | None = None
    embedding: list[float]