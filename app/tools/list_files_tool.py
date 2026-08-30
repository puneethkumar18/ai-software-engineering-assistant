
from app.tools.base import Tool
from typing import Any
from app.tools.list_files import list_files
from app.tools.schemas import LIST_FILES_SCHEMA

class ListFilesTool(Tool):

    @property
    def name(self)->str:
        return  "list_files"

    @property
    def description(self):
        return (
            "List supported files inside the repository. "
            "Returns repository-relative file paths."
        )

    @property
    def schema(self):
        return LIST_FILES_SCHEMA

    def execute(self, **kwargs:Any)->list[str]:
        repository_path = kwargs.get("repository_path")

        if not repository_path:
            raise ValueError(
                "repository_path is required."
            )

        return list_files(
            repository_path=repository_path
        )
        
