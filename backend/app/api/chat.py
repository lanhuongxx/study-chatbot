from fastapi import APIRouter

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