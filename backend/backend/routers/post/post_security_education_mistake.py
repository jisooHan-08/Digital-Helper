# post_security_education_mistake.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from firebase_admin import firestore

router = APIRouter()
db = firestore.client()

# 개별 오답 항목
class MistakeItem(BaseModel):
    case_id: int
    title: str
    mistake: str  # 어떤 실수/오답을 했는지 설명

# 전체 payload
class MistakePayload(BaseModel):
    user_id: str
    wrong_cases: List[MistakeItem]

# 오답 저장 API
@router.post("/security_education/upload_mistake")
def upload_security_mistake(payload: MistakePayload):
    doc_ref = db.collection("security_education_mistakes_byuser").document(payload.user_id)
    
    doc_ref.set({
        "user_id": payload.user_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "wrong_cases": [item.dict() for item in payload.wrong_cases]
    })

    return {"message": "오답 기록 저장 완료"}
