import requests
from openai import OpenAI 

class OpenRouterLLM:
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1"
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )

    async def generate(self, prompt: str) -> str:
        completion = self.client.chat.completions.create(
            model = self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return completion.choices[0].message.content