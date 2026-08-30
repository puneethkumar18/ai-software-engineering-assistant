from sqlalchemy.orm import Session
from sqlalchemy import select,delete

from app.db.models.vector_chunk import VectorChunk
from app.embeddings.model import EmbeddedChunk


def save_embedded_chunk(
       session: Session,
       embedded_chunk: EmbeddedChunk
):

    vector_chunk = VectorChunk(
        repository_id=embedded_chunk.repository_id,
        content=embedded_chunk.content,
        source=embedded_chunk.source,
        document_type=embedded_chunk.document_type,
        language=embedded_chunk.language,
        chunk_index=embedded_chunk.chunk_index,
        start_line=embedded_chunk.start_line,
        end_line=embedded_chunk.end_line,
        embedding=embedded_chunk.embedding,
    )


    session.add(vector_chunk)
    session.commit()
    session.refresh(vector_chunk)

    return vector_chunk

def save_embedded_chunks(
    session: Session,
    embedded_chunks: list[EmbeddedChunk],
)-> list[VectorChunk]:

    if not embedded_chunks:
        return []

    vector_chunks = [
        VectorChunk(
            repository_id=embedded_chunk.repository_id,
            content=embedded_chunk.content,
            source=embedded_chunk.source,
            document_type=embedded_chunk.document_type,
            language=embedded_chunk.language,
            chunk_index=embedded_chunk.chunk_index,
            start_line=embedded_chunk.start_line,
            end_line=embedded_chunk.end_line,
            embedding=embedded_chunk.embedding,
        )

        for embedded_chunk in embedded_chunks
    ]

    session.add_all(vector_chunks)

    session.flush()

    for vector_chunk in vector_chunks:
        session.refresh(vector_chunk)

    return vector_chunks


def delete_repository_chunks(
    session:Session,
    repository_id: int,
) -> int:


    statement = (
        delete(VectorChunk).where(
            VectorChunk.repository_id==repository_id
        )
    )
    result = session.execute(statement)

    return result.rowcount



def similarity_search(
        session: Session,
        repository_id:int,
        query_embedding: list[float],
        top_k: int = 5,
        document_type: str | None = None,
        language: str | None = None,
    )-> list[tuple[VectorChunk, float]]:


    if not query_embedding:
        return []

    if repository_id <= 0:
        raise ValueError(
            "repository_id must be greater than 0"
        )

    if top_k <= 0:
        raise ValueError("top_k must be greater than 0")

    distance = VectorChunk.embedding.cosine_distance(
        query_embedding
    )

    statement = (
        select(
            VectorChunk,
            distance.label("distance"),
        ).where(
            VectorChunk.repository_id == repository_id
        )
    )

    if document_type is not None:
        statement = statement.where(
            VectorChunk.document_type == document_type
        )

    if language is not None:
        statement = statement.where(
            VectorChunk.language == language
        )

    statement = (
        statement
        .order_by(distance)
        .limit(top_k)
    )

    results = session.execute(statement).all()


    return [
        (vector_chunk,float(distance))
        for vector_chunk,distance in results
    ]
    