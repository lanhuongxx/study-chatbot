import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Import routers
from app.api.chat import router as chat_router
from app.api.faq import router as faq_router
from app.api.admin import router as admin_router


# ============================================================
# 1. Load file .env
# ============================================================

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

MONGODB_URL = os.getenv("MONGODB_URL")

if not MONGODB_URL:
    raise ValueError("MONGODB_URL chưa được cấu hình trong file .env")


# ============================================================
# 2. Khởi tạo FastAPI - CHỈ MỘT LẦN
# ============================================================

app = FastAPI(title="Study Chatbot API Test")


# ============================================================
# 3. Cấu hình CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# 4. Kết nối MongoDB
# ============================================================

client = AsyncIOMotorClient(MONGODB_URL)

# Database dùng cho các API test cũ
db = client["study_chatbot_db"]
messages_collection = db["chat_messages"]


# ============================================================
# 5. Model cho API test /messages
# ============================================================

class ChatMessage(BaseModel):
    user_id: str
    message: str


# ============================================================
# 6. Include các router của project
# ============================================================

app.include_router(chat_router)
app.include_router(faq_router)
app.include_router(admin_router)


# ============================================================
# 7. API test kết nối MongoDB
# ============================================================

@app.get("/test-connection")
async def test_connection():
    try:
        await client.admin.command("ping")

        return {
            "status": "success",
            "message": "Kết nối MongoDB Atlas thành công!"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi kết nối MongoDB: {str(e)}"
        )


# ============================================================
# 8. API test Insert
# ============================================================

@app.post("/messages")
async def create_message(data: ChatMessage):

    new_message = {
        "user_id": data.user_id,
        "message": data.message,
    }

    try:
        result = await messages_collection.insert_one(new_message)

        return {
            "status": "success",
            "inserted_id": str(result.inserted_id),
            "data": new_message
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi lưu message: {str(e)}"
        )


# ============================================================
# 9. API test Read
# ============================================================

@app.get("/messages")
async def get_messages():

    messages = []

    try:
        cursor = messages_collection.find()

        async for document in cursor:
            document["_id"] = str(document["_id"])
            messages.append(document)

        return {
            "status": "success",
            "total": len(messages),
            "data": messages
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi đọc messages: {str(e)}"
        )


# ============================================================
# 10. Cấu hình CORS cho phép Frontend truy cập
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://study-chatbot-rjsr.onrender.com", # Cho phép tất cả domain Render
        "*"                       # Hoặc tạm thời dùng "*" để test nhanh không lo chặn CORS
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)