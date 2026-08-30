# from pathlib import Path

# from sqlalchemy.orm import Session

# from app.ingestion.repository import discover_files
# from app.ingestion.loader import load_documents
# from app.chunking.strategy import chunk_documents_with_strategy
# from app.embeddings.model import EmbeddedChunk
# from app.services.embedding_service import EmbeddingService
# from app.vectorstore.repository import (
#     save_embedded_chunks,
#     delete_repository_chunks
# )


# class IngestionService:

#     def __init__(
#         self,
#         embedding_service: EmbeddingService,
#     ):
#         self.embedding_service = embedding_service

#     async def ingest_repository(
#         self,
#         session: Session,
#         repository_id: int,
#         repository_path: str,
#         chunk_size: int = 500,
#         overlap: int = 50,
#     ) -> int:

#         repository_root = Path(repository_path)

#         files = discover_files(
#             repository_path=repository_path
#         )

#         documents = load_documents(
#             paths=files,
#             repository_root=repository_root,
#         )

#         chunks = chunk_documents_with_strategy(
#             documents=documents,
#             chunk_size=chunk_size,
#             overlap=overlap,
#         )

#         if not chunks:
#             return 0

#         embeddings = await self.embedding_service.batch_embed(
#             texts=[chunk.content for chunk in chunks]
#         )

#         embedded_chunks = [
#             EmbeddedChunk(
#                 repository_id=repository_id,
#                 content=chunk.content,
#                 source=chunk.source,
#                 document_type=chunk.document_type,
#                 language=chunk.language,
#                 chunk_index=chunk.chunk_index,
#                 start_line=chunk.start_line,
#                 end_line=chunk.end_line,
#                 embedding=embedding,
#             )
#             for chunk, embedding in zip(
#                 chunks,
#                 embeddings,
#                 strict=True,
#             )
#         ]

#         try:
#             delete_repository_chunks(
#                 session=session,
#                 repository_id=repository_id
#             )

#             save_embedded_chunks(
#                 session=session,
#                 embedded_chunks=embedded_chunks,
#             )

#             session.commit()

#         except Exception:
#             session.rollback()
#             raise

#         return len(embedded_chunks)






from pathlib import Path

from sqlalchemy.orm import Session

from app.ingestion.repository import discover_files
from app.ingestion.loader import load_documents
from app.chunking.strategy import chunk_documents_with_strategy
from app.embeddings.model import EmbeddedChunk
from app.services.embedding_service import EmbeddingService
from app.vectorstore.repository import (
    delete_repository_chunks,
    save_embedded_chunks,
)


class IngestionService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
    ):
        self.embedding_service = embedding_service

    async def ingest_repository(
        self,
        session: Session,
        repository_id: int,
        repository_path: str,
        chunk_size: int = 500,
        overlap: int = 50,
    ) -> int:

        repository_root = Path(repository_path)

        files = discover_files(
            repository_path=repository_path,
        )

        documents = load_documents(
            paths=files,
            repository_root=repository_root,
        )

        chunks = chunk_documents_with_strategy(
            documents=documents,
            chunk_size=chunk_size,
            overlap=overlap,
        )

        if not chunks:
            return 0

        embeddings = await self.embedding_service.batch_embed(
            texts=[
                chunk.content
                for chunk in chunks
            ]
        )

        embedded_chunks = [
            EmbeddedChunk(
                repository_id=repository_id,
                content=chunk.content,
                source=chunk.source,
                document_type=chunk.document_type,
                language=chunk.language,
                chunk_index=chunk.chunk_index,
                start_line=chunk.start_line,
                end_line=chunk.end_line,
                embedding=embedding,
            )
            for chunk, embedding in zip(
                chunks,
                embeddings,
                strict=True,
            )
        ]

        try:

            delete_repository_chunks(
                session=session,
                repository_id=repository_id,
            )

            save_embedded_chunks(
                session=session,
                embedded_chunks=embedded_chunks,
            )

            session.commit()

        except Exception:

            session.rollback()
            raise

        return len(embedded_chunks)