import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app  # Import app FastAPI chính của bạn

@pytest.mark.asyncio
async def test_chat_faq_rule_match():
    """
    Test Case 1: Input khớp từ khóa FAQ trong Database
    Kỳ vọng: Trả về câu trả lời với source là 'rule'
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Gửi câu hỏi khớp với keyword/FAQ đã tạo sẵn trong DB
        payload = {"message": "thủ tục đăng ký học phần"}
        response = await client.post("/api/chat", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        
        # Kiểm tra trường source trả về đúng dạng 'rule'
        assert data.get("source") == "rule"
        assert "reply" in data

@pytest.mark.asyncio
async def test_chat_gemini_fallback():
    """
    Test Case 2: Input câu hỏi lạ không có trong FAQ
    Kỳ vọng: Trả về câu trả lời do AI Gemini sinh ra với source là 'gemini'
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Gửi câu hỏi hoàn toàn ngẫu nhiên/không thuộc FAQ
        payload = {"message": "Thời tiết hôm nay thế nào?"}
        response = await client.post("/api/chat", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        
        # Kiểm tra trường source trả về đúng dạng 'gemini'
        assert data.get("source") == "gemini"
        assert "reply" in data