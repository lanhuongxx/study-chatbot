# 🎓 Study Chatbot - Backend API

Hệ thống Backend API cho ứng dụng Chatbot hỗ trợ sinh viên giải đáp thắc mắc môn học/quy chế. Hệ thống kết hợp cơ chế **Rule-based Matching Engine** (truy vấn dữ liệu FAQ từ MongoDB) và **AI Fallback** (sử dụng Google Gemini API).

---

## 🛠️ Công Nghệ Sử Dụng (Tech Stack)

* **Language:** Python 3.13+
* **Framework:** FastAPI
* **Database:** MongoDB Atlas (Async Driver: `motor`)
* **AI Model:** Google Gemini API (`google-genai` / `google-generativeai`)
* **Authentication:** JWT (JSON Web Tokens), `pwdlib[bcrypt]`
* **Environment Management:** `python-dotenv`

---

## 🏗️ Cấu Trúc Thư Mục (Project Structure)

```text
backend/
├── app/
│   ├── api/                   # Router endpoints (chat, faq, admin)
│   │   ├── admin.py
│   │   ├── chat.py
│   │   └── faq.py
│   ├── core/                  # Security, config & dependencies
│   │   ├── dependencies.py
│   │   └── security.py
│   ├── models/                # Database models
│   │   ├── chat_log.py
│   │   └── faq.py
│   ├── repositories/          # Data Access Layer (MongoDB queries)
│   │   ├── admin_repository.py
│   │   ├── chat_log_repository.py
│   │   └── faq_repository.py
│   ├── schemas/               # Pydantic Schemas (Validation)
│   │   ├── admin.py
│   │   ├── chat.py
│   │   └── faq.py
│   ├── services/              # Business Logic & External APIs
│   │   ├── gemini_service.py
│   │   └── rule_engine.py
│   ├── database.py            # MongoDB Connection
│   └── main.py                # FastAPI Application Entrypoint
├── .env                       # Environment Variables (Not committed)
├── init_admin.py              # Script khởi tạo Admin User mặc định
├── requirements.txt           # Python dependencies
└── README.md                  # Project Documentation

⚙️ Hướng Dẫn Cài Đặt & Chạy Local
1. Yêu cầu tiên quyết
- Python 3.10+
- Tài khoản MongoDB Atlas (hoặc MongoDB Local)
- Gemini API Key từ Google AI Studio

2. Cài đặt môi trường
Khởi tạo và kích hoạt môi trường ảo:
python -m venv .venv
# Trên Windows:
.\.venv\Scripts\activate
# Trên macOS/Linux:
source .venv/bin/activate

Cài đặt các gói thư viện phụ thuộc:
pip install -r requirements.txt

3. Cấu hình file môi trường (.env)
Tạo file .env tại thư mục backend/ với nội dung mẫu:
MONGODB_URL=mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=super_secret_chatbot_key_2026

4. Khởi tạo tài khoản Admin
Chạy script để khởi tạo tài khoản Admin mặc định (admin / admin123):
python init_admin.py

5. Khởi chạy Server
uvicorn app.main:app --reload

API Server: http://127.0.0.1:8000

Interactive API Docs (Swagger UI): http://127.0.0.1:8000/docs

