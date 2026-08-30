from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".java",
    ".cpp",
    ".c",
    ".go",
    ".rs",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
}

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".idea",
    ".vscode",
}

IGNORED_FILES = {
    ".env",
}


def should_include_file(path:Path)->bool:

    if path.name in IGNORED_FILES:
        return False

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return False

    return True