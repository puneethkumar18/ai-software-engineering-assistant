from sqlalchemy.orm import Session


from app.agent.agent import Agent
from app.agent.tool_context import ToolContext
from app.repositories.repository import get_repository

from app.core.exceptions import (
    RepositoryNotFoundError,
    RepositoryNotReadyError,
)

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

        repository = get_repository(
            session=session,
            repository_id=repository_id,
        )

        if repository is None:
            raise RepositoryNotFoundError(
                "Repository not found."
            )

        if repository.status != "COMPLETED":
            raise RepositoryNotReadyError(
                "Repository is not ready for analysis."
            )

        context = ToolContext(
            repository_id=repository_id
        )

        return await self.agent.run(
            session=session,
            query=query,
            context=context,
        )



        