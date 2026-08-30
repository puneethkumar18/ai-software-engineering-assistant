
from app.chunking.chunk import Chunk
from app.embeddings.model import EmbeddedChunk
from app.services.embedding_service import EmbeddingService


async def embed_chunk(
        chunk:Chunk,
        embedding_service: EmbeddingService,
)->EmbeddedChunk:

    embedding = await embedding_service.embed(chunk.content)

    return EmbeddedChunk(
        content=chunk.content,
        source=chunk.source,
        document_type=chunk.document_type,
        language=chunk.language,
        chunk_index=chunk.chunk_index,
        start_line=chunk.start_line,
        end_line=chunk.end_line,
        embedding=embedding
    )


async def embed_chunks(
        chunks:list[Chunk],
        embedding_service: EmbeddingService,
)->list[EmbeddedChunk]:

    if not chunks:
        return []

    texts = [chunk.content for chunk in chunks]

    total_embeddings = []
    
    embeddings = await embedding_service.batch_embed(texts)



    if len(total_embeddings) != len(chunks):
        raise ValueError(
            "Number of embeddings does not match number of chunks"
        )

    embedded_chunks = []

    for chunk, embedding in zip(chunks,embeddings):
        embedded_chunks.append(
            EmbeddedChunk(
                content=chunk.content,
                source=chunk.source,
                document_type=chunk.document_type,
                language=chunk.language,
                chunk_index=chunk.chunk_index,
                start_line=chunk.start_line,
                end_line=chunk.end_line,
                embedding=embedding,
            )
        )

    return embedded_chunks

    