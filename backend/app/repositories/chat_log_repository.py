from typing import Optional
from app.database import database
from app.models.chat_log import ChatLog


class ChatLogRepository:

    def __init__(self):
        self.collection = database[ChatLog.collection_name]

    async def create(
        self,
        session_id: str,
        user_message: str,
        bot_response: str,
        source: str
    ):
        document = ChatLog.create_document(
            session_id=session_id,
            user_message=user_message,
            bot_response=bot_response,
            source=source
        )

        result = await self.collection.insert_one(document)
        return result.inserted_id

    async def get_logs(self, skip: int = 0, limit: int = 20, source: Optional[str] = None):
        query = {}
        if source:
            query["source"] = source

        cursor = self.collection.find(query).sort("timestamp", -1).skip(skip).limit(limit)
        logs = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            logs.append(doc)
        return logs