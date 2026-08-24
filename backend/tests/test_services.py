import pytest
from unittest.mock import AsyncMock

import app.services.chat_service as chat_service_module
from app.services.chat_service import ChatService


@pytest.mark.asyncio
async def test_chat_service_faq_hit(monkeypatch):
    """Test câu hỏi khớp FAQ → trả lời bằng Rule-based."""

    # Mock FAQ Repository
    mock_faq_repo = AsyncMock()
    mock_faq_repo.find_matching.return_value = {
        "question": "Môn Điện toán đám mây có bao nhiêu tín chỉ?",
        "answer": "Môn Điện toán đám mây có 3 tín chỉ."
    }

    # Mock Gemini Service
    mock_gemini = AsyncMock()

    # Mock Chat Log Repository
    mock_chat_log = AsyncMock()

    # Thay các class thật bằng Mock
    monkeypatch.setattr(
        chat_service_module,
        "FAQRepository",
        lambda: mock_faq_repo
    )

    monkeypatch.setattr(
        chat_service_module,
        "GeminiService",
        lambda: mock_gemini
    )

    monkeypatch.setattr(
        chat_service_module,
        "ChatLogRepository",
        lambda: mock_chat_log
    )

    # Khởi tạo ChatService sau khi đã mock
    service = ChatService()

    result = await service.process_message(
        session_id="test01",
        message="Môn Điện toán đám mây có bao nhiêu tín chỉ?"
    )

    # Kiểm tra kết quả
    assert result["answer"] == "Môn Điện toán đám mây có 3 tín chỉ."
    assert result["source"] == "rule"

    # FAQ phải được gọi
    mock_faq_repo.find_matching.assert_awaited_once_with(
        "Môn Điện toán đám mây có bao nhiêu tín chỉ?"
    )

    # Vì đã tìm thấy FAQ → Gemini KHÔNG được gọi
    mock_gemini.generate_response.assert_not_awaited()

    # Phải lưu lịch sử chat
    mock_chat_log.create.assert_awaited_once()


@pytest.mark.asyncio
async def test_chat_service_ai_fallback(monkeypatch):
    """Test không tìm thấy FAQ → chuyển sang Gemini."""

    # Mock FAQ Repository
    mock_faq_repo = AsyncMock()
    mock_faq_repo.find_matching.return_value = None

    # Mock Gemini Service
    mock_gemini = AsyncMock()
    mock_gemini.generate_response.return_value = (
        "Điện toán đám mây là mô hình cung cấp tài nguyên CNTT qua Internet."
    )

    # Mock Chat Log Repository
    mock_chat_log = AsyncMock()

    # Thay các class thật bằng Mock
    monkeypatch.setattr(
        chat_service_module,
        "FAQRepository",
        lambda: mock_faq_repo
    )

    monkeypatch.setattr(
        chat_service_module,
        "GeminiService",
        lambda: mock_gemini
    )

    monkeypatch.setattr(
        chat_service_module,
        "ChatLogRepository",
        lambda: mock_chat_log
    )

    # Khởi tạo ChatService
    service = ChatService()

    result = await service.process_message(
        session_id="test02",
        message="Điện toán đám mây khác máy chủ truyền thống như thế nào?"
    )

    # Kiểm tra kết quả
    assert result["answer"] == (
        "Điện toán đám mây là mô hình cung cấp tài nguyên CNTT qua Internet."
    )
    assert result["source"] == "gemini"

    # FAQ phải được gọi trước
    mock_faq_repo.find_matching.assert_awaited_once_with(
        "Điện toán đám mây khác máy chủ truyền thống như thế nào?"
    )

    # Không có FAQ → Gemini phải được gọi
    mock_gemini.generate_response.assert_awaited_once_with(
        "Điện toán đám mây khác máy chủ truyền thống như thế nào?"
    )

    # Phải lưu lịch sử chat
    mock_chat_log.create.assert_awaited_once()