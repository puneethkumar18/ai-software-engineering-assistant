
from app.tools.base import Tool
from app.tools.code_structure import get_code_structure
from app.tools.schemas import CODE_STRUCTURE_SCHEMA

class CodeStructureTool(Tool):

    @property
    def name(self)->str:
        return "get_code_structure"

    @property
    def description(self):
        return (
            "Inspect the structure of a Python file. "
            "Returns classes, functions, methods, and "
            "their line numbers."
        )

    @property
    def schema(self):
        return CODE_STRUCTURE_SCHEMA

    def execute(self, **kwargs):
        repository_path = kwargs.get(
            "repository_path"
        )

        file_path = kwargs.get(
            "file_path"
        )

        if not repository_path:
            raise ValueError(
                "repository_path is required."
            )

        if not file_path:
            raise ValueError(
                "file_path is required."
            )

        
        return get_code_structure(
            repository_path=repository_path,
            file_path=file_path
        )