from datetime import datetime, timezone


class ChatLog:
    collection_name = "chat_logs"

    @staticmethod
    def create_document(
        session_id: str,
        user_message: str,
        bot_response: str,
        source: str
    ):
        return {
            "session_id": session_id,
            "user_message": user_message,
            "bot_response": bot_response,
            "source": source,
            "timestamp": datetime.now(timezone.utc)
        }