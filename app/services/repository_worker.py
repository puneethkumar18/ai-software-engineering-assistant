from app.db.database import SessionLocal
from app.services.repository_service import RepositoryService

async def process_repository(
    repository_id: int,
    url:str
)-> None:
    
    session = SessionLocal()

    try:
        repository_service = RepositoryService()

        await repository_service.process_existing_repository(
            session=session,
            repository_id=repository_id,
            url=url,
        )

    finally:
        session.close()