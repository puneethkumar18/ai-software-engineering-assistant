from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:

    def __init__(
        self,
        server_command: str = "python",
        server_args: list[str] | None = None,
    ):

        self.server_command = server_command

        self.server_args = (
            server_args
            if server_args is not None
            else ["-m","app.mcp.server"]
        )

        self._stdio_context = None
        self._session_context = None
        self.session: ClientSession | None = None

    async def connect(self)->None:

        server_params = StdioServerParameters(
            command=self.server_command,
            args=self.server_args
        )

        self._stdio_context = stdio_client(
            server_params
        )

        read, write =  await self._stdio_context.__aenter__()

        self._session_context = ClientSession(
            read,
            write
        )

        self.session = await (
            self._session_context.__aenter__()
        )

        await self.session.initialize()



    async def list_tools(self)->list[Any]:

        if self.session is None:
            raise RuntimeError(
                "MCP client is not connected."
            )

        result = await self.session.list_tools()

        return result.tools

    async def call_tool(
        self,
        name: str,
        arguments:dict[str, Any],
    )-> Any:

        if self.session is None:
            raise RuntimeError(
                "MCP client is not connected."
            )

        return await self.session.call_tool(
            name,
            arguments,
        )

    async def close(self)->None:

        if self._session_context is not None:
            await self._session_context.__aexit__(
                None,
                None,
                None
            )

        self._session_context = None
        self.session = None

        if self._stdio_context is not None:

            await self._stdio_context.__aexit__(
                None,
                None,
                None,
            )

            self._stdio_context = None




        

