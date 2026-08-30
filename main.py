import asyncio

from app.mcp.client import MCPClient


async def main():

    client = MCPClient()

    try:

        await client.connect()

        tools = await client.list_tools()

        print("\nAVAILABLE MCP TOOLS\n")

        for tool in tools:
            print(
                f"{tool.name}: "
                f"{tool.description}"
            )

        result = await client.call_tool(
            name="search_repository_code",
            arguments={
                "repository_id": 22,
                "query": "authentication",
            },
        )

        print("\nTOOL RESULT\n")

        print(result)

    finally:

        await client.close()


if __name__ == "__main__":
    asyncio.run(main())