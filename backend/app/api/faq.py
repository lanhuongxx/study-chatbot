from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status, Depends  # <--- Bổ sung Depends

from app.schemas.faq import FAQCreate, FAQResponse
from app.repositories.faq_repository import FAQRepository
from app.services.gemini_service import GeminiService
from app.core.dependencies import require_admin  # <--- Import require_admin

router = APIRouter(
    prefix="/api/faqs",
    tags=["FAQ Management"]
)

# Truyền gemini_service để FAQ tạo/sửa qua admin panel cũng có embedding
# ngay lập tức, không cần chạy lại seed_faqs.py thủ công.
faq_repo = FAQRepository(gemini_service=GeminiService())

# GET FAQ cho phép sinh viên xem công khai (Không khóa)
@router.get("", response_model=List[FAQResponse])
async def get_faqs(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100), category: Optional[str] = None):
    return await faq_repo.get_all(skip=skip, limit=limit, category=category)

@router.get("/{faq_id}", response_model=FAQResponse)
async def get_faq_by_id(faq_id: str):
    faq = await faq_repo.get_by_id(faq_id)
    if not faq:
        raise HTTPException(status_code=404, detail="Không tìm thấy FAQ")
    return faq

# Khóa POST, PUT, DELETE yêu cầu đăng nhập Admin
@router.post("", response_model=FAQResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
async def create_faq(faq_in: FAQCreate):
    return await faq_repo.create(faq_in.model_dump())

@router.put("/{faq_id}", response_model=FAQResponse, dependencies=[Depends(require_admin)])
async def update_faq(faq_id: str, faq_in: FAQCreate):
    updated_faq = await faq_repo.update(faq_id, faq_in.model_dump())
    if not updated_faq:
        raise HTTPException(status_code=404, detail="Không tìm thấy FAQ để cập nhật")
    return updated_faq

@router.delete("/{faq_id}", dependencies=[Depends(require_admin)])
async def delete_faq(faq_id: str):
    success = await faq_repo.delete(faq_id)
    if not success:
        raise HTTPException(status_code=404, detail="Không tìm thấy FAQ để xóa")
    return {"status": "success", "message": f"Đã xóa thành công FAQ có ID: {faq_id}"}