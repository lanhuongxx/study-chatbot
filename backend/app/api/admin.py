from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.admin import AdminLogin, TokenResponse
from app.repositories.admin_repository import AdminRepository
from app.repositories.chat_log_repository import ChatLogRepository  # Import ChatLogRepo
from app.core.security import verify_password, create_access_token
from app.core.dependencies import require_admin  # Import dependency bảo vệ route

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin Auth & Management"]
)

admin_repo = AdminRepository()
chat_log_repo = ChatLogRepository()

@router.post("/login", response_model=TokenResponse)
async def login(credentials: AdminLogin):
    admin = await admin_repo.get_by_username(credentials.username)
    if not admin or not verify_password(credentials.password, admin["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản hoặc mật khẩu không chính xác"
        )
    
    access_token = create_access_token(data={"sub": admin["username"], "role": admin.get("role", "admin")})
    return TokenResponse(access_token=access_token)

# API Xem Lịch sử ChatLogs dành riêng cho Admin
@router.get("/chat-logs", dependencies=[Depends(require_admin)])
async def get_chat_logs(
    skip: int = 0,
    limit: int = 20,
    source: Optional[str] = None  # Lọc theo 'rule' hoặc 'gemini'
):
    """Admin xem toàn bộ danh sách lịch sử trò chuyện của người dùng"""
    logs = await chat_log_repo.get_logs(skip=skip, limit=limit, source=source)
    return {
        "status": "success",
        "total": len(logs),
        "data": logs
    }