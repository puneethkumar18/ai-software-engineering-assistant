from fastapi import HTTPException,APIRouter,Depends
from app.schemas.agent import AgentResponse,AgentRequest
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.core.agent_dependencies import create_agent
from app.services.agent_service import AgentService

from app.core.exceptions import (
    RepositoryNotFoundError,
    RepositoryNotReadyError,
)

import logging

logger = logging.getLogger(__name__)



router = APIRouter(prefix="/repositories",tags=["Agent"])


@router.post(
    "/{repository_id}/ask",
    response_model=AgentResponse
    )
async def ask_agent(
    repository_id:int,
    request: AgentRequest,
    session: Session = Depends(get_db),
):
    try:
        agent_service = AgentService(
            agent=create_agent()
        )

        response = await agent_service.answer(
            session=session,
            repository_id=repository_id,
            query=request.message,
        )

        return response

    except RepositoryNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail="Agent execution failed.",
        )from exc
    except Exception as exc:
        logger.exception(
            "Agent API execution failed | repository_id=%s",
            repository_id,
        )
        raise HTTPException(
            status_code=500,
            detail="Agent execution failed.",
        ) from exc