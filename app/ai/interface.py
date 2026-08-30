from abc import ABC, abstractmethod
from typing import Any


class LLMProvider(ABC):

    @abstractmethod
    async def generate(self,prompt:str):
        pass

    @abstractmethod
    async def generate_with_tools(
        self,
        prompt: str,
        tools: list[dict[str, Any]],
    ):
        ...