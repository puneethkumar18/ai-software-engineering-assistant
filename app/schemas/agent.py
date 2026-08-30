from pydantic import BaseModel, Field

class AgentResponse(BaseModel):
    answer:str
    tool_calls:int
    tools_used:list[str]


class AgentRequest(BaseModel):
    message:str = Field(
        ...,
        min_length=1,
        description="Question about the repository",
    )