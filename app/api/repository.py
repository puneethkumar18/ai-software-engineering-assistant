from fastapi import APIRouter,Depends,HTTPException,BackgroundTasks

from app.schemas.repository import RepositoryCreateRequest,RepositoryResponse

from app.services.repository_worker import process_repository

from app.services.repository_service import RepositoryService

from app.core.dependencies import get_db

from app.repositories.repository import get_repository

from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/repositories",
    tags=["repositories"],
)


@router.post("",response_model=RepositoryResponse)
async def create_repository(
    request:RepositoryCreateRequest,
    background_tasks: BackgroundTasks,
    session:Session=Depends(get_db)
    ):

    repository_service = RepositoryService()

    try:
        repository = (
            repository_service.register_repository(
                session=session,
                url=request.url
            )
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    
    except RuntimeError as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    background_tasks.add_task(
        process_repository,
        repository.id,
        repository.url
    )

    return RepositoryResponse(
        id=repository.id,
        name=repository.name,
        url=repository.url,
        status=repository.status,
        indexed_at=repository.indexed_at,
        error_message=repository.error_message,
    )


@router.get("/{repository_id}",response_model=RepositoryResponse)
async def get_repository_status(
    repository_id: int,
    session:Session=Depends(get_db)
):
    repository = get_repository(
        session=session,
        repository_id=repository_id
    )

    if repository is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found.",
        )

    return RepositoryResponse(
        id=repository.id,
        name=repository.name,
        url=repository.url,
        status=repository.status,
        indexed_at=repository.indexed_at,
        error_message=repository.error_message
    )