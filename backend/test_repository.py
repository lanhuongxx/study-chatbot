import asyncio

from app.repositories.faq_repository import FAQRepository


async def main():
    repository = FAQRepository()

    print("=== TEST FIND MATCHING ===")

    message = "Môn này có mấy tín chỉ vậy?" 

    faq = await repository.find_matching(message)

    if faq:
        print("Tìm thấy FAQ:")
        print(faq)
    else:
        print("Không tìm thấy FAQ.")


if __name__ == "__main__":
    asyncio.run(main())