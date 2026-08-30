SEARCH_CODE_SCHEMA = {
    "name": "search_code",
    "description": (
        "Search the repository for an exact text match. "
        "Returns matching file paths, line numbers, "
        "and matching lines."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": (
                    "Text to search for in the repository."
                ),
            },
        },
        "required": ["query"],
    },
}


READ_FILE_SCHEMA = {
    "name": "read_file",
    "description": (
        "Read the contents of a file inside the repository."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": (
                    "Path of the file relative to "
                    "the repository root."
                ),
            },
        },
        "required": ["file_path"],
    },
}


LIST_FILES_SCHEMA = {
    "name": "list_repository_files",
    "description": (
        "List supported files inside the repository."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "repository_id": {
                "type": "integer",
                "description": (
                    "ID of the repository."
                ),
            },
        },
        "required": [
            "repository_id",
        ],
    },
}


GET_REPOSITORY_INFO_SCHEMA = {
    "name": "get_repository_information",
    "description": (
        "Get Git repository metadata including the "
        "current branch, latest commit, latest commit "
        "message, and working tree status."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "repository_id": {
                "type": "integer",
                "description": (
                    "ID of the repository."
                ),
            },
        },
        "required": [
            "repository_id",
        ],
    },
}


CODE_STRUCTURE_SCHEMA = {
    "name": "get_python_code_structure",
    "description": (
        "Inspect the structure of a Python file. "
        "Returns classes, functions, methods, "
        "and their line numbers."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "repository_id": {
                "type": "integer",
                "description": (
                    "ID of the repository to inspect."
                ),
            },
            "file_path": {
                "type": "string",
                "description": (
                    "Path of the Python file relative "
                    "to the repository root."
                ),
            },
        },
        "required": [
            "repository_id",
            "file_path",
        ],
    },
}