from app.tools.base import Tool
from app.tools.read_file_tool import ReadFileTool
from app.tools.search_code_tool import SearchCodeTool
from app.tools.list_files_tool import ListFilesTool
from app.tools.repository_info_tool import RepositoryInfoTool
from app.tools.code_structure_tool import CodeStructureTool

class ToolRegistry:

    def __init__(self):
        self._tools : dict[str,Tool] = {}

        self.register(
            SearchCodeTool()
        )

        self.register(
            ReadFileTool()
        )

        self.register(
            ListFilesTool()
        )

        self.register(
            RepositoryInfoTool()
        )

        self.register(
            CodeStructureTool()
        )

    def register(self, tool:Tool):

        if tool.name in self._tools:
            raise ValueError(
                f"Tool already registered: {tool.name}"
            )

        self._tools[tool.name] = tool


    def get(self,name:str):
        tool = self._tools.get(name)

        if tool is None:
            raise ValueError(
                f"Tool not found: {name}"
            )
        return tool

    def schemas(self):
        return [
            tool.schema
            for tool in self._tools.values()
        ]

    def list_tools(self)-> list[Tool]:
        return list(
            self._tools.values()
        )
