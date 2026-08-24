from fastapi import APIRouter, Query

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService


router = APIRouter(
    prefix="/api",
    tags=["Chat"]
)

chat_service = ChatService()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    result = await chat_service.process_message(
        session_id=request.session_id,
        message=request.message
    )
    return result


@router.get("/history/{session_id}")
async def get_chat_history(
    session_id: str,
    limit: int = Query(default=50, ge=1, le=100)
):
    """
    Lấy lịch sử trò chuyện dựa trên session_id.
    - **session_id**: Mã phiên làm việc của người dùng
    - **limit**: Số lượng tin nhắn tối đa trả về (mặc định 50)
    """
    history = await chat_service.get_history(session_id=session_id, limit=limit)
    return {
        "session_id": session_id,
        "total_messages": len(history),
        "history": history
    }