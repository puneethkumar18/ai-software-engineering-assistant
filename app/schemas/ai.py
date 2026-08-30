from pydantic import BaseModel, Field


class AIRequest(BaseModel): 
    repository_id:int = Field(
        ...,
        gt=0,
        description="Repository to search and answer from",
    )
    message:str = Field(
        ...,
        min_length=1,
        description="Message sent to the AI assistant",
    )

class AISource(BaseModel):
    source:str
    start_line:int | None
    end_line:int | None


class AIResponse(BaseModel):
    response:str
    sources: list[AISource]





