from app.repositories.faq_repository import FAQRepository
from app.repositories.chat_log_repository import ChatLogRepository
from app.services.gemini_service import GeminiService


class ChatService:

    def __init__(self):
        self.faq_repository = FAQRepository()
        self.gemini_service = GeminiService()
        self.chat_log_repository = ChatLogRepository()

    async def process_message(
        self,
        session_id: str,
        message: str
    ):
        # 1. Tìm FAQ
        faq = await self.faq_repository.find_matching(message)

        # 2. Nếu có FAQ → Rule-based
        if faq:
            answer = faq["answer"]
            source = "rule"

        # 3. Nếu không có FAQ → Gemini
        else:
            answer = await self.gemini_service.generate_response(message)
            source = "gemini"

        # 4. Lưu lịch sử chat
        await self.chat_log_repository.create(
            session_id=session_id,
            user_message=message,
            bot_response=answer,
            source=source
        )

        # 5. Trả kết quả
        return {
            "answer": answer,
            "source": source
        }