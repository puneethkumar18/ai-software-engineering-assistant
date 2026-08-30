
from app.mcp.client import MCPClient
from typing import Any

async def get_mcp_tool_schemas(
    client: MCPClient,

)->list[dict[str,Any]]:
    tools = await client.list_tools()

    schemas = []

    for tool in tools:
        schemas.append(
            {
                "name":tool.name,
                "description":tool.description,
                "parameters": tool.input_schema,
            }
        )

    return schemas