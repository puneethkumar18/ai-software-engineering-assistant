from sqlalchemy.orm import Session


from app.agent.agent import Agent
from app.agent.tool_context import ToolContext


class AgentService:

    def __init__(
        self,
        agent:Agent
    ):

        self.agent = agent

    async def answer(
        self,
        session:Session,
        repository_id:int,
        query: str,  
    ):

        context = ToolContext(
            repository_id=repository_id
        )

        return await self.agent.run(
            session=session,
            query=query,
            context=context,
        )



        