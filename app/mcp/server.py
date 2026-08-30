from mcp.server import MCPServer

from app.agent.tool_context import ToolContext
from app.mcp.adapter import MCPToolAdapter
from app.tools.executor import ToolExecutor
from app.tools.registry import ToolRegistry


mcp = MCPServer(
    "AI Software Engineering Assistant"
)


registry = ToolRegistry()

executor = ToolExecutor(
    registry=registry,
)

adapter = MCPToolAdapter(
    tool_executor=executor,
)


@mcp.tool()
def search_repository_code(
    repository_id: int,
    query: str,
) -> list[dict]:

    context = ToolContext(
        repository_id=repository_id,
    )

    return adapter.execute(
        context=context,
        tool_name="search_code",
        arguments={
            "query": query,
        },
    )


@mcp.tool()
def read_repository_file(
    repository_id: int,
    file_path: str,
) -> dict:

    context = ToolContext(
        repository_id=repository_id,
    )

    return adapter.execute(
        context=context,
        tool_name="read_file",
        arguments={
            "file_path": file_path,
        },
    )


@mcp.tool()
def list_repository_files(
    repository_id:int
)->list[str]:

    context = ToolContext(
        repository_id=repository_id,
    )

    return adapter.execute(
        context=context,
        tool_name="list_files",
        arguments={}
    )

@mcp.tool()
def get_repository_information(
    repository_id: int,
)->dict:

    context = ToolContext(
        repository_id=repository_id
    )

    return adapter.execute(
        context=context,
        tool_name="get_repository_info",
        arguments={},
    )

@mcp.tool()
def get_python_code_structure(
    repository_id:int,
    file_path:str
)->dict:
    context = ToolContext(
        repository_id=repository_id
    )
    return adapter.execute(
        context=context,
        tool_name="get_code_structure",
        arguments= {
            "file_path":file_path
        }
    ) 


if __name__ == "__main__":
    mcp.run()