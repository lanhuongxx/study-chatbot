from fastapi import APIRouter, HTTPException, status
from app.schemas.admin import AdminLogin, TokenResponse
from app.repositories.admin_repository import AdminRepository
from app.core.security import verify_password, create_access_token

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin Auth"]
)

admin_repo = AdminRepository()

@router.post("/login", response_model=TokenResponse)
async def login(credentials: AdminLogin):
    admin = await admin_repo.get_by_username(credentials.username)
    if not admin or not verify_password(credentials.password, admin["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản hoặc mật khẩu không chính xác"
        )
    
    # Tạo JWT Token chứa thông tin username và role
    access_token = create_access_token(data={"sub": admin["username"], "role": admin.get("role", "admin")})
    return TokenResponse(access_token=access_token)