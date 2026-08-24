import pytest


@pytest.mark.asyncio
async def test_chat_faq_success(client):
    """Test POST /api/chat với câu hỏi có trong FAQ."""

    response = await client.post(
        "/api/chat",
        json={
            "session_id": "integration_test_01",
            "message": "Môn Điện toán đám mây có bao nhiêu tín chỉ?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "source" in data
    assert "timestamp" in data

    assert "3 tín chỉ" in data["answer"]
    assert data["source"] == "rule"


@pytest.mark.asyncio
async def test_get_faqs_list(client):
    """Test GET /api/faqs lấy danh sách FAQ."""

    response = await client.get("/api/faqs")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_chat_history_success(client):
    """Test lấy lịch sử chat theo session_id."""

    session_id = "integration_test_history"

    # Tạo một chat trước
    chat_response = await client.post(
        "/api/chat",
        json={
            "session_id": session_id,
            "message": "Môn Điện toán đám mây có bao nhiêu tín chỉ?"
        }
    )

    assert chat_response.status_code == 200

    # Lấy lịch sử
    response = await client.get(
        f"/api/history/{session_id}"
    )

    assert response.status_code == 200

    data = response.json()

    # API trả về object chứa thông tin session và history
    assert isinstance(data, dict)

    assert "session_id" in data
    assert "total_messages" in data
    assert "history" in data

    assert data["session_id"] == session_id
    assert isinstance(data["history"], list)
    assert len(data["history"]) > 0

    # Kiểm tra nội dung lịch sử
    history = data["history"]

    assert history[0]["session_id"] == session_id
    assert history[0]["user_message"] == (
        "Môn Điện toán đám mây có bao nhiêu tín chỉ?"
    )
    assert history[0]["bot_response"] == (
        "Môn Điện toán đám mây có 3 tín chỉ."
    )
    assert history[0]["source"] == "rule"