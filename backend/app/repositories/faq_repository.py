import os
import re
from typing import List, Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from unidecode import unidecode
from rapidfuzz import fuzz


def normalize_text(text: str) -> str:
    """
    Chuyển chữ thường, khử dấu tiếng Việt
    và xóa ký tự đặc biệt.
    """
    if not text:
        return ""

    text = text.lower().strip()
    text = unidecode(text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)

    return text


class FAQRepository:

    def __init__(
        self,
        db_client: Optional[AsyncIOMotorClient] = None
    ):
        if db_client:
            self.db = db_client["study_chatbot_db"]
        else:
            mongo_url = os.getenv(
                "MONGODB_URL",
                "mongodb://localhost:27017"
            )

            client = AsyncIOMotorClient(mongo_url)
            self.db = client["study_chatbot_db"]

        self.collection = self.db["faqs"]

    # =========================================================
    # FORMAT FAQ DOCUMENT
    # =========================================================

    @staticmethod
    def _format_faq_doc(doc: dict) -> dict:
        """
        Chuyển _id của MongoDB thành id dạng string
        và xóa trường _id.
        """

        formatted = doc.copy()

        if "_id" in formatted:
            formatted["id"] = str(formatted["_id"])
            del formatted["_id"]

        return formatted

    # =========================================================
    # GET ALL FAQ
    # =========================================================

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 20,
        category: Optional[str] = None
    ) -> List[dict]:

        query = {}

        if category:
            query["category"] = category

        cursor = (
            self.collection
            .find(query)
            .skip(skip)
            .limit(limit)
        )

        faqs = []

        async for doc in cursor:
            faqs.append(
                self._format_faq_doc(doc)
            )

        return faqs

    # =========================================================
    # GET FAQ BY ID
    # =========================================================

    async def get_by_id(
        self,
        faq_id: str
    ) -> Optional[dict]:

        if not ObjectId.is_valid(faq_id):
            return None

        doc = await self.collection.find_one(
            {
                "_id": ObjectId(faq_id)
            }
        )

        if doc:
            return self._format_faq_doc(doc)

        return None

    # =========================================================
    # CREATE FAQ
    # =========================================================

    async def create(
        self,
        faq_data: dict
    ) -> dict:

        result = await self.collection.insert_one(
            faq_data
        )

        faq_data["id"] = str(
            result.inserted_id
        )

        if "_id" in faq_data:
            del faq_data["_id"]

        return faq_data

    # =========================================================
    # UPDATE FAQ
    # =========================================================

    async def update(
        self,
        faq_id: str,
        update_data: dict
    ) -> Optional[dict]:

        if not ObjectId.is_valid(faq_id):
            return None

        filtered_data = {
            key: value
            for key, value in update_data.items()
            if value is not None
        }

        if not filtered_data:
            return await self.get_by_id(faq_id)

        result = await self.collection.update_one(
            {
                "_id": ObjectId(faq_id)
            },
            {
                "$set": filtered_data
            }
        )

        if (
            result.modified_count > 0
            or result.matched_count > 0
        ):
            return await self.get_by_id(faq_id)

        return None

    # =========================================================
    # DELETE FAQ
    # =========================================================

    async def delete(
        self,
        faq_id: str
    ) -> bool:

        if not ObjectId.is_valid(faq_id):
            return False

        result = await self.collection.delete_one(
            {
                "_id": ObjectId(faq_id)
            }
        )

        return result.deleted_count > 0

    # =========================================================
    # FIND MATCHING FAQ
    # =========================================================

    async def find_matching(
        self,
        message: str,
        score_cutoff: float = 80.0
    ) -> Optional[dict]:
        """
        Tìm FAQ phù hợp với câu hỏi của sinh viên.

        Logic:

        1. Exact match:
           Câu hỏi giống hoàn toàn FAQ.

        2. Fuzzy matching:
           So sánh câu hỏi với TOÀN BỘ question của FAQ.

        3. Nếu điểm tương đồng không đủ cao:
           Trả về None để ChatService chuyển sang Gemini.

        Không sử dụng keyword đơn lẻ để quyết định match.

        Điều này tránh trường hợp:

            FAQ:
            "Lịch học môn Điện toán đám mây?"

            User:
            "Điện toán đám mây là gì?"

        bị coi là cùng một câu hỏi chỉ vì
        hai câu có chung cụm "Điện toán đám mây".
        """

        if not message:
            return None

        normalized_message = normalize_text(
            message
        )

        if not normalized_message:
            return None

        # =====================================================
        # LẤY FAQ
        # =====================================================

        cursor = self.collection.find({})

        faqs = await cursor.to_list(
            length=1000
        )

        if not faqs:
            return None

        # =====================================================
        # 1. EXACT MATCH
        # =====================================================

        for faq in faqs:

            question = normalize_text(
                faq.get("question", "")
            )

            if not question:
                continue

            if normalized_message == question:

                print(
                    "🎯 Exact FAQ match | "
                    f"Question: "
                    f"'{faq.get('question')}'"
                )

                return self._format_faq_doc(
                    faq
                )

        # =====================================================
        # 2. FUZZY MATCH
        # =====================================================

        best_faq = None
        highest_score = 0.0

        for faq in faqs:

            question = normalize_text(
                faq.get("question", "")
            )

            if not question:
                continue

            # Chỉ so sánh với QUESTION.
            #
            # Không so sánh trực tiếp với keywords
            # vì keyword có thể chỉ đại diện cho chủ đề
            # và gây false positive.

            score = fuzz.token_sort_ratio(
                normalized_message,
                question
            )

            if score > highest_score:
                highest_score = score
                best_faq = faq

        # =====================================================
        # 3. CHECK FUZZY SCORE
        # =====================================================

        if (
            best_faq
            and highest_score >= score_cutoff
        ):

            print(
                "🎯 Fuzzy FAQ match | "
                f"Score: {highest_score:.1f}% | "
                f"Question: "
                f"'{best_faq.get('question')}'"
            )

            return self._format_faq_doc(
                best_faq
            )

        # =====================================================
        # 4. KHÔNG CÓ FAQ PHÙ HỢP
        # =====================================================

        print(
            "🤖 No suitable FAQ match | "
            f"Message: '{message}' | "
            f"Best score: "
            f"{highest_score:.1f}%"
        )

        # Trả None để ChatService gọi Gemini
        return None