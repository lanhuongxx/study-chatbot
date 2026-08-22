import asyncio

from app.repositories.chat_log_repository import ChatLogRepository


async def main():
    repository = ChatLogRepository()

    result = await repository.create(
        session_id="test_session_001",
        user_message="Môn này có mấy tín chỉ?",
        bot_response="Môn học có 3 tín chỉ.",
        source="rule"
    )

    print("Chat log đã được lưu.")
    print("Inserted ID:", result)


if __name__ == "__main__":
    asyncio.run(main())