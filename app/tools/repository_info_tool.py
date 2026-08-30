

from typing import Any

from app.tools.base import Tool
from app.tools.repository_info import get_repository_info
from app.tools.schemas import GET_REPOSITORY_INFO_SCHEMA


class RepositoryInfoTool(Tool):

    @property
    def name(self)->str:
        return "get_repository_info"

    @property
    def description(self):
        return (
            "Get Git repository metadata including the "
            "current branch, latest commit, latest commit "
            "message, and working tree status."
        )

    @property
    def schema(self):
        return GET_REPOSITORY_INFO_SCHEMA

    def execute(self, **kwargs):
        repository_path = kwargs.get(
            "repository_path"
        )

        if not repository_path:
            raise ValueError(
                "repository_path is required."
            )
        
        return get_repository_info(
            repository_path=repository_path
        )