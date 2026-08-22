import asyncio
from app.repositories.admin_repository import AdminRepository

async def main():
    repo = AdminRepository()
    await repo.init_default_admin()

if __name__ == "__main__":
    asyncio.run(main())