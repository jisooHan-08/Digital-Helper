# 병원 키오스크 오답 피드백 조회
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse  # 
from firebase_init import db

router = APIRouter()

@router.get("/hospital-kiosk/mistake-feedback")
def get_hospital_kiosk_mistake_feedback(request: Request):
    user_id = request.headers.get("user-id")

    if not user_id:
        raise HTTPException(status_code=400, detail="user-id 헤더가 누락되었습니다.")

    doc = db.collection("hospital_kiosk_mistakesbackup_byuser").document(user_id).get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail=f"{user_id}에 대한 오답 기록이 없습니다.")

    data = doc.to_dict()
    return JSONResponse(
        content={
            "user_id": user_id,
            "wrong_selections": data.get("wrong_selections", [])
        },
        media_type="application/json; charset=utf-8"  # 한글 깨짐 방지
    )
