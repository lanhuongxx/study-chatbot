from pydantic import BaseModel, Field
from typing import List


class FAQCreate(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    answer: str = Field(..., min_length=1, max_length=2000)
    keywords: List[str] = Field(default_factory=list)
    category: str = Field(..., min_length=1, max_length=100)


class FAQResponse(FAQCreate):
    id: str