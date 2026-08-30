import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "app.mcp.server"],
    )

    async with stdio_client(server_params) as (
        read,
        write,
    ):
        async with ClientSession(
            read,
            write,
        ) as session:

            await session.initialize()

            tools = await session.list_tools()

            print("\nMCP TOOLS\n")

            for tool in tools.tools:
                print(
                    f"{tool.name}: "
                    f"{tool.description}"
                )

            print("\n")

            result = await session.call_tool(
                "search_repository_code",
                {
                    "repository_id": 22,
                    "query": "authentication",
                },
            )   

            print("\nSEARCH RESULT\n")

            print(result)

            file_result = await session.call_tool(
                "read_repository_file",
                {
                    "repository_id":31,
                    "file_path": "app/main.py",
                },
            )

            print("\nREAD FILE RESULT\n")

            print(file_result)

            result = await session.call_tool(
                name="list_repository_files",
                arguments={
                    "repository_id": 31,
                },
            )

            print("\nLIST FILES RESULT\n")
            print(result)

            result = await session.call_tool(
                name="get_repository_information",
                arguments={
                    "repository_id": 22,
                },
            )

            print("\nREPOSITORY INFO\n")
            print(result)

            result = await session.call_tool(
                name="get_python_code_structure",
                arguments={
                    "repository_id": 31,
                    "file_path": "app/services/context_service.py",
                },
            )

            print("\nCODE STRUCTURE RESULT\n")
            print(result)



if __name__ == "__main__":
    asyncio.run(main())