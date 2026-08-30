from pathlib import Path

from app.ingestion.file_filter import (
    IGNORED_DIRECTORIES,
    should_include_file,
)


def read_file(
    repository_path: str,
    file_path: str,
)->dict:

    root = Path(repository_path).resolve()

    target = (root / file_path).resolve()

    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError(
            "File path must be inside the repository."
        )from exc

    if not target.exists():
        raise ValueError(
            f"File does not exist: {file_path}"
        )

    if not target.is_file():
        raise ValueError(
            f"Path is not a file: {file_path}"
        )

    relative_parts = target.relative_to(root).parts

    if any(
        directory in IGNORED_DIRECTORIES
        for directory in relative_parts
    ):
        raise ValueError(
            "Access to ignored repository directories is not allowed."
        )

    if not should_include_file(target):
        raise ValueError(
            f"File type is not supported: {file_path}"
        )

    try:
        content = target.read_text(
            encoding="utf-8"
        )
    except UnicodeDecodeError as exc:

        raise ValueError(
            f"File is not valid UTF-8 text: {file_path}"
        ) from exc

    return {
        "source": str(
            target.relative_to(root)
        ),
        "content":content
    }