import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Import chat router
from app.api.chat import router as chat_router
from app.api.faq import router as faq_router
from app.api.admin import router as admin_router

# 1. Load file .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb+srv://lethilanhuong666_db_user:rMZuCqJJ7Vv7zdO3@chatbot-sv.6y3nemu.mongodb.net/?appName=chatbot-sv")

# 2. Khởi tạo FastAPI
app = FastAPI(title="Study Chatbot API Test")

# Cấu hình CORS cho phép Frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Bật cho tất cả nguồn (hoặc điền port React/Vue của bạn)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Kết nối Chat Router vào ứng dụng FastAPI
app.include_router(chat_router)

client = AsyncIOMotorClient(MONGODB_URL)
db = client["study_chatbot_db"]
messages_collection = db["chat_messages"]

# 3. Model định dạng dữ liệu truyền vào (Pydantic)
class ChatMessage(BaseModel):
    user_id: str
    message: str

# 4. API 1: Test kết nối MongoDB
@app.get("/test-connection")
async def test_connection():
    try:
        await client.admin.command('ping')
        return {"status": "success", "message": "Kết nối MongoDB Atlas thành công!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi kết nối MongoDB: {str(e)}")

# 5. API 2: Test Insert
@app.post("/messages")
async def create_message(data: ChatMessage):
    new_message = {
        "user_id": data.user_id,
        "message": data.message,
    }
    result = await messages_collection.insert_one(new_message)
    return {
        "status": "success",
        "inserted_id": str(result.inserted_id),
        "data": new_message
    }

# 6. API 3: Test Read
@app.get("/messages")
async def get_messages():
    messages = []
    cursor = messages_collection.find()
    async for document in cursor:
        document["_id"] = str(document["_id"])
        messages.append(document)
    return {
        "status": "success",
        "total": len(messages),
        "data": messages
    }

app = FastAPI(title="Study Chatbot API Test")

# Nhúng các router vào FastAPI
app.include_router(chat_router)
app.include_router(faq_router)
app.include_router(admin_router)