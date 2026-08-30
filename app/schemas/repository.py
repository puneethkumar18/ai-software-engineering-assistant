from pydantic import BaseModel,Field
from datetime import datetime



class RepositoryCreateRequest(BaseModel):
    url: str = Field(
        ...,
        min_length=1,
        description="Public GitHub repository URL",
    )


class RepositoryResponse(BaseModel):
    id: int
    name: str
    url: str
    status:str
    indexed_at: datetime | None = None
    error_message: str | None = None


