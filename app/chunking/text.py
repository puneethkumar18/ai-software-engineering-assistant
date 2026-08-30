from app.ingestion.document import Document
from app.chunking.chunk import Chunk

def chunk_text(text:str,chunk_size:int=500,overlap:int=50)->list[str]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap cannot be negative")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []

    start = 0

    while start < len(text):
        end = start+chunk_size

        chunk = text[start:end]

        if chunk:
            chunks.append(chunk)

        start += chunk_size-overlap

    return chunks


def chunk_document(document:Document,chunk_size:int=500,overlap:int=50)->list[Chunk]:
    text_chunks = chunk_text(document.content,chunk_size,overlap)


    chunks = []

    for index, content in enumerate(text_chunks):
        chunk = Chunk(
            content=content,
            source=document.source,
            document_type=document.document_type,
            language=document.language,
            chunk_index=index
        )

        chunks.append(chunk)

    return chunks


def chunk_documents(documents:list[Document],chunk_size:int=500,overlap:int=50)->list[Chunk]:
    chunks = []
    for document in documents:
        document_chunks = chunk_document(document,chunk_size=chunk_size,overlap=overlap)

        chunks.extend(document_chunks)

    return chunks

def check_document_with_lines(document:Document,chunk_size:int=500,overlap:int=50):
    document_chunks = chunk_document(document,chunk_size,overlap)

    chunks = []

    current_position = 0

    for index,chunk in enumerate(document_chunks):
        start_position = current_position

        end_position = start_position + len(chunk.content)

        start_line = document.content.count("/n",0,start_position)+1

        end_line = document.content.count("/n",0,end_position,)+1

        chunk.start_line = start_line

        chunk.end_line = end_line

        chunks.append(
            chunk
        )

    current_position += chunk_size - overlap

    return chunks

