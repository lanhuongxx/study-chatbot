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
    # 1. LỊCH HỌC
    # =========================================================
    {
        "question": "Môn Điện toán đám mây có những lịch học nào?",
        "answer": (
            "Theo lịch học hiện tại, môn Điện toán đám mây có 4 lịch: "
            "Thứ 2 tiết 16-18, hình thức E-Learning (Online), từ 03/08/2026 đến 31/08/2026; "
            "Thứ 4 tiết 7-9 tại phòng B007 - CS1, P. Thạnh Mỹ Tây, TP.HCM, dãy nhà CS1-B, "
            "từ 29/07/2026 đến 23/09/2026; "
            "Thứ 4 tiết 7-9 Online, từ 22/07/2026 đến 26/08/2026; "
            "Thứ 8 tiết 7-9 Online, ngày 23/08/2026."
        ),
        "keywords": [
            "lịch học",
            "thời khóa biểu",
            "lịch môn học",
            "học khi nào",
            "điện toán đám mây"
        ],
        "category": "lich_hoc"
    },
{
    "question": "Môn Điện toán đám mây có bao nhiêu tín chỉ?",
    "answer": "Môn Điện toán đám mây có 3 tín chỉ.",
    "keywords": [
        "số tín chỉ",
        "bao nhiêu tín chỉ",
        "3 tín chỉ",
        "tín chỉ",
        "điện toán đám mây"
    ],
    "category": "tin_chi"
},

