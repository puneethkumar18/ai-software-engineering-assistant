from typing import Any

from app.tools.base import Tool
from app.tools.read_file import read_file
from app.tools.schemas import READ_FILE_SCHEMA

class ReadFileTool(Tool):

    @property
    def name(self) -> str:
        return "read_file"

    @property
    def description(self) -> str:
        return (
            "Read the contents of a file inside "
            "the repository."
        )

    @property
    def schema(self):
        return READ_FILE_SCHEMA

    def execute(self, **kwargs: Any) -> dict:

        repository_path = kwargs.get("repository_path")
        file_path = kwargs.get("file_path")

        if not repository_path:
            raise ValueError(
                "repository_path is required."
            )

        if not file_path:
            raise ValueError(
                "file_path is required."
            )

        return read_file(
            repository_path=repository_path,
            file_path=file_path,
        )