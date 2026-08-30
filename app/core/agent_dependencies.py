from app.agent.agent import Agent
from app.services.embedding_service import EmbeddingService
from app.services.retrieval_service import RetrievalService
from app.ai.gemini import GeminiProvider
from app.mcp.client import MCPClient


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
        
    )