from bson import ObjectId
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
import os


class FAQRepository:

    def __init__(self, db_client: Optional[AsyncIOMotorClient] = None):
        if db_client:
            self.db = db_client["study_chatbot_db"]
        else:
            # Tự động lấy URI từ env nếu không truyền client
            mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
            client = AsyncIOMotorClient(mongo_url)
            self.db = client["study_chatbot_db"]

        self.collection = self.db["faqs"]

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 20,
        category: Optional[str] = None
    ) -> List[dict]:

        query = {}

        if category:
            query["category"] = category

        cursor = self.collection.find(query).skip(skip).limit(limit)

        faqs = []

        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            faqs.append(doc)

        return faqs

    async def get_by_id(self, faq_id: str) -> Optional[dict]:

        if not ObjectId.is_valid(faq_id):
            return None

        doc = await self.collection.find_one(
            {"_id": ObjectId(faq_id)}
        )

        if doc:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            return doc

        return None

    async def create(self, faq_data: dict) -> dict:

        result = await self.collection.insert_one(faq_data)

        faq_data["id"] = str(result.inserted_id)

        if "_id" in faq_data:
            del faq_data["_id"]

        return faq_data

    async def update(
        self,
        faq_id: str,
        update_data: dict
    ) -> Optional[dict]:

        if not ObjectId.is_valid(faq_id):
            return None

        # Chỉ cập nhật các trường được truyền lên
        filtered_data = {
            k: v
            for k, v in update_data.items()
            if v is not None
        }

        if not filtered_data:
            return await self.get_by_id(faq_id)

        result = await self.collection.update_one(
            {"_id": ObjectId(faq_id)},
            {"$set": filtered_data}
        )

        if result.modified_count > 0 or result.matched_count > 0:
            return await self.get_by_id(faq_id)

        return None

    async def delete(self, faq_id: str) -> bool:

        if not ObjectId.is_valid(faq_id):
            return False

        result = await self.collection.delete_one(
            {"_id": ObjectId(faq_id)}
        )

        return result.deleted_count > 0

    async def find_matching(self, message: str) -> Optional[dict]:
        """
        Tìm FAQ phù hợp với câu hỏi của sinh viên
        dựa trên keywords và nội dung question.
        """

        message_lower = message.lower().strip()

        # 1. Tìm theo keywords
        cursor = self.collection.find({})

        async for doc in cursor:
            keywords = doc.get("keywords", [])

            for keyword in keywords:
                if keyword.lower().strip() in message_lower:

                    doc["id"] = str(doc["_id"])
                    del doc["_id"]

                    return doc

        # 2. Nếu không khớp keyword,
        # thử tìm theo nội dung question
        cursor = self.collection.find({})

        async for doc in cursor:

            question = doc.get("question", "").lower()

            question_words = set(question.split())
            message_words = set(message_lower.split())

            common_words = question_words.intersection(
                message_words
            )

            # Có ít nhất 2 từ trùng nhau
            if len(common_words) >= 2:

                doc["id"] = str(doc["_id"])
                del doc["_id"]

                return doc

        return None