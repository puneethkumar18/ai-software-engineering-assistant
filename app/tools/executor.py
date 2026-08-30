from typing import Any

from app.tools.registry import ToolRegistry


class ToolExecutor:

    def __init__(
        self,
        registry: ToolRegistry,
    ):
        self.registry = registry

    def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> Any:

        tool = self.registry.get(tool_name)

        return tool.execute(**arguments)