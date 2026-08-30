from typing import Any

from app.tools.base import Tool
from app.tools.search_code import search_code

from app.tools.schemas import SEARCH_CODE_SCHEMA


class SearchCodeTool(Tool):

    @property
    def name(self) -> str:
        return "search_code"

    @property
    def description(self) -> str:
        return (
            "Search the repository for an exact text match. "
            "Returns matching file paths, line numbers, "
            "and matching lines."
        )

    @property
    def schema(self):
        return SEARCH_CODE_SCHEMA

    def execute(self, **kwargs: Any) -> list[dict]:

        repository_path = kwargs.get("repository_path")
        query = kwargs.get("query")

        if not repository_path:
            raise ValueError(
                "repository_path is required."
            )

        if not query:
            raise ValueError(
                "query is required."
            )

        return search_code(
            repository_path=repository_path,
            query=query,
        )