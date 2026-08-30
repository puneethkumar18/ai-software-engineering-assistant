from pathlib import Path

from app.ingestion.file_filter import (
    IGNORED_DIRECTORIES,
    should_include_file,
)


def discover_files(repository_path: str) -> list[Path]:
    root = Path(repository_path)

    if not root.exists():
        raise ValueError(f"Repository path does not exist: {repository_path}")

    if not root.is_dir():
        raise ValueError(f"Repository path is not a directory: {repository_path}")

    discovered_files = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        relative_parts = path.relative_to(root).parts

        if any(
            directory in IGNORED_DIRECTORIES
            for directory in relative_parts[:-1]
        ):
            continue

        if should_include_file(path):
            discovered_files.append(path)


    return discovered_files