# 보안 퀴즈 오답 저장
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List
from datetime import datetime
from firebase_admin import firestore

router = APIRouter()
db = firestore.client()

class MistakeItem(BaseModel):
    case_id: int
    title: str
    mistake: str

class MistakePayload(BaseModel):
    wrong_cases: List[MistakeItem]

@router.post("/security_education/upload_mistake")
def upload_security_mistake(request: Request, payload: MistakePayload):
    user_id = request.headers.get("user-id")

    if not user_id:
        raise HTTPException(status_code=400, detail="user-id 헤더가 누락되었습니다.")

    doc_ref = db.collection("security_quiz_mistakesbackup_byuser").document(user_id)

    doc_ref.set({
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "wrong_cases": [item.dict() for item in payload.wrong_cases]
    })

    return {"message": f"{user_id} 오답 기록 저장 완료"}