{
    "question": "Môn Điện toán đám mây thi cuối kỳ vào tuần nào?",
    "answer": (
        "Theo kế hoạch học tập, kỳ thi cuối kỳ môn Điện toán đám mây "
        "dự kiến diễn ra trong tuần 14-15."
    ),
    "keywords": [
        "lịch thi",
        "thi cuối kỳ",
        "tuần 14",
        "tuần 15",
        "thi khi nào"
    ],
    "category": "lich_thi"
},
    {
        "question": "Môn Điện toán đám mây học vào thứ 2 lúc mấy giờ?",
        "answer": (
            "Môn Điện toán đám mây có lịch học Thứ 2, tiết 16-18, "
            "hình thức E-Learning (Online), trong thời gian từ 03/08/2026 đến 31/08/2026."
        ),
        "keywords": [
            "thứ 2",
            "thứ hai",
            "tiết 16-18",
            "lịch học thứ 2",
            "online"
        ],
        "category": "lich_hoc"
    },

    {
        "question": "Môn Điện toán đám mây học vào thứ 4 lúc mấy giờ?",
        "answer": (
            "Môn Điện toán đám mây có lịch học Thứ 4, tiết 7-9. "
            "Có lịch học tại phòng B007 - CS1, P. Thạnh Mỹ Tây, TP.HCM, "
            "dãy nhà CS1-B, từ 29/07/2026 đến 23/09/2026. "
            "Ngoài ra có lịch học Online từ 22/07/2026 đến 26/08/2026."
        ),
        "keywords": [
            "thứ 4",
            "thứ tư",
            "tiết 7-9",
            "lịch học thứ 4",
            "online",
            "B007",
            "CS1-B"
        ],
        "category": "lich_hoc"
    },

    {
        "question": "Môn Điện toán đám mây có lịch học Online không?",
        "answer": (
            "Có. Theo lịch hiện tại, môn Điện toán đám mây có các lịch học Online "
            "gồm Thứ 2 tiết 16-18 từ 03/08/2026 đến 31/08/2026, "
            "Thứ 4 tiết 7-9 từ 22/07/2026 đến 26/08/2026 "
            "và Thứ 8 tiết 7-9 vào ngày 23/08/2026."
        ),
        "keywords": [
            "online",
            "học online",
            "học trực tuyến",
            "e-learning",
            "hình thức học"
        ],
        "category": "lich_hoc"
    },

    {
        "question": "Lịch học môn Điện toán đám mây kéo dài đến khi nào?",
        "answer": (
            "Theo lịch hiện tại, các lịch học có thời gian kết thúc khác nhau. "
            "Lịch Thứ 2 kết thúc ngày 31/08/2026; "
            "lịch Thứ 4 tại B007 - CS1 kết thúc ngày 23/09/2026; "
            "lịch Thứ 4 Online kết thúc ngày 26/08/2026; "
            "lịch Thứ 8 Online diễn ra ngày 23/08/2026."
        ),
        "keywords": [
            "kết thúc lịch học",
            "học đến khi nào",
            "thời gian học",
            "ngày kết thúc"
        ],
        "category": "lich_hoc"
    },


    # =========================================================
    # 2. PHÒNG HỌC
    # =========================================================
    {
        "question": "Môn Điện toán đám mây học ở phòng nào?",
        "answer": (
            "Theo lịch học, có một lịch học tại phòng B007 - CS1, "
            "P. Thạnh Mỹ Tây, TP.HCM, dãy nhà CS1-B. "
            "Các lịch học còn lại được tổ chức Online."
        ),
        "keywords": [
            "phòng học",
            "học phòng nào",
            "phòng B007",
            "B007",
            "CS1-B",
            "địa điểm học"
        ],
        "category": "phong_hoc"
    },

    {
        "question": "Phòng B007 - CS1 của môn Điện toán đám mây ở đâu?",
        "answer": (
            "Phòng B007 - CS1 nằm tại P. Thạnh Mỹ Tây, TP.HCM, "
            "thuộc dãy nhà CS1-B."
        ),
        "keywords": [
            "B007",
            "CS1",
            "CS1-B",
            "địa điểm",
            "phòng B007"
        ],
        "category": "phong_hoc"
    },

    {
        "question": "Môn Điện toán đám mây có học tại phòng B007 không?",
        "answer": (
            "Có. Theo lịch hiện tại, môn Điện toán đám mây có lịch học "
            "Thứ 4 tiết 7-9 tại phòng B007 - CS1, P. Thạnh Mỹ Tây, TP.HCM, "
            "dãy nhà CS1-B, từ 29/07/2026 đến 23/09/2026."
        ),
        "keywords": [
            "B007",
            "phòng B007",
            "CS1",
            "học tại phòng"
        ],
        "category": "phong_hoc"
    },


    # =========================================================
    # 3. NỘI DUNG MÔN HỌC
    # =========================================================
    {
        "question": "Môn Điện toán đám mây thuộc khối kiến thức nào?",
        "answer": (
            "Môn Điện toán đám mây thuộc khối kiến thức chuyên ngành "
            "của chương trình đào tạo các ngành Công nghệ thông tin, "
            "Mạng máy tính và Truyền thông dữ liệu, Khoa học dữ liệu "
            "và Hệ thống thông tin quản lý."
        ),
        "keywords": [
            "khối kiến thức",
            "chuyên ngành",
            "công nghệ thông tin",
            "khoa học dữ liệu",
            "mạng máy tính"
        ],
        "category": "noi_dung_mon_hoc"
    },

    {
        "question": "Môn Điện toán đám mây học những nội dung gì?",
        "answer": (
            "Môn học cung cấp kiến thức thực tiễn và kỹ năng thực hành "
            "về các chủ đề căn bản liên quan đến điện toán đám mây, "
            "bao gồm Infrastructure as a Service (IaaS), "
            "Platform as a Service (PaaS) và Software as a Service (SaaS)."
        ),
        "keywords": [
            "nội dung môn học",
            "học gì",
            "IaaS",
            "PaaS",
            "SaaS",
            "điện toán đám mây"
        ],
        "category": "noi_dung_mon_hoc"
    },

    {
        "question": "IaaS là một nội dung của môn Điện toán đám mây phải không?",
        "answer": (
            "Có. Infrastructure as a Service (IaaS) là một trong "
            "những chủ đề căn bản được học trong môn Điện toán đám mây."
        ),
        "keywords": [
            "IaaS",
            "Infrastructure as a Service",
            "nội dung học"
        ],
        "category": "noi_dung_mon_hoc"
    },

    {
        "question": "PaaS là một nội dung của môn Điện toán đám mây phải không?",
        "answer": (
            "Có. Platform as a Service (PaaS) là một trong "
            "những chủ đề căn bản được học trong môn Điện toán đám mây."
        ),
        "keywords": [
            "PaaS",
            "Platform as a Service",
            "nội dung học"
        ],
        "category": "noi_dung_mon_hoc"
    },

    {
        "question": "SaaS là một nội dung của môn Điện toán đám mây phải không?",
        "answer": (
            "Có. Software as a Service (SaaS) là một trong "
            "những chủ đề căn bản được học trong môn Điện toán đám mây."
        ),
        "keywords": [
            "SaaS",
            "Software as a Service",
            "nội dung học"
        ],
        "category": "noi_dung_mon_hoc"
    },


    # =========================================================
    # 4. NỘI QUY & ĐIỂM DANH
    # =========================================================
    {
        "question": "Sinh viên cần tham gia học môn Điện toán đám mây bao nhiêu phần trăm?",
        "answer": (
            "Sinh viên cần tham gia học tập đầy đủ trên lớp và phải dự lớp "
            "ít nhất 80%."
        ),
        "keywords": [
            "80%",
            "dự lớp",
            "tham gia học",
            "đi học",
            "chuyên cần"
        ],
        "category": "noi_quy"
    },

    {
        "question": "Môn Điện toán đám mây có điểm danh không?",
        "answer": (
            "Có. Sinh viên được điểm danh từng buổi học và tự CHECK IN "
            "điểm danh từng buổi. Kết quả điểm danh là căn cứ để đánh giá điểm thường xuyên."
        ),
        "keywords": [
            "điểm danh",
            "check in",
            "CHECK IN",
            "điểm danh từng buổi",
            "điểm thường xuyên"
        ],
        "category": "noi_quy"
    },

    {
        "question": "Điểm danh đúng giờ môn Điện toán đám mây được bao nhiêu điểm?",
        "answer": (
            "Sinh viên vào học đúng giờ, từ phút 0 đến phút 15, "
            "được 10 điểm điểm danh."
        ),
        "keywords": [
            "đúng giờ",
            "10 điểm",
            "điểm danh",
            "phút 0",
            "phút 15"
        ],
        "category": "noi_quy"
    },

    {
        "question": "Nếu đi trễ môn Điện toán đám mây thì được bao nhiêu điểm điểm danh?",
        "answer": (
            "Sinh viên vào học từ phút 16 đến phút 60 được 7 điểm điểm danh."
        ),
        "keywords": [
            "đi trễ",
            "trễ",
            "7 điểm",
            "phút 16",
            "phút 60",
            "điểm danh"
        ],
        "category": "noi_quy"
    },

    {
        "question": "Vắng học có phép môn Điện toán đám mây được bao nhiêu điểm điểm danh?",
        "answer": (
            "Sinh viên vắng học có phép được 4 điểm điểm danh."
        ),
        "keywords": [
            "vắng có phép",
            "nghỉ có phép",
            "4 điểm",
            "điểm danh"
        ],
        "category": "noi_quy"
    },

    {
        "question": "Vắng học không phép môn Điện toán đám mây được bao nhiêu điểm điểm danh?",
        "answer": (
            "Sinh viên vắng học không phép được 0 điểm điểm danh."
        ),
        "keywords": [
            "vắng không phép",
            "nghỉ không phép",
            "0 điểm",
            "điểm danh"
        ],
        "category": "noi_quy"
    },

    {
        "question": "Sinh viên gian lận điểm danh môn Điện toán đám mây bị xử lý như thế nào?",
        "answer": (
            "Môn học có các hình thức điểm danh bổ sung trong suốt buổi học. "
            "Nếu phát hiện gian lận, sinh viên sẽ bị kỷ luật theo quy định học vụ."
        ),
        "keywords": [
            "gian lận",
            "điểm danh gian lận",
            "kỷ luật",
            "quy định học vụ"
        ],
        "category": "noi_quy"
    },


    # =========================================================
    # 5. CÁCH TÍNH ĐIỂM
    # =========================================================
    {
        "question": "Môn Điện toán đám mây tính điểm như thế nào?",
        "answer": (
            "Điểm đánh giá môn Điện toán đám mây gồm 2 cột điểm: "
            "điểm quá trình chiếm 60% và điểm thi cuối kỳ chiếm 40%."
        ),
        "keywords": [
            "cách tính điểm",
            "tính điểm",
            "điểm quá trình",
            "điểm cuối kỳ",
            "60%",
            "40%"
        ],
        "category": "cach_tinh_diem"
    },

    {
        "question": "Điểm quá trình môn Điện toán đám mây chiếm bao nhiêu phần trăm?",
        "answer": (
            "Điểm quá trình môn Điện toán đám mây chiếm 60% tổng điểm đánh giá."
        ),
        "keywords": [
            "điểm quá trình",
            "60%",
            "tỷ lệ điểm",
            "đánh giá"
        ],
        "category": "cach_tinh_diem"
    },

    {
        "question": "Điểm thi cuối kỳ môn Điện toán đám mây chiếm bao nhiêu phần trăm?",
        "answer": (
            "Điểm thi cuối kỳ môn Điện toán đám mây chiếm 40% tổng điểm đánh giá."
        ),
        "keywords": [
            "điểm cuối kỳ",
            "thi cuối kỳ",
            "40%",
            "tỷ lệ điểm"
        ],
        "category": "cach_tinh_diem"
    },

    {
        "question": "Điểm chuyên cần môn Điện toán đám mây chiếm bao nhiêu phần trăm?",
        "answer": (
            "Điểm chuyên cần chiếm 10% tổng điểm đánh giá môn Điện toán đám mây."
        ),
        "keywords": [
            "chuyên cần",
            "10%",
            "điểm chuyên cần",
            "tỷ lệ điểm"
        ],
        "category": "cach_tinh_diem"
    },

    {
        "question": "Bài tập và thực hành trên lớp chiếm bao nhiêu phần trăm điểm môn Điện toán đám mây?",
        "answer": (
            "Bài tập, thực hành trên lớp và kiểm tra giữa kỳ L1, L2 "
            "chiếm 20% tổng điểm đánh giá."
        ),
        "keywords": [
            "bài tập",
            "thực hành",
            "kiểm tra giữa kỳ",
            "L1",
            "L2",
            "20%"
        ],
        "category": "cach_tinh_diem"
    },

    {
        "question": "Bài tập lớn môn Điện toán đám mây chiếm bao nhiêu phần trăm?",
        "answer": (
            "Bài tập lớn theo nhóm, bao gồm báo cáo và thuyết trình, "
            "chiếm 30% tổng điểm đánh giá."
        ),
        "keywords": [
            "bài tập lớn",
            "làm nhóm",
            "báo cáo",
            "thuyết trình",
            "30%"
        ],
        "category": "cach_tinh_diem"
    },

    {
        "question": "Bài thi cuối kỳ môn Điện toán đám mây có hình thức gì?",
        "answer": (
            "Bài thi cuối kỳ chiếm 40% tổng điểm và có hình thức "
            "trắc nghiệm trực quan trên máy tính."
        ),
        "keywords": [
            "thi cuối kỳ",
            "hình thức thi",
            "trắc nghiệm",
            "máy tính",
            "40%"
        ],
        "category": "cach_tinh_diem"
    },


    # =========================================================
    # 6. TÀI LIỆU & KHO HỌC LIỆU
    # =========================================================
    {
        "question": "Tài liệu chính để học môn Điện toán đám mây là gì?",
        "answer": (
            "Tài liệu chính để học tập gồm: "
            "\"Điện toán đám mây\" (2020) của Huỳnh Quyết Thắng "
            "và \"Cloud Computing: Theory and Practice\" (2022) "
            "của Dan Marinescu, 3rd Edition."
        ),
        "keywords": [
            "tài liệu chính",
            "giáo trình",
            "Điện toán đám mây",
            "Huỳnh Quyết Thắng",
            "Cloud Computing Theory and Practice",
            "Dan Marinescu"
        ],
        "category": "tai_lieu"
    },

    {
        "question": "Tài liệu môn Điện toán đám mây được tải ở đâu?",
        "answer": (
            "Sinh viên sử dụng email có tên miền ut.edu.vn để đăng nhập "
            "và download tài liệu tại trang courses.ut.edu.vn."
        ),
        "keywords": [
            "tải tài liệu",
            "download tài liệu",
            "courses.ut.edu.vn",
            "ut.edu.vn",
            "kho học liệu"
        ],
        "category": "tai_lieu"
    },

    {
        "question": "Ai có thể download tài liệu môn Điện toán đám mây?",
        "answer": (
            "Chỉ sinh viên có địa chỉ email với tên miền ut.edu.vn "
            "mới có thể download tài liệu."
        ),
        "keywords": [
            "download",
            "tài liệu",
            "email",
            "ut.edu.vn",
            "sinh viên"
        ],
        "category": "tai_lieu"
    },

    {
        "question": "Kho học liệu môn Điện toán đám mây có những gì?",
        "answer": (
            "Kho học liệu gồm tài liệu tham khảo, bài tập, video bài giảng, "
            "câu hỏi kiểm tra trắc nghiệm trực quan và các tài liệu phục vụ học tập khác."
        ),
        "keywords": [
            "kho học liệu",
            "bài tập",
            "video bài giảng",
            "câu hỏi trắc nghiệm",
            "tài liệu tham khảo"
        ],
        "category": "tai_lieu"
    },

    {
        "question": "Tài liệu môn Điện toán đám mây được sắp xếp như thế nào trên courses.ut.edu.vn?",
        "answer": (
            "Tài liệu đã được đánh số. Vì vậy, từng bài học trên trang "
            "courses.ut.edu.vn sẽ được ghi số tương ứng. Tài liệu không được "
            "đính kèm theo từng chương mục nhằm tiết kiệm không gian lưu trữ."
        ),
        "keywords": [
            "courses.ut.edu.vn",
            "đánh số tài liệu",
            "bài học",
            "chương mục",
            "sắp xếp tài liệu"
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