from pathlib import Path

from app.ingestion.document import Document

LANGUAGE_BY_EXTENSION = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".cpp": "cpp",
    ".c": "c",
    ".go": "go",
    ".rs": "rust",
}


def load_document(path:Path,repository_root: Path):
    content = path.read_text(encoding="utf-8")

    relative_path = path.relative_to(repository_root)

    if path.suffix.lower() in LANGUAGE_BY_EXTENSION:
        document_type = 'code'
        language = LANGUAGE_BY_EXTENSION[path.suffix.lower()]

    else:
        document_type = "documentation"
        language = None

    return Document(
        content=content,
        document_type=document_type,
        source=str(relative_path),
        language=language
    )


def load_documents(paths:list[Path],repository_root:Path)->list[Document]:

    documents = []

    for path in paths:
        document = load_document(path,repository_root)

        documents.append(document)
        
    return documents


    