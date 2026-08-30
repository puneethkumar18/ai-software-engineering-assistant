from abc import ABC, abstractmethod

class EmbeddingProvider():

    @abstractmethod
    async def embed(self, text:str)->list[float]:
        pass

    @abstractmethod
    async def batch_embed(self,texts: list[str])->list[list[float]]:
        pass