import ast
from pathlib import Path

from app.ingestion.file_filter import (
    IGNORED_DIRECTORIES,
    should_include_file,
)


def get_code_structure(
    repository_path: str,
    file_path: str,
) -> dict:

    root = Path(repository_path).resolve()
    target = (root / file_path).resolve()

    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError(
            "File path must be inside the repository."
        ) from exc

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

    if target.suffix != ".py":
        raise ValueError(
            "Code structure is currently supported only for Python files."
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

    try:
        tree = ast.parse(content)
    except SyntaxError as exc:
        raise ValueError(
            f"Unable to parse Python file: {file_path}"
        ) from exc

    classes = []
    functions = []
    methods = []

    for node in tree.body:

        if isinstance(node, ast.ClassDef):

            classes.append(
                {
                    "name": node.name,
                    "line": node.lineno,
                }
            )

            for child in node.body:

                if isinstance(
                    child,
                    (
                        ast.FunctionDef,
                        ast.AsyncFunctionDef,
                    ),
                ):
                    methods.append(
                        {
                            "class": node.name,
                            "name": child.name,
                            "line": child.lineno,
                        }
                    )

        elif isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):
            functions.append(
                {
                    "name": node.name,
                    "line": node.lineno,
                }
            )

    return {
        "source": str(
            target.relative_to(root)
        ),
        "classes": classes,
        "functions": functions,
        "methods": methods,
    }