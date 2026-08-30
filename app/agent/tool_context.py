from pathlib import Path

class ToolContext:

    def __init__(self,repository_id: int,):

        if repository_id <= 0:
            raise ValueError(
                "repository_id must be greater than 0. "
            )

        self.repository_id = repository_id

    @property
    def repository_path(self)->str:

        path = (
            Path("data/cloned_repositories")
            /str(self.repository_id)
        )

        if not path.exists():
            raise ValueError(
                f"Repository {self.repository_id} "
                "has not been cloned."
            )

        if not path.is_dir():
            raise ValueError(
                f"Repository path is invalid: {path}"
            )

        return str(path)