import os
import re
from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from unidecode import unidecode
from rapidfuzz import process, fuzz


def normalize_text(text: str) -> str:
    """Chuyển chữ thường, khử dấu tiếng Việt và xóa ký tự đặc biệt."""
    if not text:
        return ""
    text = text.lower().strip()
    text = unidecode(text)
    text = re.sub(r'[^\w\s]', '', text)
    return text


class FAQRepository:

    def __init__(self, db_client: Optional[AsyncIOMotorClient] = None):
        if db_client:
            self.db = db_client["study_chatbot_db"]
        else:
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

        doc = await self.collection.find_one({"_id": ObjectId(faq_id)})
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

        filtered_data = {
            k: v for k, v in update_data.items() if v is not None
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

        result = await self.collection.delete_one({"_id": ObjectId(faq_id)})
        return result.deleted_count > 0

    async def find_matching(self, message: str, score_cutoff: float = 75.0) -> Optional[dict]:
        """
        Tìm FAQ bằng Fuzzy Matching + Unidecode.
        Sử dụng token_set_ratio để tránh khớp nhầm các câu xã giao ngắn.
        """
        if not message:
            return None

        # Khử dấu & chuẩn hóa tin nhắn
        normalized_message = normalize_text(message)

        # Nếu tin nhắn quá ngắn (ví dụ: "chào", "hi"), không cho bắt FAQ linh tinh
        if len(normalized_message.split()) < 2 and normalized_message not in ["xin chao", "chao"]:
            # Nếu trong DB không có FAQ "xin chào" thì trả về None để Gemini trả lời xã giao
            pass

        cursor = self.collection.find({})
        faqs = await cursor.to_list(length=1000)

        if not faqs:
            return None

        best_faq = None
        highest_score = 0.0

        for faq in faqs:
            candidates = [faq.get("question", "")]
            candidates.extend(faq.get("keywords", []))

            normalized_candidates = [normalize_text(c) for c in candidates if c]

            if not normalized_candidates:
                continue

            # Sử dụng token_set_ratio giúp so sánh tập hợp từ chuẩn xác hơn, tránh dính bẫy WRatio
            match_result = process.extractOne(
                query=normalized_message,
                choices=normalized_candidates,
                scorer=fuzz.token_set_ratio
            )

            if match_result:
                _, score, _ = match_result
                if score > highest_score:
                    highest_score = score
                    best_faq = faq

        # Chỉ chấp nhận nếu điểm khớp >= 75%
        if best_faq and highest_score >= score_cutoff:
            print(f"🎯 Match FAQ! Score: {highest_score:.1f}% | Question: '{best_faq.get('question')}'")
            best_faq["id"] = str(best_faq["_id"])
            if "_id" in best_faq:
                del best_faq["_id"]
            return best_faq

        return None