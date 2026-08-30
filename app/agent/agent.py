from typing import Any

from google.genai import types

from app.ai.interface import LLMProvider
from app.agent.models import AgentResponse
from app.agent.tool_context import ToolContext
from app.mcp.client import MCPClient
from app.services.retrieval_service import RetrievalService
from app.services.context_service import build_context,build_rag_prompt
from app.agent.mcp_tools import get_mcp_tool_schemas

from sqlalchemy.orm import Session


class Agent:

    def __init__(
        self,
        llm: LLMProvider,
        retrieval_service: RetrievalService,
        mcp_client: MCPClient,
        max_iterations: int = 5,
    ):
        self.llm = llm
        self.mcp_client = mcp_client
        self.retrieval_service= retrieval_service
        self.max_iterations = max_iterations

    async def run(
        self,
        session: Session,
        query: str,
        context: ToolContext,
    ):
        await self.mcp_client.connect()

        try:
            return await self._run(
                query=query,
                session=session,
                context=context
            )
        finally:
            await self.mcp_client.close()

    async def _run(
        self,
        query: str,
        session:Session,
        context: ToolContext,
    ) -> AgentResponse:
        retrival_results = (
            await self.retrieval_service.retrieve(
                session=session,
                query=query,
                repository_id=context.repository_id,
                top_k=5,
            )
        )

        rag_context = build_context(
            results=retrival_results
        )

        prompt = build_rag_prompt(
            query=query,
            rag_context=rag_context,
        )

        contents: list[Any] = [
            prompt
        ]

        tool_calls = 0

        tools_used = []

        tool_schemas = await get_mcp_tool_schemas(
            client=self.mcp_client
        )

        for _ in range(self.max_iterations):

            response = await self.llm.generate_with_tools(
                contents=contents,
                tools=tool_schemas
            )

            model_content = response.candidates[0].content

            contents.append(model_content)

            function_calls = [
                part.function_call
                for part in model_content.parts
                if part.function_call is not None
            ]

            if not function_calls:

                return AgentResponse(
                    answer=response.text or "",
                    tool_calls=tool_calls,
                    tools_used=tools_used
                )

            function_response_parts = []

            for function_call in function_calls:

                tool_calls += 1

                tools_used.append(
                    function_call.name
                )

                arguments = dict(
                    function_call.args
                )

                arguments["repository_id"] = (
                    context.repository_id
                )

                try:
                    result = await self.mcp_client.call_tool(
                        name=function_call.name,
                        arguments=arguments
                    )

                    result = self._serialize_tool_result(
                        result
                    )

                except Exception as exc:
                    result = {
                        "error": str(exc)
                    }

                function_response_parts.append(
                    types.Part.from_function_response(
                        name=function_call.name,
                        response={
                            "result": result
                        },
                    )
                )

            contents.append(
                types.Content(
                    role="user",
                    parts=function_response_parts,
                )
            )

        raise RuntimeError(
            "Agent exceeded maximum tool iterations."
        )



    def _serialize_tool_result(
        self,
        result: Any,
    ) -> Any:

        if hasattr(result, "content"):

            serialized = []

            for item in result.content:

                if hasattr(item, "text"):
                    serialized.append(item.text)
                else:
                    serialized.append(str(item))

            return serialized

        return result
