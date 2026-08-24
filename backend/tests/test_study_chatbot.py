import pytest
from httpx import AsyncClient


# --- 1. TEST CHAT API ---
@pytest.mark.asyncio
async def test_chat_faq_success(client: AsyncClient):
    payload = {
        "session_id": "pytest_session_001",
        "message": "dang ky hoc phan o dau"
    }
    response = await client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["source"] in ["rule", "gemini"]


# --- 2. TEST HISTORY API ---
@pytest.mark.asyncio
async def test_get_chat_history_success(client: AsyncClient):
    session_id = "pytest_session_001"
    response = await client.get(f"/api/history/{session_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == session_id
    assert isinstance(data["history"], list)


# --- 3. TEST FAQ LIST ---
@pytest.mark.asyncio
async def test_get_faqs_list(client: AsyncClient):
    response = await client.get("/api/faqs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# --- 4. TEST ADMIN AUTH ---
@pytest.mark.asyncio
async def test_admin_chat_logs_unauthorized(client: AsyncClient):
    response = await client.get("/api/admin/chat-logs")
    assert response.status_code in [401, 403]