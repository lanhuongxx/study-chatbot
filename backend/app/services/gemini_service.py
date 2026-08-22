import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiService:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY chưa được cấu hình")

        self.client = genai.Client(api_key=api_key)

    async def generate_response(self, message: str):
        response = self.client.models.generate_content(
            model="gemini-3.6-flash",
            contents=message
        )

        return response.text