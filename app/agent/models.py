from pydantic import BaseModel


class AgentResponse(BaseModel):
    answer: str
    tool_calls: int = 0
    tools_used:list[str]