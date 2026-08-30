from typing import Any

from app.agent.tool_context import ToolContext
from app.tools.executor import ToolExecutor


class MCPToolAdapter:

    def __init__(
        self,
        tool_executor: ToolExecutor,
    ):
        self.tool_executor = tool_executor

    def execute(
        self,
        context: ToolContext,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> Any:

        tool_arguments = {
            **arguments,
            "repository_path": context.repository_path,
        }

        return self.tool_executor.execute(
            tool_name=tool_name,
            arguments=tool_arguments,
        )