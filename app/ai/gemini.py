from typing import Any

from google import genai
from google.genai import types

from app.ai.interface import LLMProvider
from app.core.config import settings


class GeminiProvider(LLMProvider):

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    async def generate(
        self,
        prompt: str,
    ) -> str:

        response = await self.client.aio.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )

        return response.text

    async def generate_with_tools(
        self,
        contents: list[Any],
        tools: list[dict[str, Any]],
    ):

        tool = types.Tool(
            function_declarations=tools
        )

        config = types.GenerateContentConfig(
            tools=[tool]
        )

        return await self.client.aio.models.generate_content(
            model="gemini-3.5-flash",
            contents=contents,
            config=config,
        )