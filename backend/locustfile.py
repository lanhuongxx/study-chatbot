import random
import uuid

from locust import HttpUser, task, between


class StudyChatbotUser(HttpUser):
    """
    Mô phỏng một sinh viên sử dụng Study Chatbot.
    """

    wait_time = between(1, 3)

    def on_start(self):
        # Mỗi user có một session_id riêng
        self.session_id = f"locust-{uuid.uuid4()}"

        # Các câu hỏi có khả năng FAQ hit
        self.faq_questions = [
            "Học phần này có bao nhiêu tín chỉ?",
            "Lịch thi diễn ra vào tuần nào?",
        ]

        # Các câu hỏi dùng để kiểm tra AI fallback
        self.ai_questions = [
            "Hãy giải thích cho tôi về nội dung của môn học.",
            "Tôi nên học môn này như thế nào để đạt kết quả tốt?",
            "Hãy đưa ra một số lời khuyên để ôn tập môn học.",
        ]

    @task(5)
    def chat_faq(self):
        """
        Gửi câu hỏi thuộc nhóm FAQ.
        Weight = 5
        """
        message = random.choice(self.faq_questions)

        with self.client.post(
            "/api/chat",
            json={
                "session_id": self.session_id,
                "message": message,
            },
            name="POST /api/chat - FAQ",
            catch_response=True,
        ) as response:

            if response.status_code == 200:
                try:
                    data = response.json()

                    if "answer" not in data:
                        response.failure(
                            "Response không có field 'answer'"
                        )
                    elif "source" not in data:
                        response.failure(
                            "Response không có field 'source'"
                        )
                    else:
                        response.success()

                except ValueError:
                    response.failure("Response không phải JSON")

            else:
                response.failure(
                    f"Expected 200, got {response.status_code}"
                )

    @task(2)
    def chat_ai_fallback(self):
        """
        Gửi câu hỏi không thuộc FAQ để kiểm tra AI fallback.
        Weight = 2
        """
        message = random.choice(self.ai_questions)

        with self.client.post(
            "/api/chat",
            json={
                "session_id": self.session_id,
                "message": message,
            },
            name="POST /api/chat - AI Fallback",
            catch_response=True,
        ) as response:

            if response.status_code == 200:
                try:
                    data = response.json()

                    if "answer" not in data:
                        response.failure(
                            "Response không có field 'answer'"
                        )
                    else:
                        response.success()

                except ValueError:
                    response.failure("Response không phải JSON")

            else:
                response.failure(
                    f"Expected 200, got {response.status_code}"
                )

    @task(2)
    def get_faqs(self):
        """
        Lấy danh sách FAQ.
        Weight = 2
        """
        with self.client.get(
            "/api/faqs",
            name="GET /api/faqs",
            catch_response=True,
        ) as response:

            if response.status_code == 200:
                try:
                    response.json()
                    response.success()
                except ValueError:
                    response.failure("Response không phải JSON")
            else:
                response.failure(
                    f"Expected 200, got {response.status_code}"
                )

    @task(1)
    def get_chat_history(self):
        """
        Lấy lịch sử chat của session hiện tại.
        Weight = 1
        """
        with self.client.get(
            f"/api/history/{self.session_id}",
            name="GET /api/history/{session_id}",
            catch_response=True,
        ) as response:

            if response.status_code == 200:
                try:
                    data = response.json()

                    if "session_id" not in data:
                        response.failure(
                            "Response không có field 'session_id'"
                        )
                    elif "history" not in data:
                        response.failure(
                            "Response không có field 'history'"
                        )
                    else:
                        response.success()

                except ValueError:
                    response.failure("Response không phải JSON")

            else:
                response.failure(
                    f"Expected 200, got {response.status_code}"
                )