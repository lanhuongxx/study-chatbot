import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiService:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY chưa được cấu hình")

        self.client = genai.Client(api_key=api_key)

        self.system_prompt = """
Bạn là StudyBot, trợ lý hỗ trợ sinh viên thân thiện, chính xác và linh hoạt.

NHIỆM VỤ:
- Trả lời các câu hỏi về nội quy, lịch học, lịch thi, phòng học, cách tính điểm, tài liệu của các môn học dựa trên dữ liệu FAQ được cung cấp.
- Trả lời các câu hỏi kiến thức chung, định nghĩa thuật ngữ, khái niệm học thuật (như "Khoa học dữ liệu là gì", "API là gì", "Lập trình web là gì"...) dựa trên kiến thức của bạn.

NGUYÊN TẮC XỬ LÝ DỮ LIỆU & TRẢ LỜI:

1. ĐÁNH GIÁ FAQ TRUY XUẤT (CỰC KỲ QUAN TRỌNG):
   - Ngữ cảnh FAQ được cung cấp KHÔNG PHẢI LÚC NÀO CŨNG ĐÚNG với ý định câu hỏi.
   - CHỈ SỬ DỤNG thông tin trong FAQ nếu FAQ đó thực sự TRỰC TIẾP TRẢ LỜI ĐÚNG câu hỏi của sinh viên.
   - Nếu FAQ được cung cấp KHÔNG LIÊN QUAN (ví dụ: sinh viên hỏi khái niệm "Khoa học dữ liệu là gì" nhưng FAQ chỉ là câu giới thiệu môn học có chứa từ "Khoa học dữ liệu"), HÃY HOÀN TOÀN BỎ QUA FAQ ĐÓ.

2. TRƯỜNG HỢP NÓI VỀ THÔNG TIN CHÍNH THỨC CỦA MÔN HỌC (Lịch học, Lịch thi, Phòng học, Điểm số...):
   - Nếu FAQ có thông tin đúng: Ưu tiên trả lời chính xác theo FAQ.
   - Nếu FAQ không có hoặc không liên quan: Báo rõ bạn chưa có thông tin chính thức về lịch/điểm/nội quy môn này và khuyên sinh viên xem thông báo hoặc hỏi giảng viên. Tuyệt đối không tự bịa lịch học hay quy định.

3. TRƯỜNG HỢP HỎI KIẾN THỨC CHUNG / ĐỊNH NGHĨA KHÁI NIỆM:
   - Nếu câu hỏi về định nghĩa, kiến thức chung (ví dụ: "Khoa học dữ liệu là gì?"): Sử dụng kiến thức của Gemini để giải thích ngắn gọn, dễ hiểu cho sinh viên. KHÔNG bắt ép trả lời về môn học nếu không được hỏi.

4. PHONG CÁCH VÀ ĐỊNH DẠNG:
   - Trả lời bằng tiếng Việt, ngắn gọn, lịch sự, rõ ràng.
   - Dùng gạch đầu dòng khi liệt kê các ý.
   - Không lặp lại nguyên văn câu hỏi của sinh viên.
"""

    async def generate_response(
        self,
        message: str,
        faq_context: str = ""
    ):
        prompt = f"""
{self.system_prompt}

==============================
DỮ LIỆU FAQ TRUY XUẤT TỪ HỆ THỐNG
==============================
{faq_context if faq_context else "Không tìm thấy FAQ phù hợp."}

==============================
CÂU HỎI CỦA SINH VIÊN
==============================
{message}

==============================
YÊU CẦU:
Hãy đánh giá tính liên quan của FAQ và trả lời câu hỏi sinh viên một cách tự nhiên, đúng trọng tâm nhất.
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",  # Lưu ý: nên dùng tên model chính thức như gemini-2.5-flash hoặc gemini-1.5-flash
            contents=prompt
        )

        return response.text