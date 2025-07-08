from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List
from datetime import datetime, timezone
from firebase_init import db

router = APIRouter()

# 오답 항목 모델 정의
class MistakeItem(BaseModel):
    correct: str
    question: str
    scenario_id: str
    scenario_title: str
    selected: str
    step_index: int

# 전체 업로드 요청 모델
class MistakeUploadRequest(BaseModel):
    wrong_selections: List[MistakeItem]

@router.post("/restaurant-kiosk/mistake")
def upload_restaurant_kiosk_mistake(request: Request, data: MistakeUploadRequest):
    user_id = request.headers.get("user-id")

    if not user_id:
        raise HTTPException(status_code=400, detail="user-id 헤더가 누락되었습니다.")

    # 문서 참조
    doc_ref = db.collection("restaurant_kiosk_mistakesbackup_byuser").document(user_id)

    # 기존 데이터 불러오기 (없으면 빈 리스트)
    existing_doc = doc_ref.get()
    existing_data = existing_doc.to_dict() if existing_doc.exists else {}
    existing_mistakes = existing_data.get("wrong_selections", [])

    # 타임스탬프 추가 후 병합
    new_entries = []
    for item in data.wrong_selections:
        entry = item.dict()
        entry["timestamp"] = datetime.now(timezone.utc).isoformat()
        new_entries.append(entry)

    updated_mistakes = existing_mistakes + new_entries

    # Firestore에 저장
    doc_ref.set({
        "wrong_selections": updated_mistakes
    })

    return {
        "message": f"{user_id}의 오답 기록이 {len(new_entries)}개 추가되었습니다.",
        "total_mistakes": len(updated_mistakes)
    }
