from datetime import datetime, timezone
from typing import Any, Dict, List

from google.genai.errors import ClientError

from app.repositories.chat_log_repository import ChatLogRepository
from app.repositories.faq_repository import FAQRepository
from app.services.gemini_service import GeminiService


class ChatService:

    def __init__(self):
        self.gemini_service = GeminiService()
        # Truyền gemini_service vào để FAQRepository dùng cho semantic search
        self.faq_repository = FAQRepository(gemini_service=self.gemini_service)
        self.chat_log_repository = ChatLogRepository()

    async def process_message(
        self,
        session_id: str,
        message: str
    ) -> Dict[str, Any]:

        # 1. Tìm FAQ phù hợp từ DB
        faq = await self.faq_repository.find_matching(message)

        # 2. Xây dựng context cho Gemini từ FAQ tìm được (nếu có)
        faq_context = ""
        if faq:
            faq_context = (
                f"Câu hỏi FAQ: {faq.get('question')}\n"
                f"Câu trả lời FAQ: {faq.get('answer')}"
            )

        # 3. Gửi câu hỏi kèm context sang Gemini để xử lý thông minh
        try:
            answer = await self.gemini_service.generate_response(
                message=message,
                faq_context=faq_context
            )
            source = "gemini"

        except ClientError as e:
            # Xử lý trường hợp bị Rate Limit (Free Tier)
            if getattr(e, "code", None) == 429:
                # Nếu Gemini lỗi 429 nhưng có FAQ khớp, dùng tạm câu trả lời từ FAQ làm fallback
                if faq:
                    answer = faq["answer"]
                    source = "rule_fallback"
                else:
                    answer = (
                        "Hệ thống AI đang quá tải. "
                        "Bạn vui lòng thử lại sau ít phút."
                    )
                    source = "fallback"
            else:
                raise

        # 4. Lưu lịch sử chat
        await self.chat_log_repository.create(
            session_id=session_id,
            user_message=message,
            bot_response=answer,
            source=source
        )

        # 5. Trả kết quả về Client
        return {
            "answer": answer,
            "source": source,
            "timestamp": datetime.now(timezone.utc)
        }

    async def get_history(
        self,
        session_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Lấy lịch sử hội thoại dựa trên session_id."""
        return await self.chat_log_repository.get_by_session_id(
            session_id=session_id,
            limit=limit
        )