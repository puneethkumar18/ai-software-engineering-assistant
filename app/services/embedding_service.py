from app.embeddings.gemini import GeminiEmbeddingProvider

class EmbeddingService:

    def __init__(self):
        self.provider = GeminiEmbeddingProvider()


    async def embed(self,text:str)->list[float]:
        return await self.provider.embed(text=text)

    async def batch_embed(self,texts:list[str])->list[list[float]]:
        return await self.provider.batch_embed(texts=texts)