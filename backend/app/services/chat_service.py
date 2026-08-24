from datetime import datetime, timezone
from typing import Any, Dict, List

from app.repositories.chat_log_repository import ChatLogRepository
from app.repositories.faq_repository import FAQRepository
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
    ) -> Dict[str, Any]:
        # 1. Tìm FAQ (sử dụng thuật toán Fuzzy Matching trong faq_repository)
        faq = await self.faq_repository.find_matching(message)

        # 2. Nếu có FAQ → Rule-based
        if faq:
            answer = faq["answer"]
            source = "rule"

        # 3. Nếu không có FAQ → Gemini
        else:
            answer = await self.gemini_service.generate_response(message)
            source = "gemini"

        # 4. Lưu lịch sử chat vào MongoDB
        await self.chat_log_repository.create(
            session_id=session_id,
            user_message=message,
            bot_response=answer,
            source=source
        )

        # 5. Trả kết quả
        return {
            "answer": answer,
            "source": source,
            "timestamp": datetime.now(timezone.utc)
        }

    async def get_history(self, session_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Lấy lịch sử hội thoại dựa trên session_id."""
        return await self.chat_log_repository.get_by_session_id(
            session_id=session_id,
            limit=limit
        )