import asyncio
from app.repositories.admin_repository import AdminRepository


async def main():
    print("⏳ Đang khởi tạo tài khoản Admin mặc định...")
    repo = AdminRepository()
    
    # Gọi hàm tạo admin mặc định
    await repo.init_default_admin()
    print("✅ Khởi tạo Admin hoàn tất! (Tài khoản: admin / Mật khẩu: admin123)")

if __name__ == "__main__":
    asyncio.run(main())