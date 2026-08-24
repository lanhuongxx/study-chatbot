import os
from datetime import datetime, timezone
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient


class ChatLogRepository:

    def __init__(self, db_client: Optional[AsyncIOMotorClient] = None):
        if db_client:
            self.db = db_client["study_chatbot_db"]
        else:
            mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
            client = AsyncIOMotorClient(mongo_url)
            self.db = client["study_chatbot_db"]

        # Lưu lịch sử chat vào collection 'chat_histories'
        self.collection = self.db["chat_histories"]

    async def create(
        self,
        session_id: str,
        user_message: str,
        bot_response: str,
        source: str
    ) -> dict:
        """
        Lưu một lượt trò chuyện (của user và bot) vào MongoDB.
        """
        chat_doc = {
            "session_id": session_id,
            "user_message": user_message,
            "bot_response": bot_response,
            "source": source,
            "timestamp": datetime.now(timezone.utc)
        }
        
        result = await self.collection.insert_one(chat_doc)
        
        # Định dạng lại ObjectId thành String ID
        chat_doc["id"] = str(result.inserted_id)
        if "_id" in chat_doc:
            del chat_doc["_id"]
            
        return chat_doc

    async def get_by_session_id(self, session_id: str, limit: int = 50) -> List[dict]:
        """
        Lấy danh sách các đoạn chat theo session_id (sắp xếp tăng dần theo thời gian).
        """
        cursor = (
            self.collection.find({"session_id": session_id})
            .sort("timestamp", 1)
            .limit(limit)
        )

        history = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            history.append(doc)

        return history