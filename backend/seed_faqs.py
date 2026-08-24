import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Load môi trường từ .env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# Bộ dữ liệu FAQ bám sát mục tiêu Đề tài: Nội quy môn học, Lịch học, Tài liệu học tập
SAMPLE_FAQS = [
    # ==========================================
    # 1. NHÓM NỘI QUY & QUY CHẾ MÔN HỌC
    # ==========================================
    {
        "question": "Nghỉ bao nhiêu tiết thì bị cấm thi môn Lập trình Web?",
        "answer": "Theo nội quy, nếu sinh viên nghỉ quá 20% tổng số tiết (tương đương vắng mặt quá 3 buổi học) sẽ bị cấm thi môn Lập trình Web.",
        "keywords": ["nghỉ bao nhiêu", "cấm thi", "vắng mặt", "chuyên cần", "nghỉ học", "nội quy"],
        "category": "noi_quy"
    },
    {
        "question": "Thang điểm và tỷ lệ điểm môn Cơ sở dữ liệu tính như thế nào?",
        "answer": "Môn Cơ sở dữ liệu tính điểm theo tỷ lệ: Chuyên cần (10%), Bài tập lớn/Giữa kỳ (30%), Thi kết thúc học phần (60%). Điểm tổng kết dưới 4.0 bị tính trượt môn.",
        "keywords": ["tỷ lệ điểm", "thang điểm", "cơ sở dữ liệu", "điểm thi", "trượt môn", "học lại"],
        "category": "noi_quy"
    },
    {
        "question": "Quy định về việc xin nghỉ học có phép như thế nào?",
        "answer": "Sinh viên cần gửi đơn xin nghỉ học kèm minh chứng (giấy khám bệnh/giấy xác nhận) cho giảng viên giảng dạy trước buổi học hoặc trong vòng 48 giờ sau buổi học.",
        "keywords": ["xin nghỉ", "nghỉ phép", "đơn xin nghỉ", "giấy khám bệnh", "quy định nghỉ"],
        "category": "noi_quy"
    },

    # ==========================================
    # 2. NHÓM LỊCH HỌC & LỊCH THI
    # ==========================================
    {
        "question": "Lịch thi học phần học kỳ này xem ở đâu?",
        "answer": "Lịch thi chính thức được cập nhật trên Cổng thông tin sinh viên tại mục 'Lịch thi' trước ngày thi ít nhất 2 tuần.",
        "keywords": ["lịch thi", "xem lịch thi", "thi học kỳ", "ngày thi", "cổng thông tin"],
        "category": "lich_hoc"
    },
    {
        "question": "Hạn nộp Đồ án chuyên ngành là khi nào?",
        "answer": "Thời hạn nộp báo cáo Đồ án chuyên ngành là trước 17h00 ngày Chủ Nhật tuần thứ 15 của học kỳ trên hệ thống LMS.",
        "keywords": ["hạn nộp", "đồ án", "nộp bài", "báo cáo đồ án", "tuần 15", "lms"],
        "category": "lich_hoc"
    },
    {
        "question": "Khi nào thì sinh viên được nghỉ Tết / nghỉ hè?",
        "answer": "Lịch nghỉ lễ, Tết và nghỉ hè được quy định chi tiết trong Khung kế hoạch thời gian năm học đăng tải trên website nhà trường.",
        "keywords": ["nghỉ tết", "nghỉ hè", "kế hoạch năm học", "thời gian nghỉ"],
        "category": "lich_hoc"
    },

    # ==========================================
    # 3. NHÓM TÀI LIỆU HỌC TẬP & MÔN HỌC
    # ==========================================
    {
        "question": "Tải Slide bài giảng và Giáo trình môn Điện toán đám mây ở đâu?",
        "answer": "Sinh viên truy cập vào hệ thống LMS của trường, đăng nhập tài khoản cá nhân, chọn môn 'Điện toán đám mây' để tải Slide và giáo trình PDF.",
        "keywords": ["tải slide", "giáo trình", "tài liệu", "điện toán đám mây", "lms", "pdf"],
        "category": "tai_lieu"
    },
    {
        "question": "Môn Lập trình Web học phần mềm và công cụ gì?",
        "answer": "Môn học sử dụng: VS Code (Code editor), Node.js / Python, MongoDB Community / Atlas, và Postman để test API.",
        "keywords": ["công cụ", "phần mềm", "lập trình web", "vs code", "node.js", "postman"],
        "category": "tai_lieu"
    },
    {
        "question": "Môn Kiến trúc phần mềm có tài liệu tham khảo nào tốt?",
        "answer": "Tài liệu tham khảo chính: Sách 'Clean Architecture' (Robert C. Martin) và các tài liệu hướng dẫn Microservices đăng trên LMS.",
        "keywords": ["tài liệu tham khảo", "sách", "kiến trúc phần mềm", "clean architecture"],
        "category": "tai_lieu"
    }
]

async def seed_data():
    mongo_url = os.getenv("MONGODB_URL")
    if not mongo_url:
        print("❌ Lỗi: Không tìm thấy MONGODB_URL trong file .env!")
        return

    client = AsyncIOMotorClient(mongo_url)
    db = client["study_chatbot_db"]
    collection = db["faqs"]

    # Làm sạch dữ liệu cũ và nạp mới
    await collection.delete_many({})
    print("🧹 Đã làm sạch collection 'faqs' cũ.")

    result = await collection.insert_many(SAMPLE_FAQS)
    print(f"✅ Đã nạp thành công {len(result.inserted_ids)} câu hỏi FAQ mẫu chuẩn đề tài vào MongoDB Atlas!")

if __name__ == "__main__":
    asyncio.run(seed_data())