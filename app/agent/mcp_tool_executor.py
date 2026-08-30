from typing import Any

from app.mcp.client import MCPClient

class MCPAgentToolExecutor:

    def __int__(
        self,
        client:MCPClient
    ):
        self.client = client


    async def excecute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    )->Any:
        self.client.call_tool(
            name=tool_name,
            arguments=arguments
        )
        