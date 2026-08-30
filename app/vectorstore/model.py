from pydantic import BaseModel

class VectorRecord(BaseModel):
    content:str
    sourece:str
    document_type:str
    language: str | None = None
    chunk_index: int
    start_line: int | None = None
    end_line: int | None = None
    embedding: list[float]