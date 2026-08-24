import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGODB_URL")
client = AsyncIOMotorClient(MONGO_URL)
database = client["study_chatbot_db"] # Tên database của bạn

async def check_connection():
    try:
        await client.admin.command("ping")

        print("Kết nối MongoDB Atlas thành công!")
        print("Database đang sử dụng:", database.name)

        collections = await database.list_collection_names()
        print("Collections:", collections)

    except Exception as e:
        print(f"Lỗi kết nối: {e}")