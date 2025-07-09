# 병원 키오스크 오답 저장
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse  
from pydantic import BaseModel
from typing import List
from datetime import datetime, timezone

from firebase_init import db  

router = APIRouter()

class MistakeItem(BaseModel):
    scenario_id: str
    scenario_title: str
    step_index: int
    question: str
    selected: str
    correct: str

class MistakeUploadRequest(BaseModel):
    wrong_selections: List[MistakeItem]

@router.post("/hospital-kiosk/mistake")
def upload_hospital_kiosk_mistake(request: Request, data: MistakeUploadRequest):
    user_id = request.headers.get("user-id")

    if not user_id:
        raise HTTPException(status_code=400, detail="user-id 헤더가 누락되었습니다.")

    doc_ref = db.collection("hospital_kiosk_mistakesbackup_byuser").document(user_id)

    existing_doc = doc_ref.get()
    existing_data = existing_doc.to_dict() if existing_doc.exists else {}
    wrong_list = existing_data.get("wrong_selections", [])

    for item in data.wrong_selections:
        item_with_time = item.dict()
        item_with_time["timestamp"] = datetime.now(timezone.utc).isoformat()
        wrong_list.append(item_with_time)

    doc_ref.set({"wrong_selections": wrong_list})

    return JSONResponse(
        content={
            "message": f"{len(data.wrong_selections)}개의 오답이 저장되었습니다.",
            "user_id": user_id
        },
        media_type="application/json; charset=utf-8"  # 한글 인코딩
    )
