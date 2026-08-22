import asyncio

from app.services.chat_service import ChatService


async def main():
    service = ChatService()

    print("=== TEST 1: FAQ → RULE ===")

    result = await service.process_message(
        session_id="test_session_001",
        message="Môn này có mấy tín chỉ vậy?"
    )

    print("Answer:", result["answer"])
    print("Source:", result["source"])

    print("\n=== TEST 2: NO FAQ → GEMINI ===")

    result = await service.process_message(
        session_id="test_session_001",
        message="Data Science là gì?"
    )

    print("Answer:", result["answer"])
    print("Source:", result["source"])


if __name__ == "__main__":
    asyncio.run(main())