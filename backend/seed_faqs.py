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

    # =========================================================
    # THÔNG TIN CHUNG
    # =========================================================

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "Môn Điện toán đám mây có bao nhiêu tín chỉ?",
        "answer": (
            "Môn Điện toán đám mây có 3 tín chỉ."
        ),

        "keywords": [
            "số tín chỉ",
            "bao nhiêu tín chỉ"
        ],

        "category": "tin_chi"
    },

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "Môn Điện toán đám mây học những nội dung gì?",
        "answer": (
            "Môn học cung cấp các kiến thức và kỹ năng thực tiễn về "
            "điện toán đám mây, bao gồm các mô hình dịch vụ đám mây "
            "như IaaS, PaaS, SaaS, triển khai và quản lý tài nguyên "
            "trên nền tảng đám mây."
        ),

        "keywords": [
            "nội dung môn học",
            "môn học gồm những gì",
            "học những gì",
            "kiến thức môn học"
        ],

        "category": "noi_dung_mon_hoc"
    },

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "Môn Điện toán đám mây thuộc khối kiến thức nào?",
        "answer": (
            "Học phần thuộc khối kiến thức chuyên ngành của chương trình "
            "đào tạo các ngành Công nghệ thông tin, Mạng máy tính và "
            "Truyền thông dữ liệu, Khoa học dữ liệu và Hệ thống thông tin quản lý."
        ),

        "keywords": [
            "khối kiến thức",
            "thuộc chuyên ngành",
            "ngành đào tạo"
        ],

        "category": "noi_dung_mon_hoc"
    },


    # =========================================================
    # LỊCH HỌC
    # =========================================================

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "Lịch học môn Điện toán đám mây hiện tại như thế nào?",
        "answer": (
            "Theo lịch học hiện tại, môn Điện toán đám mây có các lịch học sau:\n"
            "- Thứ 2, tiết 16-18: E-Learning (Online), "
            "từ 03/08/2026 đến 31/08/2026.\n"
            "- Thứ 4, tiết 7-9: phòng B007 - CS1, "
            "P. Thạnh Mỹ Tây, TP.HCM, từ 29/07/2026 đến 23/09/2026.\n"
            "- Thứ 4, tiết 7-9: Online, "
            "từ 22/07/2026 đến 26/08/2026.\n"
            "- Thứ 8, tiết 7-9: Online, ngày 23/08/2026."
        ),

        "keywords": [
            "lịch học",
            "thời khóa biểu",
            "lịch học hiện tại",
            "các buổi học"
        ],

        "category": "lich_hoc"
    },

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "Môn Điện toán đám mây học vào thứ mấy?",
        "answer": (
            "Môn học hiện có các buổi học vào Thứ 2, Thứ 4 và Thứ 8 "
            "theo lịch học được công bố."
        ),

        "keywords": [
            "học thứ mấy",
            "lịch theo thứ",
            "ngày học"
        ],

        "category": "lich_hoc"
    },

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "Môn Điện toán đám mây có học online không?",
        "answer": (
            "Có. Môn học có các buổi được tổ chức theo hình thức "
            "E-Learning (Online). Sinh viên cần theo dõi lịch học "
            "để biết chính xác buổi nào học trực tuyến."
        ),

        "keywords": [
            "lịch học online",
            "học trực tuyến",
            "hình thức online",
            "e-learning"
        ],

        "category": "lich_hoc"
    },

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "Môn Điện toán đám mây học đến khi nào?",
        "answer": (
            "Theo lịch hiện tại, các buổi học được tổ chức trong "
            "các khoảng thời gian từ tháng 07/2026 đến tháng 09/2026, "
            "tùy theo từng lịch học."
        ),

        "keywords": [
            "học đến khi nào",
            "kết thúc lịch học",
            "ngày kết thúc lịch"
        ],

        "category": "lich_hoc"
    },


    # =========================================================
    # LỊCH THI
    # =========================================================

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "Lịch thi môn Điện toán đám mây khi nào?",
        "answer": (
            "Lịch thi của môn Điện toán đám mây dự kiến rơi vào "
            "tuần 14-15. Sinh viên cần theo dõi thông báo chính thức "
            "để biết ngày, giờ và phòng thi cụ thể."
        ),

        "keywords": [
            "lịch thi",
            "thời gian thi",
            "thi cuối kỳ",
            "tuần thi"
        ],

        "category": "lich_thi"
    },


    # =========================================================
    # PHÒNG HỌC
    # =========================================================

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "Môn Điện toán đám mây học ở phòng nào?",
        "answer": (
            "Theo lịch hiện tại, có buổi học tại phòng B007 - CS1, "
            "P. Thạnh Mỹ Tây, TP.HCM, dãy nhà CS1-B. "
            "Ngoài ra môn học còn có các buổi Online."
        ),

        "keywords": [
            "phòng học",
            "học phòng nào",
            "địa điểm học",
            "phòng B007"
        ],

        "category": "phong_hoc"
    },

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "Phòng B007 nằm ở đâu?",
        "answer": (
            "Phòng B007 thuộc dãy nhà CS1-B, "
            "P. Thạnh Mỹ Tây, TP.HCM."
        ),

        "keywords": [
            "phòng B007 ở đâu",
            "vị trí phòng B007",
            "địa chỉ phòng B007"
        ],

        "category": "phong_hoc"
    },


    # =========================================================
    # NỘI QUY - CHUYÊN CẦN
    # =========================================================

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "Môn Điện toán đám mây yêu cầu dự lớp bao nhiêu phần trăm?",
        "answer": (
            "Sinh viên phải dự lớp ít nhất 80% số buổi học."
        ),

        "keywords": [
            "yêu cầu chuyên cần",
            "tỷ lệ dự lớp",
            "phải dự bao nhiêu phần trăm",
            "điều kiện dự lớp"
        ],

        "category": "noi_quy"
    },

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "Môn Điện toán đám mây có điểm danh không?",
        "answer": (
            "Có. Sinh viên được điểm danh từng buổi học "
            "và tự CHECK IN điểm danh từng buổi."
        ),

        "keywords": [
            "có điểm danh không",
            "hình thức điểm danh",
            "check in điểm danh"
        ],

        "category": "noi_quy"
    },

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "Điểm danh đúng giờ được bao nhiêu điểm?",
        "answer": (
            "Sinh viên điểm danh đúng giờ, từ phút 0 đến phút 15, "
            "được 10 điểm điểm danh."
        ),

        "keywords": [
            "điểm danh đúng giờ",
            "điểm danh phút 0-15",
            "10 điểm điểm danh"
        ],

        "category": "noi_quy"
    },

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "Điểm danh đi trễ được bao nhiêu điểm?",
        "answer": (
            "Sinh viên điểm danh từ phút 16 đến phút 60 "
            "được 7 điểm điểm danh."
        ),

        "keywords": [
            "điểm danh đi trễ",
            "đi trễ bao nhiêu điểm",
            "điểm danh phút 16-60"
        ],

        "category": "noi_quy"
    },

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "Vắng học có phép được bao nhiêu điểm điểm danh?",
        "answer": (
            "Sinh viên vắng học có phép được 4 điểm điểm danh."
        ),

        "keywords": [
            "vắng có phép",
            "nghỉ có phép bao nhiêu điểm",
            "điểm danh vắng có phép"
        ],

        "category": "noi_quy"
    },

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "Vắng học không phép được bao nhiêu điểm điểm danh?",
        "answer": (
            "Sinh viên vắng học không phép được 0 điểm điểm danh."
        ),

        "keywords": [
            "vắng không phép",
            "nghỉ không phép bao nhiêu điểm",
            "điểm danh vắng không phép"
        ],

        "category": "noi_quy"
    },

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "Gian lận điểm danh bị xử lý như thế nào?",
        "answer": (
            "Nếu phát hiện gian lận điểm danh, sinh viên sẽ bị "
            "xử lý theo quy định học vụ."
        ),

        "keywords": [
            "gian lận điểm danh",
            "xử lý gian lận điểm danh",
            "vi phạm điểm danh"
        ],

        "category": "noi_quy"
    },


    # =========================================================
    # NỘI DUNG MÔN HỌC
    # =========================================================

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "IaaS là gì?",
        "answer": (
            "IaaS (Infrastructure as a Service) là mô hình cung cấp "
            "hạ tầng công nghệ thông tin dưới dạng dịch vụ, chẳng hạn "
            "như máy chủ, lưu trữ và mạng."
        ),

        "keywords": [
            "IaaS",
            "Infrastructure as a Service",
            "hạ tầng dưới dạng dịch vụ"
        ],

        "category": "noi_dung_mon_hoc"
    },

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "PaaS là gì?",
        "answer": (
            "PaaS (Platform as a Service) là mô hình cung cấp "
            "nền tảng để phát triển, triển khai và quản lý ứng dụng "
            "mà không cần tự quản lý toàn bộ hạ tầng bên dưới."
        ),

        "keywords": [
            "PaaS",
            "Platform as a Service",
            "nền tảng dưới dạng dịch vụ"
        ],

        "category": "noi_dung_mon_hoc"
    },

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "SaaS là gì?",
        "answer": (
            "SaaS (Software as a Service) là mô hình cung cấp "
            "phần mềm dưới dạng dịch vụ, cho phép người dùng "
            "sử dụng ứng dụng thông qua Internet mà không cần "
            "tự cài đặt và quản lý hạ tầng phần mềm."
        ),

        "keywords": [
            "SaaS",
            "Software as a Service",
            "phần mềm dưới dạng dịch vụ"
        ],

        "category": "noi_dung_mon_hoc"
    },


    # =========================================================
    # CÁCH TÍNH ĐIỂM
    # =========================================================

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "Môn Điện toán đám mây tính điểm như thế nào?",
        "answer": (
            "Điểm học phần được tính dựa trên các thành phần đánh giá "
            "theo quy định của môn học, bao gồm điểm chuyên cần, "
            "quá trình, bài tập và bài thi cuối kỳ."
        ),

        "keywords": [
            "cách tính điểm",
            "công thức tính điểm",
            "cơ cấu điểm"
        ],

        "category": "cach_tinh_diem"
    },

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "Điểm quá trình chiếm bao nhiêu phần trăm?",
        "answer": (
            "Điểm quá trình là một trong các thành phần dùng để "
            "đánh giá kết quả học tập của học phần. "
            "Sinh viên cần tham khảo cơ cấu điểm chính thức "
            "được công bố cho học phần."
        ),

        "keywords": [
            "tỷ lệ điểm quá trình",
            "điểm quá trình bao nhiêu phần trăm"
        ],

        "category": "cach_tinh_diem"
    },

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "Điểm cuối kỳ chiếm bao nhiêu phần trăm?",
        "answer": (
            "Điểm cuối kỳ là một thành phần trong cơ cấu đánh giá "
            "kết quả học tập của học phần. Sinh viên cần tham khảo "
            "cơ cấu điểm chính thức được công bố."
        ),

        "keywords": [
            "tỷ lệ điểm cuối kỳ",
            "điểm thi cuối kỳ bao nhiêu phần trăm"
        ],

        "category": "cach_tinh_diem"
    },


    # =========================================================
    # HÌNH THỨC THI
    # =========================================================

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "Môn Điện toán đám mây thi cuối kỳ theo hình thức nào?",
        "answer": (
            "Sinh viên cần theo dõi thông báo chính thức của học phần "
            "để biết hình thức thi cuối kỳ, thời gian và địa điểm thi."
        ),

        "keywords": [
            "hình thức thi cuối kỳ",
            "cách thức thi",
            "thi trắc nghiệm",
            "thi trên máy tính"
        ],

        "category": "lich_thi"
    },


    # =========================================================
    # TÀI LIỆU
    # =========================================================

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "Tài liệu môn Điện toán đám mây được tải ở đâu?",
        "answer": (
            "Sinh viên sử dụng email có tên miền ut.edu.vn để đăng nhập "
            "và tải tài liệu tại trang courses.ut.edu.vn."
        ),

        "keywords": [
            "tải tài liệu",
            "download tài liệu",
            "địa chỉ tải tài liệu",
            "trang tải tài liệu"
        ],

        "category": "tai_lieu"
    },

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "Ai được phép tải tài liệu môn học?",
        "answer": (
            "Sinh viên sử dụng email có tên miền ut.edu.vn "
            "để đăng nhập và tải tài liệu học tập."
        ),

        "keywords": [
            "điều kiện tải tài liệu",
            "quyền tải tài liệu",
            "email được phép tải"
        ],

        "category": "tai_lieu"
    },

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "Kho học liệu của môn gồm những gì?",
        "answer": (
            "Kho học liệu có thể bao gồm tài liệu tham khảo, bài tập, "
            "video bài giảng, câu hỏi kiểm tra trắc nghiệm và các "
            "tài nguyên phục vụ học tập."
        ),

        "keywords": [
            "nội dung kho học liệu",
            "kho học liệu gồm gì",
            "tài nguyên học tập"
        ],

        "category": "tai_lieu"
    },

    {
        "course_code": "CLOUD101",
        "course_name": "Điện toán đám mây",

        "question": "Tài liệu trong kho học liệu được sắp xếp như thế nào?",
        "answer": (
            "Tài liệu được tổ chức theo từng nhóm nội dung của học phần "
            "để sinh viên thuận tiện tìm kiếm và sử dụng."
        ),

        "keywords": [
            "cách sắp xếp tài liệu",
            "tài liệu theo bài học",
            "tổ chức tài liệu"
        ],

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