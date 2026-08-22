import os
from dotenv import load_dotenv

load_dotenv()

mongo_url = os.getenv("MONGODB_URL")

if mongo_url:
    print("MONGODB_URL đã được đọc.")
    print("Bắt đầu bằng:", mongo_url[:20])
else:
    print("MONGODB_URL KHÔNG được tìm thấy.")