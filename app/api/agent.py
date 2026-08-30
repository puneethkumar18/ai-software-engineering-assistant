from fastapi import HTTPException,APIRouter,Depends
from app.schemas.agent import AgentResponse,AgentRequest
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.core.agent_dependencies import create_agent
from app.agent.tool_context import ToolContext
from app.services.agent_service import AgentService



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

        result = await agent_service.answer(
            session=session,
            repository_id=repository_id,
            query=request.message,
        )

        return AgentResponse(
            answer=result.answer,
            tool_calls=result.tool_calls,
            tools_used=result.tools_used
        )
    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc)
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc