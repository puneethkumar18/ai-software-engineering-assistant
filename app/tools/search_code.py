from pathlib import Path

from app.ingestion.file_filter import IGNORED_DIRECTORIES,should_include_file


def search_code(
    repository_path: str,
    query: str,
)->list[dict]:

    if not query.strip():
        raise ValueError(
            "Search query cannot be empty."
        )

    root = Path(repository_path)

    if not root.exists():
        raise ValueError(
            f"Repository path does not exist: {repository_path}"
        )

    if not root.is_dir():
        raise ValueError(
            f"Repository path is not a directory: {repository_path}"
        )

    results = []

    for path in root.rglob("*"):

        if not path.is_file():
            continue

        relative_parts = path.relative_to(root).parts


        if any(
            directory in IGNORED_DIRECTORIES
            for directory in relative_parts
        ):
            continue

        if not should_include_file(path):
            continue

        try:
            lines = path.read_text(
                encoding="utf-8"
            ).splitlines()

        except (UnicodeDecodeError, OSError):

            continue

        for line_number, line in enumerate(lines,start=1):
            if query.lower() in line.lower():
                results.append(
                    {
                        "source":str(path.relative_to(root)),
                        "line":line_number,
                        "content": line.strip(),
                    }
                )

    return results

    