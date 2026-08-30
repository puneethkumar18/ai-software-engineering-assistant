import shutil
import subprocess

from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.services.embedding_service import EmbeddingService
from app.services.ingestion_service import IngestionService

from app.repositories.repository import (
    create_repository,
    get_repository,
    get_repository_by_url,
    update_repository_status,
)


class RepositoryService:

    def validate_github_url(
        self,
        url: str,
    ) -> None:

        parsed = urlparse(url)

        if parsed.scheme != "https":
            raise ValueError(
                "Only HTTPS GitHub URLs are supported."
            )

        if parsed.netloc.lower() != "github.com":
            raise ValueError(
                "Only GitHub repositories are supported."
            )

    def register_repository(
        self,
        session: Session,
        url: str,
    ):

        self.validate_github_url(url)

        existing_repository = get_repository_by_url(
            session=session,
            url=url,
        )

        if existing_repository is not None:
            raise ValueError(
                "Repository has already been registered. "
                f"Repository id: {existing_repository.id}"
            )

        parsed = urlparse(url)

        repository_name = (
            parsed.path
            .strip("/")
            .removesuffix(".git")
            .split("/")[-1]
        )

        repository = create_repository(
            session=session,
            name=repository_name,
            url=url,
        )

        session.commit()
        session.refresh(repository)

        return repository

    def clone_repository(
        self,
        url: str,
        destination: str,
    ) -> Path:

        self.validate_github_url(url)

        destination_path = Path(destination)

        if destination_path.exists():
            raise ValueError(
                f"Destination already exists: {destination}"
            )

        destination_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        try:
            subprocess.run(
                [
                    "git",
                    "clone",
                    "--depth",
                    "1",
                    url,
                    str(destination_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

        except subprocess.CalledProcessError as exc:
            raise RuntimeError(
                f"Failed to clone repository: {exc.stderr}"
            ) from exc

        return destination_path

    async def process_existing_repository(
        self,
        session: Session,
        repository_id: int,
        url: str,
        chunk_size: int = 500,
        overlap: int = 50,
    ) -> None:

        repository = get_repository(
            session=session,
            repository_id=repository_id,
        )

        if repository is None:
            raise ValueError(
                f"Repository {repository_id} not found."
            )

        destination = (
            Path("data/cloned_repositories")
            / str(repository.id)
        )

        try:

            # -------------------------
            # CLONING
            # -------------------------

            repository.error_message = None

            update_repository_status(
                session=session,
                repository=repository,
                status="CLONING",
            )

            session.commit()

            repository_path = self.clone_repository(
                url=url,
                destination=str(destination),
            )

            # -------------------------
            # INDEXING
            # -------------------------

            update_repository_status(
                session=session,
                repository=repository,
                status="INDEXING",
            )

            session.commit()

            embedding_service = EmbeddingService()

            ingestion_service = IngestionService(
                embedding_service=embedding_service,
            )

            await ingestion_service.ingest_repository(
                session=session,
                repository_id=repository.id,
                repository_path=repository_path,
                chunk_size=chunk_size,
                overlap=overlap,
            )

            # -------------------------
            # READY
            # -------------------------


            repository.indexed_at = datetime.now(timezone.utc)
            repository.error_message = None

            update_repository_status(
                session=session,
                repository=repository,
                status="READY",
            )

            session.commit()

        except Exception as exc:

            session.rollback()

            try:

                repository = get_repository(
                    session=session,
                    repository_id=repository_id,
                )

                if repository is not None:
                    repository.error_message = str(exc)
                    update_repository_status(
                        session=session,
                        repository=repository,
                        status="FAILED",
                    )

                    session.commit()

            except Exception:

                session.rollback()

            if destination.exists():
                shutil.rmtree(destination)

            raise