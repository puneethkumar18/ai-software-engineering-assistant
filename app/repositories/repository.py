from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models.repository import Repository


def update_repository_status(
    session:Session,
    repository: Repository,
    status:str
)->Repository:

    repository.status = status
    session.commit()
    session.refresh(repository)

    return repository

def create_repository(
    session:Session,
    name: str,
    url: str,
)->Repository:

    repository = Repository(
        name=name,
        url=url
    )

    session.add(repository)
    session.commit()
    session.refresh(repository)

    return repository

def get_repository(
    session: Session,
    repository_id: int,
)->Repository|None:
    statement = select(Repository).where(
        Repository.id == repository_id
    )

    return session.scalar(statement)


def get_repository_by_url(
    session: Session,
    url: str,
) -> Repository | None:

    statement = select(Repository).where(
        Repository.url == url
    )

    return session.scalar(statement=statement)
    
