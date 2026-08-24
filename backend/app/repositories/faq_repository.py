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
    text = re.sub(r'\s+', ' ', text)  # Chuẩn hóa khoảng trắng thừa
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

    @staticmethod
    def _format_faq_doc(doc: dict) -> dict:
        """Chuyển đổi _id thành id dạng string và xóa _id."""
        formatted = doc.copy()
        if "_id" in formatted:
            formatted["id"] = str(formatted["_id"])
            del formatted["_id"]
        return formatted

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
            faqs.append(self._format_faq_doc(doc))
        return faqs

    async def get_by_id(self, faq_id: str) -> Optional[dict]:
        if not ObjectId.is_valid(faq_id):
            return None

        doc = await self.collection.find_one({"_id": ObjectId(faq_id)})
        if doc:
            return self._format_faq_doc(doc)
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

    async def find_matching(
        self,
        message: str,
        score_cutoff: float = 75.0
    ) -> Optional[dict]:
        """
        Tìm FAQ theo 3 bước:
        1. Exact match với câu hỏi
        2. Keyword/phrase match
        3. Fuzzy matching
        """
        if not message:
            return None

        normalized_message = normalize_text(message)
        if not normalized_message:
            return None

        cursor = self.collection.find({})
        faqs = await cursor.to_list(length=1000)

        if not faqs:
            return None

        # =========================================================
        # 1. EXACT MATCH
        # =========================================================
        for faq in faqs:
            question = normalize_text(faq.get("question", ""))
            if normalized_message == question:
                print(
                    "🎯 Exact FAQ match | "
                    f"Question: '{faq.get('question')}'"
                )
                return self._format_faq_doc(faq)

        # =========================================================
        # 2. KEYWORD / PHRASE MATCH
        # =========================================================
        keyword_matches = []

        for faq in faqs:
            keywords = faq.get("keywords", [])

            for keyword in keywords:
                normalized_keyword = normalize_text(keyword)

                if not normalized_keyword:
                    continue

                # So khớp từ nguyên vẹn với ranh giới từ (word boundary)
                pattern = r'\b' + re.escape(normalized_keyword) + r'\b'
                if re.search(pattern, normalized_message):
                    keyword_matches.append(
                        (
                            len(normalized_keyword.split()),
                            faq,
                            normalized_keyword
                        )
                    )

        if keyword_matches:
            # Ưu tiên keyword dài hơn / cụ thể hơn
            keyword_matches.sort(
                key=lambda x: x[0],
                reverse=True
            )

            _, best_faq, matched_keyword = keyword_matches[0]

            print(
                "🎯 Keyword FAQ match | "
                f"Keyword: '{matched_keyword}' | "
                f"Question: '{best_faq.get('question')}'"
            )

            return self._format_faq_doc(best_faq)

        # =========================================================
        # 3. FUZZY MATCHING
        # =========================================================
        best_faq = None
        highest_score = 0.0

        for faq in faqs:
            candidates = [faq.get("question", "")]
            candidates.extend(faq.get("keywords", []))

            normalized_candidates = [
                normalize_text(c)
                for c in candidates
                if c
            ]

            if not normalized_candidates:
                continue

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

        # =========================================================
        # 4. CHECK FUZZY SCORE
        # =========================================================
        if best_faq and highest_score >= score_cutoff:
            print(
                f"🎯 Fuzzy FAQ match | "
                f"Score: {highest_score:.1f}% | "
                f"Question: '{best_faq.get('question')}'"
            )
            return self._format_faq_doc(best_faq)

        return None