from pydantic import BaseModel


class Document(BaseModel):
    content: str
    source: str
    document_type: str
    language: str | None = None