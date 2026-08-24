# 🤖 Study Chatbot - Backend API

Hệ thống API Backend cho Chatbot hỗ trợ học tập, tích hợp tìm kiếm FAQ thông minh từ cơ sở dữ liệu và tự động trả lời câu hỏi bằng Google Gemini API.

---

## 🚀 Demo & Online Documentation

* **Live API Base URL:** `https://study-chatbot-backend.onrender.com`
* **Interactive API Docs (Swagger UI):** [https://study-chatbot-backend.onrender.com/docs](https://study-chatbot-backend.onrender.com/docs)

---

## 🛠️ Công Nghệ Sử Dụng

* **Framework:** Python 3.12+ / FastAPI
* **Database:** MongoDB Atlas (sử dụng `motor` làm async driver)
* **LLM / AI Integration:** Google Gemini API (`google-genai` / `google-generativeai`)
* **Authentication & Security:** JWT (JSON Web Tokens), Passlib (Bcrypt)
* **Deployment:** Render (Web Service)

---

## 📂 Cấu Trúc Thư Mục Backend

```text
backend/
├── app/
│   ├── api/             # Các route API (chat, faqs, auth,...)
│   ├── core/            # Config, security, dependencies
│   ├── models/          # Schemas Pydantic
│   ├── repositories/    # Xử lý truy vấn MongoDB
│   ├── services/        # Logic nghiệp vụ (Gemini API, RAG/FAQ match)
│   └── main.py          # Entry point chính của FastAPI
├── .env.example         # File mẫu cấu hình biến môi trường
├── Procfile             # File cấu hình lệnh chạy trên Render
├── requirements.txt     # Danh sách thư viện Python
└── seed_faqs.py         # Script khởi tạo dữ liệu FAQ mẫu

⚙️ Hướng Dẫn Cài Đặt & Chạy Local
1. Yêu cầu tiên quyết
- Python 3.10+
- Tài khoản MongoDB Atlas (hoặc MongoDB Local)
- Gemini API Key từ Google AI Studio

2. Clone Repository & Chuyển Thư Mục
git clone https://github.com/lanhuongxx/study-chatbot.git

3. Cài đặt môi trường
Khởi tạo và kích hoạt môi trường ảo:
python -m venv .venv
# Trên Windows:
.\.venv\Scripts\activate
# Trên macOS/Linux:
source .venv/bin/activate

Cài đặt các gói thư viện phụ thuộc:
pip install -r requirements.txt

4. Cấu hình file môi trường (.env)
Tạo file .env tại thư mục backend/ với nội dung mẫu:
MONGODB_URL=mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
GEMINI_API_KEY=your_gemini_api_key_here
JWT_SECRET=super_secret_chatbot_key_2026
ALGORITHM=HS256

5. Khởi Tạo Tài Khoản Admin Mặc Định
Chạy script để tạo tài khoản Admin ban đầu trong database:
```bash
python init_admin.py

6. Nạp dữ liệu FAQ Mẫu (Optional)
python seed_faqs.py

7. Khởi chạy Server
uvicorn app.main:app --reload

API Server: http://127.0.0.1:8000

Interactive API Docs (Swagger UI): http://127.0.0.1:8000/docs

NOTE: 
Để kết nối Frontend tới Backend đã deploy, cập nhật Base URL API trong dự án Frontend thành
[https://study-chatbot-backend.onrender.com](https://study-chatbot-backend.onrender.com)
CORS đã được cấu hình cho phép toàn bộ requests.