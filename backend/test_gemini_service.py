import asyncio

from app.services.gemini_service import GeminiService


async def main():
    service = GeminiService()

    response = await service.generate_response(
        "Hãy giải thích ngắn gọn Data Science là gì?"
    )

    print("=== GEMINI RESPONSE ===")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())