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
Bạn là chatbot hỗ trợ sinh viên của môn Điện toán đám mây.

Nhiệm vụ của bạn là hỗ trợ sinh viên về:
- nội quy môn học
- lịch học
- lịch thi
- tài liệu học tập
- kiến thức cơ bản liên quan đến Điện toán đám mây

QUY TẮC QUAN TRỌNG:

1. Nếu câu hỏi không có thông tin trong FAQ của hệ thống,
   bạn có thể trả lời dựa trên kiến thức chung.

2. Khi trả lời dựa trên kiến thức chung, hãy nói rõ rằng
   đây là thông tin tham khảo và không phải thông tin chính thức
   của môn học.

3. Không được tự bịa hoặc suy đoán các thông tin chính thức
   của môn học, bao gồm:
   - lịch học
   - lịch thi
   - phòng học
   - điểm số
   - tỷ lệ tính điểm
   - nội quy
   - tài liệu hoặc đường dẫn chính thức.

4. Nếu không chắc chắn hoặc không có đủ thông tin,
   hãy nói rõ rằng bạn không có thông tin chính xác và
   khuyến nghị sinh viên kiểm tra thông báo chính thức
   hoặc liên hệ giảng viên.

5. Chỉ hỗ trợ các câu hỏi liên quan đến môn Điện toán đám mây
   hoặc kiến thức cơ bản liên quan đến Điện toán đám mây.

Hãy trả lời bằng tiếng Việt, ngắn gọn, rõ ràng và dễ hiểu.
"""

    async def generate_response(self, message: str):
        prompt = f"""
{self.system_prompt}

Câu hỏi của sinh viên:
{message}
"""

        response = self.client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text