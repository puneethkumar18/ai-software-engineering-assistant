from typing import Any
import logging
import asyncio
from google.genai import types
from sqlalchemy.orm import Session

from app.ai.interface import LLMProvider
from app.agent.mcp_tools import get_mcp_tool_schemas
from app.agent.models import AgentResponse
from app.agent.tool_context import ToolContext
from app.mcp.client import MCPClient
from app.services.context_service import (
    build_context,
    build_rag_prompt,
)
from app.services.retrieval_service import RetrievalService


logger = logging.getLogger(__name__)


class Agent:

    def __init__(
        self,
        llm: LLMProvider,
        retrieval_service: RetrievalService,
        mcp_client: MCPClient,
        max_iterations: int = 5,
        max_tool_calls: int = 10,
    ):
        self.llm = llm
        self.retrieval_service = retrieval_service
        self.mcp_client = mcp_client
        self.max_iterations = max_iterations
        self.max_tool_calls = max_tool_calls

    async def run(
        self,
        session: Session,
        query: str,
        context: ToolContext,
    ) -> AgentResponse:

        logger.info(
            "Agent started | repository_id=%s",
            context.repository_id,
        )

        await self.mcp_client.connect()

        try:
            return await self._run(
                query=query,
                session=session,
                context=context,
            )
        finally:
            await self.mcp_client.close()

    async def _run(
        self,
        query: str,
        session: Session,
        context: ToolContext,
    ) -> AgentResponse:

        retrieval_results = (
            await self.retrieval_service.retrieve(
                session=session,
                query=query,
                repository_id=context.repository_id,
                top_k=5,
            )
        )

        rag_context = build_context(
            results=retrieval_results
        )

        prompt = build_rag_prompt(
            query=query,
            rag_context=rag_context,
        )

        contents: list[Any] = [prompt]

        tool_calls = 0
        tools_used: list[str] = []

        tool_schemas = await get_mcp_tool_schemas(
            client=self.mcp_client
        )

        for _ in range(self.max_iterations):
            try:
                response = await self.llm.generate_with_tools(
                    contents=contents,
                    tools=tool_schemas,
                )
            except asyncio.TimeoutError as exc:
                logger.error(
                    "LLM request timed out | repository_id=%s",
                    context.repository_id,
                )

                raise RuntimeError(
                    "LLM request timed out."
                )from exc

            if not response.candidates:
                raise RuntimeError(
                    "LLM returned no candidates."
                )

            model_content = response.candidates[0].content

            contents.append(model_content)

            function_calls = [
                part.function_call
                for part in model_content.parts
                if part.function_call is not None
            ]

            if not function_calls:

                logger.info(
                    "Agent completed | repository_id=%s | tool_calls=%s",
                    context.repository_id,
                    tool_calls,
                )
                return AgentResponse(
                    answer=response.text or "",
                    tool_calls=tool_calls,
                    tools_used=tools_used,
                )

            function_response_parts = []

            for function_call in function_calls:

                tool_calls += 1

                if tool_calls > self.max_tool_calls:
                    logger.warning(
                        "Agent exceeded maximum tool calls | "
                        "repository_id=%s",
                        context.repository_id,
                    )
                    raise RuntimeError(
                        "Agent exceeded maximum tool calls."
                    )

                tool_name = function_call.name

                if tool_name not in tools_used:
                    tools_used.append(tool_name)

                arguments = dict(function_call.args)

                arguments["repository_id"] = (
                    context.repository_id
                )

                try:
                    self._validate_tool_arguments(
                        tool_name=tool_name,
                        arguments=arguments,
                        tool_schemas=tool_schemas
                    )
                except ValueError as exc:

                    logger.warning(
                        "Invalid tool arguments | tool=%s | error=%s",
                        tool_name,
                        str(exc),
                    )

                    result = {
                        "error": str(exc)
                    }
                    function_response_parts.append(
                        types.Part.from_function_response(
                            name=tool_name,
                            response={
                                "result": result
                            },
                        )
                    )

                    continue

                logger.info(
                    "Agent calling tool | tool=%s | repository_id=%s",
                    tool_name,
                    context.repository_id,
                )

                try:

                    result = await self.mcp_client.call_tool(
                        name=tool_name,
                        arguments=arguments,
                    )

                    result = self._serialize_tool_result(
                        result
                    )

                    logger.info(
                        "Tool completed | tool=%s | repository_id=%s",
                        tool_name,
                        context.repository_id,
                    )

                except Exception as exc:

                    logger.exception(
                        "Tool execution failed | tool=%s | repository_id=%s",
                        tool_name,
                        context.repository_id,
                    )

                    result = {
                        "error": str(exc)
                    }

                function_response_parts.append(
                    types.Part.from_function_response(
                        name=tool_name,
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

    

    @staticmethod
    def _serialize_tool_result(
        result: Any,
    ) -> Any:

        if not hasattr(result, "content"):
            return result

        serialized = []

        for item in result.content:

            if hasattr(item, "text"):
                serialized.append(item.text)

            else:
                serialized.append(str(item))

        return serialized



    def _validate_tool_arguments(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        tool_schemas: list[dict[str, Any]],
    ) -> None:

        if not isinstance(arguments, dict):
            raise ValueError(
                "Tool arguments must be an object."
            )

        schema = next(
            (
                tool
                for tool in tool_schemas
                if tool["name"] == tool_name
            ),
            None,
        )

        if schema is None:
            raise ValueError(
                f"Unknown tool: {tool_name}"
            )

        parameters = schema.get(
            "parameters",
            {},
        )

        properties = parameters.get(
            "properties",
            {},
        )

        required = parameters.get(
            "required",
            [],
        )

        for parameter in required:

            if parameter not in arguments:
                raise ValueError(
                    f"Missing required argument: {parameter}"
                )

            if arguments[parameter] is None:
                raise ValueError(
                    f"Argument cannot be null: {parameter}"
                )

        unknown_arguments = (
            set(arguments)
            - set(properties)
        )

        if unknown_arguments:
            raise ValueError(
                "Unknown tool arguments: "
                + ", ".join(sorted(unknown_arguments))
            )