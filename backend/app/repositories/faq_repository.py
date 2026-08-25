import math
import os
import re
from typing import List, Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from unidecode import unidecode

from app.services.gemini_service import GeminiService


def normalize_text(text: str) -> str:
    """
    Chuyển chữ thường, khử dấu tiếng Việt
    và xóa ký tự đặc biệt.

    Lưu ý: chỉ dùng hàm này cho EXACT MATCH và KEYWORD MATCH (so khớp
    ký tự y hệt). Không dùng để đo độ "giống nhau" giữa 2 câu khác nhau,
    vì việc khử dấu tiếng Việt làm mất thông tin ngữ nghĩa quan trọng
    (ví dụ "khoa học dữ liệu" và "kho học liệu" sau khi khử dấu trông
    rất giống nhau về ký tự dù nghĩa hoàn toàn khác) — việc đo độ giống
    về NGHĨA được giao cho embedding (semantic search) bên dưới.
    """
    if not text:
        return ""

    text = text.lower().strip()
    text = unidecode(text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)

    return text


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Độ tương đồng cosine giữa 2 vector embedding, trong khoảng [-1, 1]."""
    if not vec_a or not vec_b or len(vec_a) != len(vec_b):
        return 0.0

    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)


class FAQRepository:

    def __init__(
        self,
        db_client: Optional[AsyncIOMotorClient] = None,
        gemini_service: Optional[GeminiService] = None
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

        # gemini_service dùng để tạo embedding cho semantic search.
        # Optional vì một số nơi (vd CRUD admin thuần túy) không cần.
        self.gemini_service = gemini_service

    # =========================================================
    # TẠO EMBEDDING CHO 1 FAQ (dùng khi tạo/sửa FAQ)
    # =========================================================

    async def _build_embedding(self, faq_data: dict) -> Optional[List[float]]:
        if not self.gemini_service:
            return None

        text = faq_data.get("question", "")
        keywords = faq_data.get("keywords") or []
        if keywords:
            text += "\n" + "\n".join(keywords)

        if not text.strip():
            return None

        try:
            return await self.gemini_service.embed_text(
                text, task_type="RETRIEVAL_DOCUMENT"
            )
        except Exception as e:
            print(f"⚠️ Không tạo được embedding cho FAQ: {e}")
            return None

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

        embedding = await self._build_embedding(faq_data)
        if embedding:
            faq_data["embedding"] = embedding

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

        # Nếu question hoặc keywords thay đổi, embedding cũ không còn
        # đúng nữa -> phải tạo lại, nếu không semantic search sẽ dùng
        # nhầm vector cũ ứng với nội dung đã bị sửa.
        if "question" in filtered_data or "keywords" in filtered_data:
            current = await self.get_by_id(faq_id) or {}
            merged = {**current, **filtered_data}
            embedding = await self._build_embedding(merged)
            if embedding:
                filtered_data["embedding"] = embedding

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
        similarity_cutoff: float = 0.72,
        margin: float = 0.04
    ) -> Optional[dict]:
        """
        Tìm FAQ phù hợp nhất với câu hỏi, theo 3 tầng tăng dần chi phí:

        1. EXACT MATCH: câu hỏi giống hệt (sau khi chuẩn hoá) -> gần như
           chắc chắn đúng, trả về ngay.
        2. KEYWORD MATCH: tin nhắn chứa nguyên 1 keyword đã khai báo cho
           FAQ -> rẻ, tín hiệu mạnh, trả về ngay.
        3. SEMANTIC SEARCH (embedding): nếu 2 tầng trên không match,
           đo độ giống NGHĨA (không phải giống ký tự) giữa câu hỏi và
           từng FAQ bằng cosine similarity của vector embedding. Đây là
           tầng thay thế cho fuzzy string-matching cũ — fuzzy chỉ so
           ký tự nên dễ nhầm "khoa học dữ liệu" với "kho học liệu" (giống
           ký tự, khác nghĩa); embedding hiểu nghĩa nên phân biệt được.

        similarity_cutoff: điểm cosine tối thiểu để chấp nhận 1 match
        (thang 0..1, threshold ~0.7-0.75 là hợp lý cho câu hỏi tiếng Việt
        ngắn, có thể tinh chỉnh dựa trên log thực tế).

        margin: điểm số của FAQ tốt nhất phải nhỉnh hơn FAQ tốt nhì ít
        nhất "margin" thì mới được chấp nhận. Nếu 2 FAQ có điểm sát nhau,
        nghĩa là câu hỏi mơ hồ giữa 2 chủ đề -> an toàn hơn là để Gemini
        trả lời từ kiến thức chung thay vì đoán bừa 1 FAQ.
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

        # -----------------------------------------------------
        # 1. EXACT MATCH
        # -----------------------------------------------------
        for faq in faqs:
            question = normalize_text(faq.get("question", ""))
            if question and normalized_message == question:
                print(f"🎯 Exact FAQ match | Question: '{faq.get('question')}'")
                return self._format_faq_doc(faq)

        # -----------------------------------------------------
        # 2. KEYWORD MATCH
        # -----------------------------------------------------
        for faq in faqs:
            for kw in faq.get("keywords", []) or []:
                kw_norm = normalize_text(kw)
                if kw_norm and kw_norm in normalized_message:
                    print(
                        f"🔑 Keyword FAQ match | Keyword: '{kw}' | "
                        f"Question: '{faq.get('question')}'"
                    )
                    return self._format_faq_doc(faq)

        # -----------------------------------------------------
        # 3. SEMANTIC SEARCH (embedding)
        # -----------------------------------------------------
        if not self.gemini_service:
            print("⚠️ Chưa cấu hình GeminiService cho FAQRepository, bỏ qua semantic search.")
            return None

        try:
            query_embedding = await self.gemini_service.embed_text(
                message, task_type="RETRIEVAL_QUERY"
            )
        except Exception as e:
            print(f"⚠️ Lỗi tạo embedding cho câu hỏi: {e}")
            return None

        best_faq = None
        best_score = 0.0
        second_best_score = 0.0

        for faq in faqs:
            faq_embedding = faq.get("embedding")
            if not faq_embedding:
                # FAQ này chưa có embedding (dữ liệu cũ trước khi nâng cấp,
                # hoặc tạo qua API mà chưa cấu hình gemini_service).
                # Cần chạy lại seed_faqs.py để backfill.
                continue

            score = cosine_similarity(query_embedding, faq_embedding)

            if score > best_score:
                second_best_score = best_score
                best_score = score
                best_faq = faq
            elif score > second_best_score:
                second_best_score = score

        if (
            best_faq
            and best_score >= similarity_cutoff
            and (best_score - second_best_score) >= margin
        ):
            print(
                f"🎯 Semantic FAQ match | Score: {best_score:.3f} "
                f"(2nd best: {second_best_score:.3f}) | "
                f"Question: '{best_faq.get('question')}'"
            )
            return self._format_faq_doc(best_faq)

        # -----------------------------------------------------
        # 4. KHÔNG CÓ FAQ PHÙ HỢP -> CHUYỂN GEMINI KIẾN THỨC CHUNG
        # -----------------------------------------------------
        print(
            f"🤖 No suitable FAQ match | Message: '{message}' | "
            f"Best score: {best_score:.3f} (2nd: {second_best_score:.3f})"
        )
        return None