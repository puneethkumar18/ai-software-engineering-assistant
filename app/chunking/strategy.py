from app.ingestion.document import Document
from collections.abc import Callable
from app.chunking.text import check_document_with_lines
from app.chunking.code import (
    chunk_python_document,
    chunk_cpp_document
    )
from app.chunking.chunk import Chunk

def select_chunker(document: Document)->str:
    if document.document_type == "code":
        return "code"
    return "text"


def chunk_with_strategy(document:Document,chunk_size:int=500,overlap:int=50)->list[Chunk]:

    strategy = select_chunker(document)

    if strategy == "text":
        return check_document_with_lines(
            document=document,
            chunk_size=chunk_size,
            overlap=overlap
        )

    if strategy == "code": 
        if document.language == "python":
            return chunk_python_document(document=document)
        elif document.language == "cpp":
            return chunk_cpp_document(document=document)

    raise NotImplementedError(
        f"Chunking strategy '{strategy}' is not implemented yet."
        f"language='{document.language}'"
    )


def chunk_documents_with_strategy(
        documents:list[Document],
        chunk_size:int=500,
        overlap:int=50
)->list[Chunk]:

    chunks = []
    print("files count : ", len(documents))
    for document in documents:
        document_chunks = chunk_with_strategy(
            document=document,
            chunk_size=chunk_size,
            overlap=overlap)
        chunks.extend(document_chunks)

    print("chunks_count: ", len(chunks))

    return chunks

    



