from google import genai

from app.core.config import settings
from app.embeddings.interface import EmbeddingProvider


class GeminiEmbeddingProvider(EmbeddingProvider):

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    async def embed(self, text):
        response = await self.client.aio.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )

        return response.embeddings[0].values


    async def batch_embed(self, texts)-> list[list[float]]:

        final_response = []
        for i in range(0,len(texts),99):
            batched_text = texts[i:i+99]
            response = await self.client.aio.models.embed_content(
                model="gemini-embedding-001",
                contents=batched_text
            )

            final_response.extend(
                embeddings.values
                for embeddings in response.embeddings
            )
            
        
        return final_response
        