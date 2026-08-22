import os
from pathlib import Path
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.security import get_password_hash

# Load file .env từ thư mục gốc dự án
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class AdminRepository:
    def __init__(self, db_client=None):
        if db_client:
            self.db = db_client["study_chatbot_db"]
        else:
            mongo_url = os.getenv("MONGODB_URL")
            if not mongo_url:
                raise ValueError("Không tìm thấy MONGODB_URL trong file .env!")
            client = AsyncIOMotorClient(mongo_url)
            self.db = client["study_chatbot_db"]
        self.collection = self.db["admins"]

    async def get_by_username(self, username: str):
        return await self.collection.find_one({"username": username})

    async def init_default_admin(self):
        """Khởi tạo tài khoản admin mặc định nếu chưa tồn tại"""
        existing_admin = await self.get_by_username("admin")
        if not existing_admin:
            hashed_pwd = get_password_hash("admin123")  # Mật khẩu mặc định
            await self.collection.insert_one({
                "username": "admin",
                "password": hashed_pwd,
                "role": "admin"
            })
            print("--> Đã khởi tạo tài khoản Admin mặc định thành công! (username: admin / pass: admin123)")
        else:
            print("--> Tài khoản Admin đã tồn tại sẵn trong MongoDB Atlas.")