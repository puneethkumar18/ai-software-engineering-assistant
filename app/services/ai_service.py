from app.ai.gemini import GeminiProvider

class AIService:

    def __init__(self):
        self.llm = GeminiProvider()


    async def ask(self,prompt:str)->str:
        return await self.llm.generate(prompt=prompt)
