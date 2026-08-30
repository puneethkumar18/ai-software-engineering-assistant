
from pydantic import BaseModel


class Chunk(BaseModel):
    content:str
    source:str
    document_type: str
    language: str | None = None
    chunk_index:int
    start_line: int | None = None
    end_line: int | None = None