from app.agent.agent import Agent
from app.services.embedding_service import EmbeddingService
from app.services.retrieval_service import RetrievalService
from app.ai.gemini import GeminiProvider
from app.mcp.client import MCPClient
from app.core.config import settings


def create_agent()->Agent:

    llm = GeminiProvider()

    embedding_service = EmbeddingService()

    retrieval_service = RetrievalService(
        embedding_service=embedding_service
    )

    mcp_client = MCPClient()

    return Agent(
        llm=llm,
        mcp_client=mcp_client,
        retrieval_service=retrieval_service,
        max_iterations=settings.AGENT_MAX_ITERATIONS,
        max_tool_calls = settings.AGENT_MAX_TOOL_CALLS   
    )